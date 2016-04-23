#!/usr/bin/python

import os
def touch(fname, times=None):
    fhandle = open(fname, 'a')
    try:
        os.utime(fname, times)
    finally:
        fhandle.close()

dir = os.path.dirname(os.path.realpath(__file__))
file = dir + '/wsgi.py'
touch (file)


