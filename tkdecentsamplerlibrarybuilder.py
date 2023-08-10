# version 0.4
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
import pathlib
import shutil
from xml.dom import minidom
import argparse
import itertools

xml_doctype_tag = """<?xml version="1.0" encoding="UTF-8"?>
"""
_DESKTOP_BGFILE = pathlib.Path.home() / "Desktop" / "bg.png"
_SENTINEL_UNSET = ":NOT SET:"
_MSG_NOT_READY = "Not enough info to build!"
_MSG_BUILD_START = "Build starting..."
args = argparse.ArgumentParser()
args.add_argument("--do-build",action="store_true")
args.add_argument("--input-folder",type=pathlib.Path)
args.add_argument("--output-folder",type=pathlib.Path)
args.add_argument("--background-image",type=pathlib.Path,
                  default=_DESKTOP_BGFILE)
args.add_argument("--start-note",type=int,default=21)
args.add_argument("--have-reverb",action="store_true")
args.add_argument("--have-tone",action="store_true")
args.add_argument("--have-chorus",action="store_true")
args.add_argument("--have-midicc1",action="store_true")
args.add_argument("--no-attack",action="store_true")
args.add_argument("--no-decay",action="store_true")
args.add_argument("--no-sustain",action="store_true")
args.add_argument("--no-release",action="store_true")
args.add_argument("--cut-all-by-all",action="store_true")
args.add_argument("--silencing-mode",choices=["normal","fast"],
                  default="normal")
ns = args.parse_args()
print("argument namespace:",ns)
# import sys
# sys.exit()
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
class Toolbar(ttk.Frame):
    @property
    def parent(self):
        return self.master.master
    #{{{2 app_quit
    def app_quit(self):
        print("bye")
        self.quit()
    #}}}2
    #{{{2 choose_input_dir
    def choose_input_dir(self,*event):
        d = filedialog.askdirectory()
        print("d:",d)
        newpath = pathlib.Path(d).resolve()
        print("newpath:",newpath)
        if newpath.is_dir():
            self.parent.input_dir.set(str(newpath))
    #}}}2
    #{{{2 choose_output_dir
    def choose_output_dir(self,*event):
        d = filedialog.askdirectory()
        print("d:",d)
        newpath = pathlib.Path(d).resolve()
        print("newpath:",newpath)
        if newpath.is_dir():
            self.parent.output_dir.set(str(newpath))
    #}}}2
    #{{{2 choose_bg_image
    def choose_bg_image(self,*event):
        d = filedialog.askopenfilename(filetypes=[("PNG",".png")])
        print("d:",d)
        newpath = pathlib.Path(d).resolve()
        print("newpath:",newpath)
        if newpath.is_file():
            self.parent.bgimg.set(str(newpath))
    #}}}2
    #{{{2 build_library
    def build_library(self,*event):
        if not self.build_library_poll():
            self.parent.status_message.set(_MSG_NOT_READY)
            return
        self.parent.status_message.set(_MSG_BUILD_START)
        self.parent.update_idletasks()
        idir = pathlib.Path(self.parent.input_dir.get())
        odir = pathlib.Path(self.parent.output_dir.get())
        bgimg = pathlib.Path(self.parent.bgimg.get())
        notenum = int(self.parent.startnote.get())
        self.parent.output_dir.set(self.parent.output_dir.get())
        oname = self.parent.output_name.get()
        samples = list(idir.glob("*.wav"))
        for s in samples:
            shutil.copy(s,odir)
            print(s,"copied to",odir)
        shutil.copy(bgimg,odir)
        print(bgimg,"copied to",odir)
        presetfilepath = odir / (oname + ".dspreset")
        libraryfilepath = odir.parent / (oname + ".dslibrary")
        have_attack = self.parent.have_attack_knob.get()
        have_decay = self.parent.have_decay_knob.get()
        have_sustain = self.parent.have_sustain_knob.get()
        have_release = self.parent.have_release_knob.get()
        have_tone = self.parent.have_tone_knob.get()
        have_chorus = self.parent.have_chorus_knob.get()
        have_reverb = self.parent.have_reverb_knob.get()
        have_midicc1 = self.parent.have_midicc1.get()
        doc = minidom.Document()
        elem = doc.createElement
        root = elem("DecentSampler")
        root.attrt(("minVersion","1.0.0"))
        ui = elem("ui")
        root += ui
        ui.attrt(("width","812"))
        ui.attrt(("height","375"))
        ui.attrt(("layoutMode","relative"))
        ui.attrt(("bgMode","top_left"))
        ui.attrt(("bgImage",bgimg.name))
        tab = elem("tab")
        ui += tab
        tab.attrt(("name","main"))
        knobcount = itertools.count(0)
        knob_offset = 200
        tone_knob_position = -1
        knob_spacing = 70
        if have_attack:
            attack_knob = elem("labeled-knob")
            tab += attack_knob
            attack_knob_position = next(knobcount)
            x = knob_offset + (attack_knob_position * knob_spacing)
            attack_knob.attrt(("x",str(x)))
            attack_knob.attrt(("y","75"))
            attack_knob.attrt(("textSize","16"))
            attack_knob.attrt(("textColor","AA000000"))
            attack_knob.attrt(("trackForegroundColor","CC000000"))
            attack_knob.attrt(("trackBackgroundColor","66999999"))
            attack_knob.attrt(("label","Attack"))
            attack_knob.attrt(("type","float"))
            attack_knob.attrt(("minValue","0.0"))
            attack_knob.attrt(("maxValue","10.0"))
            attack_knob.attrt(("value","0.01"))
            attack_binding = elem("binding")
            attack_knob += attack_binding
            attack_binding.attrt(("type","amp"))
            attack_binding.attrt(("level","instrument"))
            # attack_binding.attrt(("position",str(attack_knob_position)))
            attack_binding.attrt(("position",0))
            attack_binding.attrt(("parameter","ENV_ATTACK"))
        if have_decay:
            decay_knob = elem("labeled-knob")
            tab += decay_knob
            decay_knob_position = next(knobcount)
            x = knob_offset + (decay_knob_position * knob_spacing)
            decay_knob.attrt(("x",str(x)))
            decay_knob.attrt(("y","75"))
            decay_knob.attrt(("textSize","16"))
            decay_knob.attrt(("textColor","AA000000"))
            decay_knob.attrt(("trackForegroundColor","CC000000"))
            decay_knob.attrt(("trackBackgroundColor","66999999"))
            decay_knob.attrt(("label","Decay"))
            decay_knob.attrt(("type","float"))
            decay_knob.attrt(("minValue","0.0"))
            decay_knob.attrt(("maxValue","25.0"))
            decay_knob.attrt(("value","1.0"))
            decay_binding = elem("binding")
            decay_knob += decay_binding
            decay_binding.attrt(("type","amp"))
            decay_binding.attrt(("level","instrument"))
            # decay_binding.attrt(("position",str(decay_knob_position)))
            decay_binding.attrt(("position",0))
            decay_binding.attrt(("parameter","ENV_DECAY"))
        if have_sustain:
            sustain_knob = elem("labeled-knob")
            tab += sustain_knob
            sustain_knob_position = next(knobcount)
            x = knob_offset + (sustain_knob_position * knob_spacing)
            sustain_knob.attrt(("x",str(x)))
            sustain_knob.attrt(("y","75"))
            sustain_knob.attrt(("textSize","16"))
            sustain_knob.attrt(("textColor","AA000000"))
            sustain_knob.attrt(("trackForegroundColor","CC000000"))
            sustain_knob.attrt(("trackBackgroundColor","66999999"))
            sustain_knob.attrt(("label","Sustain"))
            sustain_knob.attrt(("type","float"))
            sustain_knob.attrt(("minValue","0.0"))
            sustain_knob.attrt(("maxValue","1.0"))
            sustain_knob.attrt(("value","1.0"))
            sustain_binding = elem("binding")
            sustain_knob += sustain_binding
            sustain_binding.attrt(("type","amp"))
            sustain_binding.attrt(("level","instrument"))
            # sustain_binding.attrt(("position",str(sustain_knob_position)))
            sustain_binding.attrt(("position",0))
            sustain_binding.attrt(("parameter","ENV_SUSTAIN"))
        if have_release:
            release_knob = elem("labeled-knob")
            tab += release_knob
            release_knob_position = next(knobcount)
            x = knob_offset + (release_knob_position * knob_spacing)
            release_knob.attrt(("x",str(x)))
            release_knob.attrt(("y","75"))
            release_knob.attrt(("textSize","16"))
            release_knob.attrt(("textColor","AA000000"))
            release_knob.attrt(("trackForegroundColor","CC000000"))
            release_knob.attrt(("trackBackgroundColor","66999999"))
            release_knob.attrt(("label","Release"))
            release_knob.attrt(("type","float"))
            release_knob.attrt(("minValue","0.0"))
            release_knob.attrt(("maxValue","25.0"))
            release_knob.attrt(("value","0.430"))
            release_binding = elem("binding")
            release_knob += release_binding
            release_binding.attrt(("type","amp"))
            release_binding.attrt(("level","instrument"))
            # release_binding.attrt(("position",str(release_knob_position)))
            release_binding.attrt(("position",0))
            release_binding.attrt(("parameter","ENV_RELEASE"))
        fx_position = -1
        if have_chorus:
            fx_position += 1
            chorus_knob = elem("labeled-knob")
            tab += chorus_knob
            chorus_knob_position = next(knobcount)
            x = knob_offset + (chorus_knob_position * knob_spacing)
            chorus_knob.attrt(("x",str(x)))
            chorus_knob.attrt(("y","75"))
            chorus_knob.attrt(("textSize","16"))
            chorus_knob.attrt(("textColor","AA000000"))
            chorus_knob.attrt(("trackForegroundColor","CC000000"))
            chorus_knob.attrt(("trackBackgroundColor","66999999"))
            chorus_knob.attrt(("label","Chorus"))
            chorus_knob.attrt(("type","float"))
            chorus_knob.attrt(("minValue","0.0"))
            chorus_knob.attrt(("maxValue","1.0"))
            chorus_knob.attrt(("value","0.0"))
            chorus_binding = elem("binding")
            chorus_knob += chorus_binding
            chorus_binding.attrt(("type","effect"))
            chorus_binding.attrt(("level","instrument"))
            # chorus_binding.attrt(("position",str(chorus_knob_position)))
            chorus_binding.attrt(("position",fx_position))
            chorus_binding.attrt(("parameter","FX_MIX"))
        if have_tone:
            fx_position += 1
            tone_knob = elem("labeled-knob")
            tab += tone_knob
            tone_knob_position = next(knobcount)
            x = knob_offset + (tone_knob_position * knob_spacing)
            tone_knob.attrt(("x",str(x)))
            tone_knob.attrt(("y","75"))
            tone_knob.attrt(("textSize","16"))
            tone_knob.attrt(("textColor","AA000000"))
            tone_knob.attrt(("trackForegroundColor","CC000000"))
            tone_knob.attrt(("trackBackgroundColor","66999999"))
            tone_knob.attrt(("label","Tone"))
            tone_knob.attrt(("type","float"))
            tone_knob.attrt(("minValue","0"))
            tone_knob.attrt(("maxValue","1"))
            tone_knob.attrt(("value","1"))
            tone_binding = elem("binding")
            tone_knob += tone_binding
            tone_binding.attrt(("type","effect"))
            tone_binding.attrt(("level","instrument"))
            # tone_binding.attrt(("position",str(tone_knob_position)))
            tone_binding.attrt(("position",fx_position))
            tone_binding.attrt(("parameter","FX_FILTER_FREQUENCY"))
            tone_binding.attrt(("translation","table"))
            tone_binding.attrt(("translationTable","0,33;0.3,150;0.4,450;0.5,1100;0.7,4100;0.9,11000;1.0001,22000"))
        if have_reverb:
            fx_position
            reverb_knob = elem("labeled-knob")
            tab += reverb_knob
            reverb_knob_position = next(knobcount)
            x = knob_offset + (reverb_knob_position * knob_spacing)
            reverb_knob.attrt(("x",str(x)))
            reverb_knob.attrt(("y","75"))
            reverb_knob.attrt(("textSize","16"))
            reverb_knob.attrt(("textColor","AA000000"))
            reverb_knob.attrt(("trackForegroundColor","CC000000"))
            reverb_knob.attrt(("trackBackgroundColor","66999999"))
            reverb_knob.attrt(("label","Reverb"))
            reverb_knob.attrt(("type","percent"))
            reverb_knob.attrt(("minValue","0"))
            reverb_knob.attrt(("maxValue","100"))
            reverb_knob.attrt(("value","50"))
            reverb_binding = elem("binding")
            reverb_knob += reverb_binding
            reverb_binding.attrt(("type","effect"))
            reverb_binding.attrt(("level","instrument"))
            reverb_binding.attrt(("position",str(reverb_knob_position)))
            reverb_binding.attrt(("position",fx_position))
            reverb_binding.attrt(("parameter","FX_REVERB_WET_LEVEL"))
            reverb_binding.attrt(("translation","linear"))
            reverb_binding.attrt(("translationOutputMin","0"))
            reverb_binding.attrt(("translationOutputMax","1"))
        groups = elem("groups")
        root += groups
        groups.attrt(("attack","0.000"))
        groups.attrt(("decay","25"))
        groups.attrt(("sustain","1.0"))
        groups.attrt(("release","0.430"))
        groups.attrt(("volume","-3dB"))
        group = elem("group")
        groups += group
        for s in odir.glob("*.wav"):
            sample_elem = elem("sample")
            sample_elem.attrt(("path",s.name))
            sample_elem.attrt(("loNote",str(notenum)))
            sample_elem.attrt(("hiNote",str(notenum)))
            sample_elem.attrt(("rootNote",str(notenum)))
            group += sample_elem
            notenum += 1
        if self.parent.cut_all_by_all.get():
            group.attrt(("tags","cutgroup0"))
            group.attrt(("silencedByTags","cutgroup0"))
            group.attrt(("silencingMode",self.parent.silencing_mode.get()))
        fx = elem("effects")
        root += fx
        if have_chorus:
            chorus_effect = elem("effect")
            fx += chorus_effect
            chorus_effect.attrt(("type","chorus"))
            chorus_effect.attrt(("mix","0.0"))
            chorus_effect.attrt(("modDepth","0.2"))
            chorus_effect.attrt(("modRate","0.2"))
        if have_tone:
            tone_effect = elem("effect")
            fx += tone_effect
            tone_effect.attrt(("type","lowpass"))
            tone_effect.attrt(("frequency","22000.0"))
        if have_reverb:
            reverb_effect = elem("effect")
            fx += reverb_effect
            reverb_effect.attrt(("type","reverb"))
            reverb_effect.attrt(("wetLevel","0.5"))
        if have_midicc1 and tone_knob_position > -1:
            midi = elem("midi")
            root += midi
            tone_midicc_mapping = elem("cc")
            midi += tone_midicc_mapping
            tone_midicc_mapping.attrt(("number","1"))
            tone_midicc_binding = elem("binding")
            tone_midicc_mapping += tone_midicc_binding
            tone_midicc_binding.attrt(("level","ui"))
            tone_midicc_binding.attrt(("type","control"))
            tone_midicc_binding.attrt(("parameter","VALUE"))
            tone_midicc_binding.attrt(("position",str(tone_knob_position)))
            tone_midicc_binding.attrt(("translation","linear"))
            tone_midicc_binding.attrt(("translationOutputMin","0"))
            tone_midicc_binding.attrt(("translationOutputMax","1"))
        rootxml = root.toprettyxml().strip()
        doctxt = xml_doctype_tag + rootxml
        with open(presetfilepath,"w") as presetfile:
            presetfile.write(doctxt)
        print("preset file written in",odir)
        print("zipping",odir,"up...",end="")
        shutil.make_archive(libraryfilepath,"zip",odir)
        print("zipped OK")
        print("zip archive created:",libraryfilepath)
        zippedlibpath = pathlib.Path(str(libraryfilepath) + ".zip")
        zippedlibpath.rename(libraryfilepath)
        print("archive renamed with dslibrary suffix(",zippedlibpath,")")
        print("BUILD COMPLETED")
        print("-"*40)
        self.parent.status_message.set("Built "+libraryfilepath.name)
    #}}}2
    #{{{2 build_library_poll
    def build_library_poll(self):
        idir_t = self.parent.input_dir.get()
        odir_t = self.parent.output_dir.get()
        bgimg_t = self.parent.bgimg.get()
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
    #}}}2
    #{{{2 __init__
    def __init__(self,master):
        super().__init__(master)
        self.menubutton = ttk.Menubutton(self,text="Menu")
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
    #}}}2

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
    #{{{2 __init__
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
        self.have_reverb_knob = tk.IntVar()
        self.have_reverb_knob.set(ns.have_reverb)
        self.have_tone_knob = tk.IntVar()
        self.have_tone_knob.set(ns.have_tone)
        self.have_chorus_knob = tk.IntVar()
        self.have_chorus_knob.set(ns.have_chorus)
        self.have_attack_knob = tk.IntVar()
        self.have_attack_knob.set(not ns.no_attack)
        self.have_decay_knob = tk.IntVar()
        self.have_decay_knob.set(not ns.no_decay)
        self.have_sustain_knob = tk.IntVar()
        self.have_sustain_knob.set(not ns.no_sustain)
        self.have_release_knob = tk.IntVar()
        self.have_release_knob.set(not ns.no_release)
        self.have_midicc1 = tk.IntVar()
        self.have_midicc1.set(ns.have_midicc1)
        self.cut_all_by_all = tk.IntVar()
        self.cut_all_by_all.set(ns.cut_all_by_all)
        self.silencing_mode = tk.StringVar()
        self.silencing_mode.set(ns.silencing_mode)
        self.status_message = tk.StringVar()
        """Create the widgets"""
        self.outerframe = ttk.Frame(self)
        self.outerframe.pack(expand=True,fill="both")
        self.toolbar = Toolbar(self.outerframe)
        self.toolbar.pack(expand=True,fill="x")
        ttk.Separator(self.outerframe).pack(expand=True,fill="x")
        self.mainframe = ttk.Frame(self.outerframe)
        self.mainframe.pack(expand=True,fill="both")
        self.input_dir_frame = ttk.Labelframe(self.mainframe,
                                              text="Input Folder")
        self.input_dir_frame.pack(expand=True,fill="x")
        self.input_dir_btn = ttk.Button(self.input_dir_frame,
                                        textvariable=self.input_dir,
                                        command=self.toolbar.choose_input_dir)
        self.input_dir_btn.pack()
        self.input_dir_info_frame = ttk.Labelframe(self.input_dir_frame,
                                                   text="wav file count")
        self.input_dir_info_frame.pack(expand=True,fill="x")
        self.filecount_label = ttk.Label(self.input_dir_info_frame,
                                        textvariable=self.input_dir_wavfile_count)
        self.filecount_label.pack()
        ttk.Separator(self.mainframe).pack(expand=True,fill="x")
        self.output_dir_frame = ttk.Labelframe(self.mainframe,
                                               text="Output Folder")
        self.output_dir_frame.pack(expand=True,fill="x")
        self.output_dir_btn = ttk.Button(self.output_dir_frame,
                                         textvariable=self.output_dir,
                                         command=self.toolbar.choose_output_dir)
        self.output_dir_btn.pack()
        self.output_dir_info_frame = ttk.Labelframe(self.output_dir_frame,
                                                    text="Output Name")
        self.output_dir_info_frame.pack(expand=True,fill="x")
        self.output_name_label = ttk.Label(self.output_dir_info_frame,
                                          textvariable=self.output_name)
        self.output_name_label.pack()
        ttk.Separator(self.mainframe).pack(expand=True,fill="x")
        self.bg_img_frame = ttk.Labelframe(self.mainframe,
                                           text="Background Image (812px x 375px)")
        self.bg_img_frame.pack(expand=True,fill="x")
        self.bg_img_btn = ttk.Button(self.bg_img_frame,
                                     textvariable=self.bgimg,
                                     command=self.toolbar.choose_bg_image)
        self.bg_img_btn.pack()
        ttk.Separator(self.mainframe).pack(expand=True,fill="x")
        self.start_note_frame = ttk.Labelframe(self.mainframe,
                                               text="Starting Note Number")
        self.start_note_frame.pack(expand=True,fill="x")
        self.start_note_spinbox = ttk.Spinbox(self.start_note_frame,
                                             from_=0,to=127,
                                             textvariable=self.startnote,
                                             wrap=True)
        self.start_note_spinbox.pack()
        self.start_note_info_frame = ttk.Labelframe(self.start_note_frame,
                                                    text="Note Info")
        self.start_note_info_frame.pack(expand=True,fill="x")
        self.start_note_label = ttk.Label(self.start_note_info_frame,
                                         textvariable=self.startnote)
        self.start_note_label.pack()
        self.start_note_info_label = ttk.Label(self.start_note_info_frame,
                                              textvariable=self.startnote_info)
        self.start_note_info_label.pack()
        ttk.Separator(self.mainframe).pack(expand=True,fill="x")
        self.knobs_frame = ttk.Labelframe(self.mainframe,text="Knobs")
        self.knobs_frame.pack(expand=True,fill="x")
        self.attack_chk = ttk.Checkbutton(self.knobs_frame,
                                          text="Attack",
                                          variable=self.have_attack_knob)
        self.attack_chk.pack(anchor="w")
        self.decay_chk = ttk.Checkbutton(self.knobs_frame,
                                          text="Decay",
                                          variable=self.have_decay_knob)
        self.decay_chk.pack(anchor="w")
        self.sustain_chk = ttk.Checkbutton(self.knobs_frame,
                                          text="Sustain",
                                          variable=self.have_sustain_knob)
        self.sustain_chk.pack(anchor="w")
        self.release_chk = ttk.Checkbutton(self.knobs_frame,
                                          text="Release",
                                          variable=self.have_release_knob)
        self.release_chk.pack(anchor="w")
        ttk.Separator(self.knobs_frame).pack(expand=True,fill="x")
        self.chorus_chk = ttk.Checkbutton(self.knobs_frame,
                                          text="Chorus",
                                          variable=self.have_chorus_knob)
        self.chorus_chk.pack(anchor="w")
        self.tone_chk = ttk.Checkbutton(self.knobs_frame,
                                          text="Tone",
                                          variable=self.have_tone_knob)
        self.tone_chk.pack(anchor="w")
        self.reverb_chk = ttk.Checkbutton(self.knobs_frame,
                                          text="Reverb",
                                          variable=self.have_reverb_knob)
        self.reverb_chk.pack(anchor="w")
        ttk.Separator(self.mainframe).pack(expand=True,fill="x")
        self.cutgroups_frame = ttk.Labelframe(self.mainframe,
                                             text="Cut Groups")
        self.cutgroups_frame.pack(expand=True,fill="x")
        self.cut_all_by_all_chk = ttk.Checkbutton(self.cutgroups_frame,
                                                  text="Cut all by all",
                                                  variable=self.cut_all_by_all)
        self.cut_all_by_all_chk.pack()
        self.silencing_mode_radio_normal = ttk.Radiobutton(
            self.cutgroups_frame,
            text="Normal",value="normal",
            variable=self.silencing_mode)
        self.silencing_mode_radio_normal.pack(side="left")
        self.silencing_mode_radio_fast = ttk.Radiobutton(
            self.cutgroups_frame,
            text="Fast",value="fast",
            variable=self.silencing_mode)
        self.silencing_mode_radio_fast.pack(side="right")
        ttk.Separator(self.mainframe).pack(expand=True,fill="x")
        self.midi_frame = ttk.Labelframe(self.mainframe,text="MIDI")
        self.midi_frame.pack(expand=True,fill="x")
        self.midicc1_chk = ttk.Checkbutton(self.midi_frame,
                                           text="Map tone knob to CC1",
                                           variable=self.have_midicc1)
        self.midicc1_chk.pack()
        ttk.Separator(self.mainframe).pack(expand=True,fill="x")
        self.build_button = ttk.Button(self.mainframe,text="Build Library",
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
        can_build = self.toolbar.build_library_poll()
        if can_build:
            self.status_message.set("Ready to build")
        if ns.do_build:
            if can_build:
                self.update_idletasks()
                self.toolbar.build_library()
                import sys
                sys.exit()
            else:
                print("--do-build flag supplied with incomplete info. Exiting.")
                import sys
                sys.exit()
    #}}}2
#}}}1

if __name__ == "__main__":
    app = App()
    app.tk.call("source", "azure.tcl")
    # app.tk.call("set_theme", "light")
    app.tk.call("set_theme", "dark")
    app.mainloop()
