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
./sway-kbswitcher-1.0.0
```

Or add this to the SwayWM config:

```
exec /path/to/sway-kbswitcher-1.0.0
```
