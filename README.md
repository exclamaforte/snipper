## Install
Requires python3.x. Start server via `python3 main.py`. Still in alpha so we only have one partially completed plugin for neovim.

## Plugins
https://github.com/Daphron/vim-snipper


## Inspiration
Dan is a Vim user and I am a Emacs user. In order to unite our warring tribes, we decided to band together and create a snippet generator that will work on every editor.

## What it does
Below is a picture of a demo of the snippet generation.
It looks for patterns in what you type and adds a star character when we can generalize the input. For example:
```
def foo():
def bar():
```
These two lines differ only in the 'foo' and 'bar' slot. Our algorithm finds this and replaces it with a * entry field to create:
```
def * ():
```
which an editor transforms into a valid snippet.

## How we built it
As you type, the characters are sent to our snippet generating server by the editor. The editor listens for the server to send back good snippets, which the server does as soon as it finds them.

## What's next
This could work with multiple editors sending snippets at the same time, and we have plans to make it work remotely so that one could have a general snippet server that works wherever you're coding on.
