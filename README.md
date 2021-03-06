Pydsigner's Generic Python Utilities
================================================================================

A collection of handy Python utilities created by Daniel Foerster (a.k.a.
pydsigner)

<pydsigner@gmail.com>

http://github.com/pydsigner/PGPU


PGPU is distributed under the LGPLv3 (or greater), see COPYING for details.

--------------------------------------------------------------------------------

The modules and packages included do not necessarily relate to one another, so
they will be described here individually.

* tkinter2x is a package providing a Python3-like Tkinter wrapping for both
  Python3 and Python2.

* compatibility.py contains some name-mappings and a Print() function to
  provide a Python3-like feel to some of the major builtin differences.
* dictionaries.py provides several special dictionary implementations,
  including a SortedDict() and a GUIDict() with a Tkinter interface.
* encoding.py contains a unified interface to many different standard encodings
  and hashers, as well as some unique ones.
* file_utils.py includes functions for working with files and filesystems, such
  a simple configuration file reader/writer, and a recursive folder size
  finder.
* iter_utils.py is for working with all sorts of iterables, with functions for
  multiple replacements, sectioning, flattening, and so on.
* math_utils.py contains a broad assortment of mathematical utilities,
  including functions for factoring and limiting numbers and finding euclidean
  distances, as well as a Decimal() subclass with trigonometric methods and a
  powerful Vector() class.
* string_utils.py contains utilities for working with strings.
* time_widgets.py includes Tkinter mega-widgets for working with time, such as
  a timer and a chronograph (stop-watch).
* tk_utils.py contains general Tkinter utilities, including several powerful
  extensions to Text(), a font-picker, and a CSS-like best font selector.
* wrappers.py contains function-like classes for some common cases, such as
  chaining several function calls together or counting objects, or simply
  returning the same value.

--------------------------------------------------------------------------------

To see some examples:

    $ cd examples

And then:

    $ python triplets_app.py

This example is a interesting demo that uses tk_utils, encoding, and tkinter2x.

    $ python test_dictionaries.py

This example is a demo/test of dictionaries.UpdatingDict() and
dictionaries.SortedDict().

    $ python test_libs.py

This example is a demo/test of math_utils, iter_utils, file_utils, and
security. Can easily and most likely will be extended in the future.

    $ python metagui.py

This example is a GUI implementation of an OGG and MP3 tag editor. It uses
dictionaries.GUIDict(), but requires mutagen for tag loading.

More examples are desired, so if you make a small program heavily using this
library that you would like to share, please send it to me.

--------------------------------------------------------------------------------

If you would like to contribute to PGPU in any way, whether through bug
reports, bug fixes, better code, or new code altogether, please visit the Github page and open an Issue or Pull Request.

--------------------------------------------------------------------------------

If you use this library to do something useful, be sure to let me know! It is
important to me to know what sort of user base my libraries have before making
major API changes.

--------------------------------------------------------------------------------

Thanks to:
* Mark Lutz, for inspiring the tk_utils.STextPlus() widget
* The www.python-forum.org community, for helping me learn the RIGHT way to
  code in Python
* The PGU packagers, for a package I could base mine off of
* The FIFE packagers, for a package clearing up some of my questions
