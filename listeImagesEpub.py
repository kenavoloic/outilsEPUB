#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
trame ='''<item href="images/%s" id="%s" media-type="image/jpeg" />'''
newline="\n"
t = os.listdir('.')
t.sort()
fichier = open('listeImages.txt','w')
for x in t:
    texte = trame %(x,x[:-4])
    fichier.write(texte)
    fichier.write(newline)
fichier.close()

                    

