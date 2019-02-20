#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os,sys

t = os.listdir('.')
t.sort()
for x in t:
    os.rename(x,x+".txt")
