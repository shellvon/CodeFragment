#!encoding=utf-8
#! /usr/bin/env python

#为了打包成exe.
#命令行下：python setup.py pyexe
from distutils.core import setup
import py2exe

setup(console=["jwc_gui.py"])