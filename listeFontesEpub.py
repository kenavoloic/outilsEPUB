#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

newline="\n"

css='''@font-face {
font-family: serif;
font-style: normal;
font-weight: normal;
src:url(../fontes/%s);
}
'''
ttfotf=['application/x-font-ttf','application/opentype']

trame='''<item href="fontes/%s" id="fonte%02i" media-type="%s"/>'''

t = os.listdir('.')
t.sort()
index = 1
fichier = open('listeFontes.txt','w')
for x in t:
    if x[-4:] == '.otf':
        texte = trame % (x,index,ttfotf[1])
        fichier.write(texte)
        fichier.write(newline)
        index +=1
    else:
        texte = trame %(x,index,ttfotf[0])
        fichier.write(texte)
        fichier.write(newline)
        index +=1
fichier.close()

fichier2 = open('fontesCss.txt','w')
for x in t:
    texte = css % (x)
    fichier2.write(texte)
    fichier2.write(newline)

fichier.close()

