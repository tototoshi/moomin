# moomin

A Command line tool for MoinMoin wiki.

## Install

1. First, install 'moomin' command.

```
$ sudo python setup.py install
```

2. Create ~/.moinrc.

```
http://your.moinmoin.url user:password
```

## Usage

```
moomin [command] args...

command:
  - list                  list all pages.
  - browse <page>         open the page with your default browser
  - show <page>           show the page.
  - save <page> <file>    update page with the content of the file.
```

## Using with Emacs

1. Install moomin.el in ~/.emacs.d
2. Add `(require 'moomin)` in your .emacs.d/init.el

`helm-moomin` open wiki page in your emacs' buffer. Press `C-c C-c` to save the page.

## TODO

- Checking conflict.
- Reducing http request.

## LICENSE

BSD License
