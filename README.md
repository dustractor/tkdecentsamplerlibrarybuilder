# tkdecentsamplerlibrarybuilder
a tkinter utility for making a folder full of samples and a background image into a decent sampler (the vst) library

get Decent Sampler here: https://www.decentsamples.com/product/decent-sampler-plugin/


tl;dr here's a video: https://youtu.be/n9n_xIFs5Os

---

# usage

you make a folder and put some wav file samples in it

then you make an empty folder and give it a name

then you make a background image png that is 812x375

then you run this program

use the menu to choose your input folder the one with the samples in it

use the menu to choose your output folder the empty one you gave it a name

use the menu to choose your background png (hint: if you just save it on your desktop as bg.png it will be automatically selected)

use the up down arrows for the start note to choose where on the keyboard the samples will get laid out from. the default is 21 because that's the lowest note on an 88-key keyboard but you can set it to 0 if you intend to use this thing mainly from a piano roll

then use the menu to build the library

the library will be sitting next to the output folder and you copy that whatever.dslibrary file to the place where Decent Sampler keeps it's presets

on my machine that folder is C:\Users\user\AppData\Roaming\Decidedly\DecentSampler\Sample Libraries

that's it good luck have fun

### command-line options:

    optional arguments:
      -h, --help            show this help message and exit
      --do-build
      --input-folder INPUT_FOLDER
      --output-folder OUTPUT_FOLDER
      --background-image BACKGROUND_IMAGE
      --start-note START_NOTE
      --have-reverb
      --have-tone
      --have-chorus
      --have-midicc1
      --no-attack
      --no-decay
      --cut-all-by-all
      --silencing-mode {normal,fast}
      --theme {cosmo,flatly,litera,minty,lumen,sandstone,yeti,pulse,united,morph,journal,darkly,superhero,solar,cyborg,vapor,simplex,cerculean}


# tips

windows users: right-click builder.vbs -> send to desktop (create shortcut) is the thing you want to do if you want something double-clickable.

you can use audacity to make a macro to convert non-wav files into wavs https://www.audacityteam.org

windows powertoys PowerRename might be helpful https://learn.microsoft.com/en-us/windows/powertoys/

https://www.mp3tag.de/en/index.html is useful to remove the metadata


if this is useful to you my cashapp handle is $shamskitz throw me a couple bucks so I can keep making useful stuff

---

## change log

added command-line arguments.  Run with ``--help`` flag to see them.

~~there is also 'fancy' branch which uses ttkbootstrap to make the ui look a bit more modern.  will merge that into this branch once I'm sure it runs ok with or without ttkbootstrap.~~ branch merged

---

## road map

make it pip installable

support for multiple groups

NOT planning to tackle legato

more options for what controls to show / what midi mappings to assign

colors

a better tutorial

