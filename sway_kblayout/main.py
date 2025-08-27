import sys
import logging
from typing import Literal

import click
from i3ipc import Connection, Event


logger = logging.getLogger("main")

layouts: dict[str, int] = {}

previously_focused_window_id: int | None = None
default_kb_layout_index: int | None = None

i3 = Connection()


@click.group()
def cli(): ...


def configure_logging(level: Literal[10, 20, 30, 40]) -> None:
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z",
    )


def decide_fallblack_kb_layout_index(current_kb_layout_index: int) -> int:
    if default_kb_layout_index is None:
        logger.debug(
            f"fallblack kb layout value is the current layout: {current_kb_layout_index}"
        )
        return current_kb_layout_index
    else:
        logger.debug(
            f"fallblack kb layout value is the default one: {default_kb_layout_index}"
        )
        return default_kb_layout_index


def get_current_kb_layout_index() -> str:
    inputs = i3.get_inputs()
    for device in inputs:
        if device.type == "keyboard":
            return device.xkb_active_layout_index


def set_kb_layout(window, index: int) -> str:
    reply = window.command(f"input type:keyboard xkb_switch_layout {index}")
    if not reply[0].success:
        logger.error(f"Error setting kb layout to {index}: {reply[0].error}")


def initialize() -> None:
    global previously_focused_window_id
    focused = i3.get_tree().find_focused()
    if focused:
        previously_focused_window_id = focused.id


def on_window_focus(i3, e):
    global previously_focused_window_id
    logger.debug("========== New focus window event ===========")

    current_kb_layout_index = get_current_kb_layout_index()

    logger.debug(f"{previously_focused_window_id=}")
    logger.debug(f"{current_kb_layout_index=}")

    fallblack_kb_layout_index = decide_fallblack_kb_layout_index(
        current_kb_layout_index
    )

    previously_focused = None
    if previously_focused_window_id:
        logger.debug(
            f"trying to find previously focused window with id {previously_focused_window_id}"
        )
        previously_focused = i3.get_tree().find_by_id(previously_focused_window_id)

    if previously_focused:
        logger.debug(
            f"found previously focused window: {previously_focused.id}. "
            f"Window name: {previously_focused.name!r}."
        )
        layouts[previously_focused.id] = current_kb_layout_index
        logger.debug(
            f"Saved kb layout of previous window. Current layout memory: {layouts}"
        )

    new_focused = i3.get_tree().find_focused()
    logger.debug(f"trying to get new focused window")
    if new_focused:
        logger.debug(
            f"found new focused window: {new_focused.id}. name: {new_focused.name!r}"
        )
        previously_focused_window_id = new_focused.id
        new_kb_layout = layouts.get(new_focused.id, fallblack_kb_layout_index)
        logger.debug(f"{new_kb_layout=}")
        set_kb_layout(new_focused, new_kb_layout)

    logger.debug("========== Event processed ===========")


@cli.command()
@click.option(
    "--default-layout",
    default=None,
    type=int,
)
@click.option("--debug", is_flag=True)
def run(default_layout: int | None, debug: bool):
    global default_kb_layout_index
    default_kb_layout_index = default_layout

    logger.debug(f"{debug=}")
    if debug:
        configure_logging(logging.DEBUG)

    logger.debug(f"{default_kb_layout_index=}")

    initialize()
    i3.on(Event.WINDOW_FOCUS, on_window_focus)
    i3.main()


if __name__ == "__main__":
    if getattr(sys, "frozen", False):
        cli(sys.argv[1:])
