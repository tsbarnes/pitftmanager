# PiTFT Manager

Display manager for framebuffer devices (like the PiTFT) on Raspberry Pi.

## What's a display manager?

Simply put, a display manager is an application that provides other applications with access to the display.
In practice, this means you can create your own apps for it, switch between apps on the fly, and more!

## Why PiTFT?

The Adafruit PiTFT 3.5" is what I'm developing it on/for, so I chose to reference it in the name.

## What apps come with it?

Right now, there are three included apps:

* `system` - displays system information
* `fortune` - displays fortune cookies
  * Note: requires `fortune-mod` to be installed!
* `affirmations` - displays positive affirmations

## Creating apps

Creating apps is simple, each app is a Python module that provides an `App` class,
which should inherit from the `apps.AbstractApp` class. Then you just need to implement
the `run_iteration` method and have it do whatever you want the app to do!

More documentation for development coming soon.

## Installation

* First, clone the repository onto the Raspberry Pi, I recommend cloning it to `/home/pi/pitftmanager` and then change directory into it.
* Second, install the required Python libraries.
* Third, link the `pitftmanager.service` file into `/etc/systemd/system`.
* Fourth, enable the `systemd` service.
* Lastly, start the `systemd` service, or reboot.

Quick command list to install:

```shell
git clone https://github.com/tsbarnes/pitftmanager.git ~/pitftmanager
cd ~/pitftmanager
sudo pip3 install -r requirements.txt
sudo ln -s /home/pi/pitftmanager/pitftmanager.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable pitftmanager
sudo systemctl start pitftmanager
```