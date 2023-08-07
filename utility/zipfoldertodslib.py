import pathlib
import shutil
import argparse
import os
import sys
args = argparse.ArgumentParser()
args.add_argument("--in-folder",type=pathlib.Path)
args.add_argument("--zip-only",action="store_true")
args.add_argument("--rename-only",action="store_true")
ns = args.parse_args()
print(ns)

print("os.getcwd():",os.getcwd())


in_dir = ns.in_folder.resolve()
print("in_dir:",in_dir)
os.chdir(in_dir)
print("os.getcwd():",os.getcwd())
# sys.exit()
if not ns.rename_only:
    dirs = [d for d in in_dir.iterdir() if d.is_dir()]
    L = len(dirs)
    print(L,"folders to zip")
    for n,d in enumerate(dirs):
        print("zipping ",n+1,"of",L,d)
        shutil.make_archive(d.name,"zip",d)
if not ns.zip_only:
    zips = [z for z in in_dir.iterdir() if (z.is_file() and z.suffix == ".zip")]
    L = len(zips)
    for n,z in enumerate(zips):
        newname = z.stem+".dslibrary"
        print("renaming",n+1,"of",L,z.name,"to",newname)
        z.rename(newname)
print("OK")

