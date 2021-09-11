# PiTFT Manager

Display manager for framebuffer devices (like the PiTFT) on Raspberry Pi.

## What's a display manager?

Simply put, a display manager is an application that provides other applications with access to the display.
In practice, this means you can create your own apps for it, switch between apps on the fly, and more!

## Why PiTFT?

The Adafruit PiTFT 3.5" is what I'm developing it on/for, so I chose to reference it in the name.

## What apps come with it?

Right now, there are two included apps:

* `system` - displays system information
* `fortune` - displays fortune cookies
  * Note: requires `fortune-mod` to be installed!

## Creating apps

Creating apps is simple, each app is a Python module that provides an `App` class,
which should inherit from the `apps.AbstractApp` class. Then you just need to implement
the `run_iteration` method and have it do whatever you want the app to do!

More documentation for development coming soon.
