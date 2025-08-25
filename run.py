import logging
from i3ipc import Connection, Event


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")

layouts: dict[str, int] = {}

previously_focused_window_id: int | None = None

i3 = Connection()


def get_current_kb_layout_index() -> str:
    inputs = i3.get_inputs()
    for device in inputs:
        if device.type == "keyboard":
            return device.xkb_active_layout_index


def set_kb_layout(window, index: int) -> str:
    reply = window.command(f"input type:keyboard xkb_switch_layout {index}")
    if not reply[0].success:
        raise AssertionError(f"Error setting kb layout to {index}: {reply[0].error}")


def on_window_focus(i3, e):
    global previously_focused_window_id
    current_kb_layout_index = get_current_kb_layout_index()

    logger.debug("========== New focus window event ===========")
    logger.debug(f"{previously_focused_window_id=}")
    logger.debug(f"{current_kb_layout_index=}")

    previously_focused = None
    if previously_focused_window_id:
        logger.debug(
            f"trying to find previously focused window with id {previously_focused_window_id}"
        )
        previously_focused = i3.get_tree().find_by_id(previously_focused_window_id)

    if previously_focused:
        logger.debug(f"found previously focused window: {previously_focused.id}")
        layouts[previously_focused.id] = current_kb_layout_index
        logger.debug(
            f"Saved kb layout of previous window. Current layout memory: {layouts}"
        )

    new_focused = i3.get_tree().find_focused()
    logger.debug(f"trying to get new focused window")
    if new_focused:
        logger.debug(f"found new focused window: {new_focused.id}")
        previously_focused_window_id = new_focused.id
        new_kb_layout = layouts.get(new_focused.id, current_kb_layout_index)
        logger.debug(f"{new_kb_layout=}")
        set_kb_layout(new_focused, new_kb_layout)

    logger.debug("========== Event processed ===========")


def main():
    i3.on(Event.WINDOW_FOCUS, on_window_focus)
    try:
        i3.main()
    except KeyboardInterrupt:
        print("Bye!")


if __name__ == "__main__":
    raise SystemExit(main())
