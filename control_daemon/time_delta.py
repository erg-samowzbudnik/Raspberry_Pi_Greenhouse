#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'config_filez'))
import light
from light import SUNRISE, SUNSET

def until_sunrise(t1=SUNRISE, t2=SUNSET):
        
    t1_H, t1_M = t1.split(':')
    t2_H, t2_M = t2.split(':')

    t1_int = int(t1_H) * 3600 + int(t1_M) * 60
    t2_int = int(t2_H) * 3600 + int(t2_M) * 60

    t3 = ( 86400 - t2_int + t1_int) # time from sunset untill the next sunrise
                                    # in seconds
    return t3
