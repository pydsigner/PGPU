#! /usr/bin/env python
import os

import mutagen
import mutagen.mp3, mutagen.oggvorbis

import pgpu.tkinter2x as tk
from pgpu.tkinter2x.filedialog import askopenfilename
from pgpu.tkinter2x.constants import *
from pgpu.dictionaries import GUIDict, UpdatingDict


MTYPES = {'mp3': mutagen.mp3.MP3, 'ogg': mutagen.oggvorbis.Open}


class MutagenGUI(tk.Frame):
    ignore = ['coverart', 'coverartmime']
    def __init__(self, master, *args, **kw):
        tk.Frame.__init__(self, master, *args, **kw)
        
        bpack = tk.Frame(self)
        tk.Button(bpack, text = 'Save changes', command = self.dump_changes
                ).pack(side = RIGHT, expand = True, fill = X)
        tk.Button(bpack, text = 'Open new', command = self.load_new
                ).pack(side = LEFT, expand = True, fill = X)
        self.title_label = tk.Label(bpack)
        self.title_label.pack(side = BOTTOM, expand = True, fill = X)
        bpack.pack(side = BOTTOM, expand = True, fill = X)
        
        ret = self.load_new()
        if not ret:
            self._root().destroy()
    
    def load_new(self):
        fl = askopenfilename(
          filetypes=[(k, '*.%s' % k) for k in MTYPES] + [('Any', '*.*')], 
          title='Choose music')
        
        if not fl:
            return
        self.title_label['text'] = os.path.split(fl)[1]
        
        self.opened = MTYPES.get(fl.split('.')[-1])(fl)
        
        self.d = UpdatingDict(self.opened)
        for k in self.ignore:
            self.d.pop(k, None)
        
        try:
            self.gdict.destroy()
        except AttributeError:
            pass
        
        self.gdict = GUIDict(self, self.d)
        self.gdict.pack(side=TOP, expand=True, fill=BOTH)
        return True
    
    def dump_changes(self):
        for k in self.d:
            self.opened[k] = self.d[k]
        for k in self.opened:
            if k not in list(self.d) + self.ignore:
                del self.opened[k]
        self.opened.save()


def main():
    win = tk.Tk()
    win.title('Mutagen GUI')
    tk.Button(win, text='Quit', command=win.destroy).grid(sticky=NW+SE, row=1, 
                                                          column=0)
    
    MutagenGUI(win).grid(sticky=NW+SE, row=0, column=0)
    win.rowconfigure(0, weight=6)
    win.rowconfigure(1, weight=1)
    win.columnconfigure(0, weight=1)
    win.mainloop()

if __name__ == '__main__':
    main()
