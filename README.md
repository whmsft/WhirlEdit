![whirlEdit full logo](logo-full.png)

when writing "whirlEdit" remember to capitalize "E" because it focuses more on editing that "whirling"

[![Old screenshot](https://github.com/whmsft/WhirlEdit/raw/2f83fac9a30d441cfb4eb9a5c0964ffb9a980f6d/screenshot.png)](https://github.com/whmsft/WhirlEdit/raw/2f83fac9a30d441cfb4eb9a5c0964ffb9a980f6d/screenshot.png) 
<i>Screenshot from 24 October 2021</i>

[![Build Status](https://github.com/whmsft/whirledit/actions/workflows/python-app.yml/badge.svg)](https://github.com/whmsft/whirledit/actions/workflows/python-app.yml)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![GitHub license](https://img.shields.io/github/license/Whmsft/whirledit.svg)](https://github.com/whirlpool-programmer/whirledit/blob/master/LICENSE)
![Size](https://shields.io/github/repo-size/Whmsft/WhirlEdit)

### Please NOTE: WhirlEdit is now obsolete! I just started [Thee editor](https://github.com/whmsft/thee)

WhirlEdit is still usable if you want to
<hr>

FUTURE NOTES: (what i want whirlEdit to be)
```
better extensions (possible rewrite of extension manager)
more and more syntax highlighting  -> doing, Doing, DOING!
change "wday" and "confscript" formats to YAML
better UI -> LARGE rewriting
lightweight  -> Nuitka (see below)
switch executable building from pyinstaller to nuitka -> Under progress
```

CHANGELOG:
```
v4.1:
> UI:
  + Slight rework
  - bugfixes
> features:
  + extensions modify execution code
  - remove updating features (see #8)

v4.0:
> UI
  + Complete UI change with ttkbootstrap
  + introduction to Monokai-Aora (theme & scheme)
  + auto-indent when last line is indented
  + Welcome Screen
  + new close icon for tabs
> features
  + widgets' code in "widgets.py"
  + default data in "data.py"
  + updating feature
  + extensions install via command line

v3.5:
> bugfixes
  - syntax dropdown chooser
> UI
  + new style syntax change button
> features
  + an image previewer
  + raise error on UnicodeDecodeError
 
v3.4:
> bug fixes
> UI
  + better about window
> features
  + Find
  + Find & replace

v3.2.2:
> refix bug
  - font with ' '
> UI
  + Tab with close button
> features
  + runners saved in 'confscript'

v3.1.1:
> bugfixes
  - unable to update config
  - program crashes with font names having space ' ' character
> UI
  + added a "Confirm & Save" button to Settings pane

v3.1:
> Side Bar pane(s)
> Configuration File
> Many themes
> Many syntax Support
> simple terminal
> Ease of use 
> Tooltips for ease of use

v2:
> complete rewrite
> python syntax
> tabs
> scrollbar fix
> key bindings
> runner
> new theme (azure ttk theme)
> made with ttk instead of tk

v1:
> initial
```
<br>
<hr>

## WhirlEdit can't:

1. edit large files (30kb+) (it may slow down loading & customization experience) (even the source code "main.py" can't be opened without a lag).

2. preview most of images in previewer (it is not so advanced)

3. be "really" stable (it may crash on any error, either internal problem or extension)

4. highlight multi-line strings/comments (due to a "tkcode" problem)

<hr>

# And now something completely different:

![Joke](https://readme-jokes.vercel.app/api)

(c) 2020-22 whmsft
Licensed under GNU GPL v3
