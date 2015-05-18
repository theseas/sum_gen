#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#
# Author: Theseas Maroulis
# Copyright: Athens 2015 All right reserved
#
# This script generates a checksum file of all files recursively
# using sha512 algorithm.

# Usage:
# $ sum_gen.py [./path/to/folder/]
# if path to folder is ommited then the current working
# directory is assumed

import hashlib, os, sys

# computes the hash for the file.
#
# Opens the the file and computes the sha512
# sum of its contents.
#
# @param dir: dir path of the file (usually relative to the programs cwd)
# @param fname: name of the file we want to compute.
# @return sha512 hash hexdigest of the files contents.
def file_hash(fname):
    buffer_size = 1024
    _hash = hashlib.sha512()
    dig = b''
    try:
        _file = open(fname, 'rb')
        buff = _file.read(buffer_size)
        while(buff!=b''):
            _hash.update(buff)
            del buff # free the memory from the previous buffer
            buff = _file.read(buffer_size)
        _file.close()
        del _file
        dig = _hash.hexdigest()
        del _hash
    except OSError as e:
        sys.stderr.write("Cannot open the {0} for reading".format(os.path.join(dir,fname)))
        dig = b''
    return dig

# walks in the directory tree and computes
# the checksum of all file.
#
# @param root: the top directory we want to traverse
# @return True if traversal was successful or False if it can't create the checksum
# file
def walk(root):
    #abs_root = os.path.abspath(root)
    curr_dir = root
    if not os.path.exists(root):
        sys.stderr.write("This path does not exist or we lack permissions to access it!\n")
        return False
    else:
        os.chdir(root)
    sum_file = None
    try:
        sum_file = open("sum.sha512", "w")
    except OSError as e:
        sys.stderr.write("We cannot create checksum file!\n")
        return False
    dir_list = [curr_dir]
    while(len(dir_list)>0):
        curr_dir = dir_list.pop()
        for f in os.listdir(curr_dir):
            fname = os.path.join(curr_dir, f)
            if os.path.isdir(fname):
                dir_list.append(fname)
                continue
            if os.path.isfile(fname) and fname!=os.path.join(root, 'sum.sha512'):
                sum_file.write("{0}\t{1}\n".format(file_hash(os.path.abspath(fname)), fname))
    sum_file.flush()
    sum_file.close()
    return True


if __name__=='__main__':
    exit_status = 0
    root = '.'
    if len(sys.argv)==2:
        root = sys.argv[1]
    result = walk(root)
    if result==False:
        exit_status = 1
    exit(exit_status)
