#!/usr/bin/env /usr/bin/python3

import sys
import os

def is_cmd(line):
    return line[0] == "$"

def parse_cmd(line):
    return line[2:4], line[5:]

def apply_cd(cd, arg):
    return os.path.normpath(os.path.join(cd, arg))

def parse_ls_output(line, cd):
    x, name = line.split(" ")
    path = os.path.join(cd, name)
    if x == "dir":
        return path, True, 0
    else:
        return path, False, int(x)

def directory_and_parents(directory):
    while True:
        yield directory
        if directory == "/":
            break
        directory = os.path.normpath(os.path.join(directory, ".."))
    
# output dict of {dir: size}
def size_dirs(fs):
    dirs = {}
    for path in fs:
        is_dir, size = fs[path]
        if is_dir:
            for d in directory_and_parents(path):
                if not d in dirs:
                    dirs[d] = 0
                else:
                    pass
        else:
            d = os.path.dirname(path)
            for d in directory_and_parents(d):
                if not d in dirs:
                    dirs[d] = size
                else:
                    dirs[d] = dirs[d] + size
    return dirs
        
    
# outputs dict of {path: (type, size)} for files
def parse_input(stdin):
    cd = "/"
    files = {}
    cmd = None
    for line in stdin:
        if is_cmd(line):
            cmd, arg = parse_cmd(line)
            if cmd == "cd":
                cd = apply_cd(cd, arg)
            elif cmd == "ls":
                pass
            else:
                raise f"Unknown command {cmd} {args}"
        else:
            if cmd == None:
                raise "Input started with a non-command"
            elif cmd == "cd":
                raise "Output following cd command"
            else: #ls
                path, is_dir, size = parse_ls_output(line, cd)
                if path in files:
                    pass
                else:
                    files[path] = is_dir, size
    return files

stdin = sys.stdin.read().splitlines()
fs = parse_input(stdin)
dirs = size_dirs(fs)
dirs = filter(lambda x: x <= 100000, dirs.values())
print(sum(dirs))
