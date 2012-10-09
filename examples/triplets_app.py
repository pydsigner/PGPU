#! /usr/bin/env python

import pgpu.tk_utils as tk_utils
from pgpu.tkinter2x.constants import *
import pgpu.tkinter2x as tk
from pgpu.security import fetcher, encoder_classes


def get_encoder():
    c = encoder_var.get()
    return fetcher(c)


def set_buttons(t = 100):
    e_btn['state'] = NORMAL if 'encode' in dir(get_encoder()) else DISABLED
    d_btn['state'] = NORMAL if 'decode' in dir(get_encoder()) else DISABLED
    win.after(t, set_buttons, t)


def do_decode():
    out_text.settext(get_encoder().decode(in_text.gettext()))


def do_encode():
    out_text.settext(get_encoder().encode(in_text.gettext()))


font = ('Helvetica', 13, 'normal')

win = tk.Tk()
win.title('Triplet Code Program')

entrybox = tk.Frame(win)
sidebar = tk.Frame(win)

all_secure = list(encoder_classes)
all_secure.sort()

encoder_var = tk.StringVar()
tk.OptionMenu(sidebar, encoder_var, all_secure[0], *all_secure[1:]
              ).pack(side=TOP, fill=X, expand=True, anchor=N, pady=10)
encoder_var.set(all_secure[0])

win.columnconfigure(0, weight=100)

entrybox.grid(row=0, column=0)
sidebar.grid(row=0, column=1, sticky=N + SW)

buttonbox = tk.Frame(sidebar)
buttonbox.pack(side=BOTTOM, fill=X, expand=True, anchor=S)

entrybox.columnconfigure(1, weight=6)
entrybox.columnconfigure(0, weight=1)

tk.Label(entrybox, font=font, text='Input:'
         ).grid(column=0, sticky=EW + N, row=0)
tk.Label(entrybox, font=font, text='Output:'
         ).grid(column=0, sticky=EW + N, row=2)

in_text = tk_utils.STextPlus(entrybox, wrap=WORD, height=10)
out_text = tk_utils.STextPlus(entrybox, height=10)

in_text.grid(column=1, sticky=EW, row=0, rowspan=2)
out_text.grid(column=1, sticky=EW, row=2, rowspan=2)

tk.Button(entrybox, font=font, text='Clear', command=in_text.clear
          ).grid(column=0, sticky=EW + S, row=1)
tk.Button(entrybox, font=font, text='Clear', command=out_text.clear
          ).grid(column=0, sticky=EW + S, row=3)

tk.Button(buttonbox, text='Quit', command=win.destroy, font=font
          ).pack(anchor=S, side=BOTTOM, fill=X, expand=True)

e_btn = tk.Button(buttonbox, text='Encode', command=do_encode, font=font)
e_btn.pack(anchor=S, side=BOTTOM, fill=X, expand=True)

d_btn = tk.Button(buttonbox, text = 'Decode', command=do_decode, font=font)
d_btn.pack(anchor=S, side=BOTTOM, fill=X, expand=True)

set_buttons(200)
tk.mainloop()
