# CodeReplay for Sublime Text 3

When enabled, CodeReplay records everything you type into your editor. Think of it as a text-based screen recorder. You can then take the recordings and replay them.

## Installation

### Manual

Clone, copy, or unzip this repository into your Sublime Text packages folder (`Preferences > Browse Packages`). Restart Sublime Text to allow the dependency to load.

### Package Control

We haven't packaged for Package Control yet, but we plan to!

## Getting Started

Simply place a file named `RECORD` (no extension) in any folder whose files you wish to record. The entire path is checked, so placing it in any parent directory will record all subdirectories.

Now the plugin will record your keystrokes alongside your code in a file named `.$FILENAME.keys`. For example, if you were editing `README.md` a file named `.README.md.keys` will be created to store anything you type.

## Replay

Simply grab the contents of the `.keys` file you want to replay and head on over to `the domain I haven't bought yet`.