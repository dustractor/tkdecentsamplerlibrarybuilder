# version 0.2

import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import pathlib
import os
import sys
import shutil
from xml.dom import minidom
from string import Template
import argparse

_DESKTOP_BGFILE = pathlib.Path.home() / "Desktop" / "bg.png"

args = argparse.ArgumentParser()
args.add_argument("--input-folder",type=pathlib.Path)
args.add_argument("--output-folder",type=pathlib.Path)
args.add_argument("--background-image",type=pathlib.Path,
                  default=_DESKTOP_BGFILE)
args.add_argument("--start-note",type=int,default=21)
ns = args.parse_args()

print("ns:",ns)

# sys.exit()


_SENTINEL_UNSET = ":NOT SET:"
_MSG_NOT_READY = "Not enough info to build!"
_MSG_BUILD_START = "Build starting..."

#{{{1 noteinfo

noteinfo = [
    [0,"C-1"],
    [1,"C#-1"],
    [2,"D-1"],
    [3,"D#-1"],
    [4,"E-1"],
    [5,"F-1"],
    [6,"F#-1"],
    [7,"G-1"],
    [8,"G#-1"],
    [9,"A-1"],
    [10,"A#-1"],
    [11,"B-1"],
    [12,"C0"],
    [13,"C#0"],
    [14,"D0"],
    [15,"D#0"],
    [16,"E0"],
    [17,"F0"],
    [18,"F#0"],
    [19,"G0"],
    [20,"G#0"],
    [21,"A0"],
    [22,"A#0"],
    [23,"B0"],
    [24,"C1"],
    [25,"C#1"],
    [26,"D1"],
    [27,"D#1"],
    [28,"E1"],
    [29,"F1"],
    [30,"F#1"],
    [31,"G1"],
    [32,"G#1"],
    [33,"A1"],
    [34,"A#1"],
    [35,"B1"],
    [36,"C2"],
    [37,"C#2"],
    [38,"D2"],
    [39,"D#2"],
    [40,"E2"],
    [41,"F2"],
    [42,"F#2"],
    [43,"G2"],
    [44,"G#2"],
    [45,"A2"],
    [46,"A#2"],
    [47,"B2"],
    [48,"C3"],
    [49,"C#3"],
    [50,"D3"],
    [51,"D#3"],
    [52,"E3"],
    [53,"F3"],
    [54,"F#3"],
    [55,"G3"],
    [56,"G#3"],
    [57,"A3"],
    [58,"A#3"],
    [59,"B3"],
    [60,"C4"],
    [61,"C#4"],
    [62,"D4"],
    [63,"D#4"],
    [64,"E4"],
    [65,"F4"],
    [66,"F#4"],
    [67,"G4"],
    [68,"G#4"],
    [69,"A4"],
    [70,"A#4"],
    [71,"B4"],
    [72,"C5"],
    [73,"C#5"],
    [74,"D5"],
    [75,"D#5"],
    [76,"E5"],
    [77,"F5"],
    [78,"F#5"],
    [79,"G5"],
    [80,"G#5"],
    [81,"A5"],
    [82,"A#5"],
    [83,"B5"],
    [84,"C6"],
    [85,"C#6"],
    [86,"D6"],
    [87,"D#6"],
    [88,"E6"],
    [89,"F6"],
    [90,"F#6"],
    [91,"G6"],
    [92,"G#6"],
    [93,"A6"],
    [94,"A#6"],
    [95,"B6"],
    [96,"C7"],
    [97,"C#7"],
    [98,"D7"],
    [99,"D#7"],
    [100,"E7"],
    [101,"F7"],
    [102,"F#7"],
    [103,"G7"],
    [104,"G#7"],
    [105,"A7"],
    [106,"A#7"],
    [107,"B7"],
    [108,"C8"],
    [109,"C#8"],
    [110,"D8"],
    [111,"D#8"],
    [112,"E8"],
    [113,"F8"],
    [114,"F#8"],
    [115,"G8"],
    [116,"G#8"],
    [117,"A8"],
    [118,"A#8"],
    [119,"B8"],
    [120,"C9"],
    [121,"C#9"],
    [122,"D9"],
    [123,"D#9"],
    [124,"E9"],
    [125,"F9"],
    [126,"F#9"],
    [127,"G9"]
    ]

#}}}1

# {{{1 boilerplate
boilerplate = Template(
    """<?xml version="1.0" encoding="UTF-8"?>
<DecentSampler minVersion="1.0.0">
  <ui width="812" height="375" layoutMode="relative"
      bgMode="top_left"
      bgImage="$bg_img">
    <tab name="main">
      <labeled-knob x="445" y="75" width="90" textSize="16" textColor="AA000000" 
                    trackForegroundColor="CC000000" trackBackgroundColor="66999999" 
                    label="Attack" type="float" minValue="0.0" maxValue="4.0" value="0.01" >
        <binding type="amp" level="instrument" position="0" parameter="ENV_ATTACK" />
      </labeled-knob>
      <labeled-knob x="515" y="75" width="90" textSize="16" textColor="AA000000" 
                    trackForegroundColor="CC000000" trackBackgroundColor="66999999" 
                    label="Release" type="float" minValue="0.0" maxValue="20.0" value="1" >
        <binding type="amp" level="instrument" position="0" parameter="ENV_RELEASE" />
      </labeled-knob>
      <labeled-knob x="585" y="75" width="90" textSize="16" textColor="AA000000" 
                    trackForegroundColor="CC000000" trackBackgroundColor="66999999" 
                    label="Chorus" type="float" minValue="0.0" maxValue="1" value="0" >
        <binding type="effect" level="instrument" position="1" parameter="FX_MIX" />
      </labeled-knob>
      <labeled-knob x="655" y="75" width="90" textSize="16" textColor="FF000000"
                    trackForegroundColor="CC000000" trackBackgroundColor="66999999"
                    label="Tone" type="float" minValue="0" maxValue="1" value="1">
        <binding type="effect" level="instrument" position="0" parameter="FX_FILTER_FREQUENCY"
                 translation="table" 
                 translationTable="0,33;0.3,150;0.4,450;0.5,1100;0.7,4100;0.9,11000;1.0001,22000"/>
      </labeled-knob>
      <labeled-knob x="725" y="75" width="90" textSize="16" textColor="AA000000" 
                    trackForegroundColor="CC000000" trackBackgroundColor="66999999" 
                    label="Reverb" type="percent" minValue="0" maxValue="100" 
                    textColor="FF000000" value="50">
        <binding type="effect" level="instrument" position="2" 
                 parameter="FX_REVERB_WET_LEVEL" translation="linear" 
                 translationOutputMin="0" translationOutputMax="1" />
      </labeled-knob>
    </tab>
  </ui>
  <groups attack="0.000" decay="25" sustain="1.0" release="0.430" volume="-3dB">
        $samples
  </groups>
  <effects>
    <effect type="lowpass" frequency="22000.0"/>
    <effect type="chorus"  mix="0.0" modDepth="0.2" modRate="0.2" />
    <effect type="reverb" wetLevel="0.5"/>
  </effects>
  <midi>
    <!-- This causes MIDI CC 1 to control the 4th knob (cutoff) -->
    <cc number="1">
      <binding level="ui" type="control" parameter="VALUE" position="3" 
               translation="linear" translationOutputMin="0" 
               translationOutputMax="1" />
    </cc>
  </midi>
</DecentSampler>
""") #}}}1

#{{{1 minidom setup

def _elem_inplace_addition(self,other):
    self.appendChild(other)
    return self

def _elem_textnode(self,text):
    textnode = self.ownerDocument.createTextNode(text)
    self.appendChild(textnode)
    return self

def _elem_set_attributes_from_tuple(self,*args):
    for k,v in args:
        self.setAttribute(k,str(v))
    return self

minidom.Element.__iadd__ = _elem_inplace_addition
minidom.Element.txt = _elem_textnode
minidom.Element.attrt = _elem_set_attributes_from_tuple
minidom.Element.__str__ = lambda s:s.toprettyxml().strip()

#}}}1

#{{{1 Toolbar
class Toolbar(tk.Frame):
    def app_quit(self):
        print("bye")
        self.quit()
    def choose_input_dir(self,*event):
        d = filedialog.askdirectory()
        print("d:",d)
        newpath = pathlib.Path(d).resolve()
        print("newpath:",newpath)
        if newpath.is_dir():
            self.master.input_dir.set(str(newpath))
    def choose_output_dir(self,*event):
        d = filedialog.askdirectory()
        print("d:",d)
        newpath = pathlib.Path(d).resolve()
        print("newpath:",newpath)
        if newpath.is_dir():
            self.master.output_dir.set(str(newpath))

    def choose_bg_image(self,*event):
        d = filedialog.askopenfilename(filetypes=[("PNG",".png")])
        print("d:",d)
        newpath = pathlib.Path(d).resolve()
        print("newpath:",newpath)
        if newpath.is_file():
            self.master.bgimg.set(str(newpath))

    def build_library(self,*event):
        if not self.build_library_poll():
            self.master.status_message.set(_MSG_NOT_READY)
            return

        self.master.status_message.set(_MSG_BUILD_START)
        self.master.update_idletasks()

        idir = pathlib.Path(self.master.input_dir.get())
        odir = pathlib.Path(self.master.output_dir.get())
        bgimg = pathlib.Path(self.master.bgimg.get())
        notenum = int(self.master.startnote.get())
        self.master.output_dir.set(self.master.output_dir.get())
        oname = self.master.output_name.get()

        samples = list(idir.glob("*.wav"))
        for s in samples:
            shutil.copy(s,odir)
            print(s,"copied to",odir)
            
        shutil.copy(bgimg,odir)

        print(bgimg,"copied to",odir)

        presetfilepath = odir / (oname + ".dspreset")
        libraryfilepath = odir.parent / (oname + ".dslibrary")

        doc = minidom.Document()
        elem = doc.createElement
        root = elem("group")

        for s in odir.glob("*.wav"):
            sample_elem = elem("sample")
            sample_elem.attrt(("path",s.name))
            sample_elem.attrt(("loNote",str(notenum)))
            sample_elem.attrt(("hiNote",str(notenum)))
            sample_elem.attrt(("rootNote",str(notenum)))
            root += sample_elem
            notenum += 1

        groupxml = root.toprettyxml().strip()
        mapping = dict(bg_img=str(bgimg),samples=groupxml)
        group_content_str = boilerplate.substitute(mapping)

        with open(presetfilepath,"w") as presetfile:
            presetfile.write(group_content_str)

        print("preset file written in",odir)
        print("zipping",odir,"up...",end="")
        shutil.make_archive(libraryfilepath,"zip",odir)
        print("zipped OK")
        print("zip archive created:",libraryfilepath)
        zippedlibpath = pathlib.Path(str(libraryfilepath) + ".zip")
        zippedlibpath.rename(libraryfilepath)
        print("archive renamed with dslibrary suffix(",zippedlibpath,")")
        os.startfile(odir.parent)
        print("BUILD COMPLETED")
        print("-"*40)
        self.master.status_message.set("Built "+libraryfilepath.name)

    def build_library_poll(self):
        idir_t = self.master.input_dir.get()
        odir_t = self.master.output_dir.get()
        bgimg_t = self.master.bgimg.get()
        if idir_t == odir_t:
            return False
        if not idir_t or (idir_t == _SENTINEL_UNSET):
            return False
        if not odir_t or (odir_t == _SENTINEL_UNSET):
            return False
        if not bgimg_t or (odir_t == _SENTINEL_UNSET):
            return False
        idir = pathlib.Path(idir_t)
        odir = pathlib.Path(odir_t)
        bgimg = pathlib.Path(bgimg_t)
        if not idir.is_dir():
            return False
        if not odir.is_dir():
            return False
        if not bgimg.is_file():
            return False
        if not bgimg.suffix.lower() == ".png":
            return False
        return True


        
    def __init__(self,master):
        super().__init__(master)
        self.menubutton = tk.Menubutton(self,text="Menu")
        self.menubutton.menu = tk.Menu(self.menubutton,tearoff=False)
        self.menubutton["menu"] = self.menubutton.menu
        self.menubutton.menu.add_command(command=self.choose_input_dir,
                                         label="Choose Input Folder...",
                                         accelerator="Ctrl+I")
        self.menubutton.menu.add_command(command=self.choose_output_dir,
                                         label="Choose Output Folder...",
                                         accelerator="Ctrl+O")
        self.menubutton.menu.add_command(command=self.choose_bg_image,
                                         label="Choose Background Image...",
                                         accelerator="Ctrl+B")
        self.menubutton.menu.add_command(command=self.build_library,
                                         label="Build Library",
                                         accelerator="Ctrl+K")
        self.menubutton.menu.add_command(command=self.app_quit,
                                         label="Exit",
                                         accelerator="Ctrl+Q")
        self.menubutton.pack(anchor="w")
#}}}1

#{{{1 App

class App(tk.Tk):

    #{{{2 input_dir_info trace function

    def input_dir_info(self,*ignore):
        print("-"*40)
        print("Input Folder Info:")
        p = self.input_dir.get()
        if p != _SENTINEL_UNSET:
            path = pathlib.Path(p)
            print("path:",path)
            for n,f in enumerate(path.glob("*.wav")):
                print("n,f:",n,f)
            print(path,"contains",n+1,"wav files")
            self.input_dir_wavfile_count.set(n+1)
        else:
            print("no info")
        print("-"*40)

    #}}}2

    #{{{2 output_dir_info trace function

    def output_dir_info(self,*ignore):
        print("-"*40)
        print("Output Folder Info:")
        p = self.output_dir.get()
        if p != _SENTINEL_UNSET:
            path = pathlib.Path(p)
            print("path:",path)
            name = path.name
            print("name:",name)
            name = name.replace(" ","_")
            self.output_name.set(name)
        else:
            print("no info")
        print("-"*40)

    #}}}2

    #{{{2 startnote_info trace function

    def startnote_info(self,*ignore):
        note_i = self.startnote.get()
        print("note_i:",note_i)
        info = noteinfo[int(note_i)]
        self.startnote_info.set(info)

    #}}}2
    
    def __init__(self):
        super().__init__()
        """Set up the variables"""
        self.input_dir = tk.StringVar()
        if ns.input_folder and ns.input_folder.is_dir():
            self.input_dir.set(ns.input_folder)
        else:
            self.input_dir.set(_SENTINEL_UNSET)
        self.input_dir.trace("w",self.input_dir_info)
        self.input_dir_wavfile_count = tk.IntVar()

        self.output_dir = tk.StringVar()
        if ns.output_folder and ns.output_folder.is_dir():
            self.output_dir.set(ns.output_folder)
        else:
            self.output_dir.set(_SENTINEL_UNSET)
        self.output_dir.trace("w",self.output_dir_info)
        self.output_name = tk.StringVar()
        
        self.bgimg = tk.StringVar()
        if (ns.background_image.is_file() and
            ns.background_image.suffix.lower() == ".png"):
            self.bgimg.set(str(ns.background_image))
        else:
            self.bgimg.set(_SENTINEL_UNSET)

        self.startnote = tk.IntVar()
        self.startnote.trace("w",self.startnote_info)
        self.startnote_info = tk.StringVar()
        self.startnote.set(ns.start_note)
        
        self.status_message = tk.StringVar()

        """Create the widgets"""
        self.toolbar = Toolbar(self)
        self.toolbar.pack(expand=True,fill="x")

        ttk.Separator(self).pack(expand=True,fill="x")

        self.mainframe = tk.Frame(self)
        self.mainframe.pack(expand=True,fill="both")

        self.input_dir_frame = ttk.Labelframe(self.mainframe,
                                              text="Input Folder")
        self.input_dir_frame.pack()
        self.input_dir_label = tk.Label(self.input_dir_frame,
                                        textvariable=self.input_dir)
        self.input_dir_label.pack()
        self.input_dir_info_frame = ttk.Labelframe(self.input_dir_frame,
                                                   text="wav file count")
        self.input_dir_info_frame.pack()
        self.filecount_label = tk.Label(self.input_dir_info_frame,
                                        textvariable=self.input_dir_wavfile_count)
        self.filecount_label.pack()

        ttk.Separator(self.mainframe).pack(expand=True,fill="x")

        self.output_dir_frame = ttk.Labelframe(self.mainframe,
                                               text="Output Folder")
        self.output_dir_frame.pack()
        self.output_dir_label = tk.Label(self.output_dir_frame,
                                         textvariable=self.output_dir)
        self.output_dir_label.pack()
        self.output_dir_info_frame = ttk.Labelframe(self.output_dir_frame,
                                                    text="Output Name")
        self.output_dir_info_frame.pack()
        self.output_name_label = tk.Label(self.output_dir_info_frame,
                                          textvariable=self.output_name)
        self.output_name_label.pack()

        ttk.Separator(self.mainframe).pack(expand=True,fill="x")

        self.bg_img_frame = ttk.Labelframe(self.mainframe,
                                           text="Background Image (812px x 375px)")
        self.bg_img_frame.pack()
        self.bg_img_label = tk.Label(self.bg_img_frame,textvariable=self.bgimg)
        self.bg_img_label.pack()

        ttk.Separator(self.mainframe).pack(expand=True,fill="x")
        self.start_note_frame = ttk.Labelframe(self.mainframe,
                                               text="Starting Note Number")
        self.start_note_frame.pack()
        self.start_note_spinbox = tk.Spinbox(self.start_note_frame,
                                             from_=0,to=127,
                                             textvariable=self.startnote,
                                             wrap=True)
        self.start_note_spinbox.pack()
        self.start_note_info_frame = ttk.Labelframe(self.start_note_frame,
                                                    text="Note Info")
        self.start_note_info_frame.pack()
        self.start_note_label = tk.Label(self.start_note_info_frame,
                                         textvariable=self.startnote)
        self.start_note_label.pack()
        self.start_note_info_label = tk.Label(self.start_note_info_frame,
                                              textvariable=self.startnote_info)
        self.start_note_info_label.pack()

        ttk.Separator(self.mainframe).pack(expand=True,fill="x")

        self.build_button = tk.Button(self.mainframe,text="Build Library",
                                      command=self.toolbar.build_library)
        self.build_button.pack()

        ttk.Separator(self.mainframe).pack(expand=True,fill="x")

        self.statusbar = ttk.Label(self.mainframe,
                                   background="#CCC",
                                  textvariable=self.status_message)
        self.statusbar.pack(expand=True,fill="x")

        """Bind the accelerators"""
        self.bind("<Control-q>",lambda _:self.quit())
        self.bind("<Control-i>",self.toolbar.choose_input_dir)
        self.bind("<Control-o>",self.toolbar.choose_output_dir)
        self.bind("<Control-b>",self.toolbar.choose_bg_image)
        self.bind("<Control-k>",self.toolbar.build_library)

        """Check if ready to build"""
        if self.toolbar.build_library_poll():
            self.status_message.set("Ready to build")

#}}}1

if __name__ == "__main__":
    App().mainloop()

