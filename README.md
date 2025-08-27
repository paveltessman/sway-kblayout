# Sway Keyboard Layout Switcher

This utility allows you to have window-specific keyboard layout on SwayWM, a.k.a keyboard layout per window.

It remembers keyboard layout at the moment you've changed focus from the window, and then restores the remembered layout when you focuse the window again.

I don't guarantee there're no bugs here. If you have any, leave an issue, and I will look at it.


## Installation

### Prebuit binary

You can download a binary from the [Releases page](https://github.com/paveltessman/sway-kblayout/releases/).

### Build from source

Or you can build it from source.

First, clone the repo:

```bash
git clone https://github.com/paveltessman/sway-kblayout.git && cd sway-kblayout
```

Run the build script:

```bash
./build.sh
```

After the build process is complete, the executable will be in the `dist/` directory.


## Usage

The simplest way is to just run the executable:

```bash
./sway-kbswitcher-1.1.0 run
```

Or add this to the SwayWM config:

```
exec /path/to/sway-kbswitcher-1.0.0 run
```

You can specify default layout:

```
exec /path/to/sway-kbswitcher-1.0.0 run --default-layout [index]
```

`[index]` is the layout index you want. Probably it's either `0` or `1`. Maybe I will add an option to get all layout indices in the future.

Default layout is the layout that is chosen when there is no saved layout for the focused window (e.g. when the window has just been created and it is focused for the first time). If no default layout is specified, then the current one is chosen.


Also is can be run it with debug logs enabled:

```
./sway-kbswitcher-1.1.0 run --debug
```

But I don't know why would you do that.
