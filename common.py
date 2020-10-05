import configparser
import sys
import os
curpath=os.path.dirname(os.path.realpath(__file__))
cfgpath=os.path.join(curpath,"main.ini")
conf=configparser.RawConfigParser()
conf.read(cfgpath,encoding="utf-8")