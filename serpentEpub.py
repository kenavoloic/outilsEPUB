#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import fnmatch 
"""
06 01 2012
mod 9.01.2012
ce script gère la création de content.opf et toc.ncx.
Pour qu'il fonctionne,c-à-d, pour ne pas avoir à tout réécrire à la main,
voici la structure du dossier OEBPS
OEBPS/css
OEBPS/images
OEBPS/textes --> c'est dans ce dossier que se trouvent tous les fichiers xhtml.
OEBPS/fontes
Après la création des deux fichiers, il faut les mettre à la racine,c-à-d dans OEBPS avec
couverture.xhtml
page_de_titre.xhtml

"""
trame1 = "<navPoint class=\"other\" id=\"%s\" playOrder=\"%i\">\n<navLabel>\n<text>%s</text>\n</navLabel>\n<content src=\"textes/%s\"/>\n</navPoint>"

trame2 = "<item id=\"%s\" href=\"textes/%s\" media-type=\"application/xhtml+xml\" />"

trame3 = "<itemref idref=\"%s\" linear=\"yes\" />"

enteteopf ='''<?xml version="1.0" encoding="UTF-8"?>
<package version="2.0" xmlns="http://www.idpf.org/2007/opf" unique-identifier="BookId">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
    <dc:title></dc:title>
    <dc:language>en</dc:language>
    <dc:identifier id="BookId">urn:uuid:inpennylane-123456</dc:identifier>
    <dc:creator opf:role="aut"></dc:creator>
    <dc:date opf:event="original-publication"></dc:date>
    <dc:date opf:event="ops-publication"></dc:date>
    <dc:publisher>Jéroboam N.</dc:publisher>
    <dc:subject>Fiction</dc:subject>
    <dc:source>http://localhost</dc:source>
  </metadata>
  <manifest>
    <item id="style" href="css/cca.css" media-type="text/css" />
    <item id="cover-image" href="images/cover.jpg" media-type="image/jpeg"/>
    <item id="cover" href="couverture.xhtml" media-type="application/xhtml+xml" />
    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml" />
    <item id="cred" href="credits.xhtml" media-type="application/xhtml+xml" />
    <item id="title_page" href="page_de_titre.xhtml" media-type="application/xhtml+xml" />
    <item id="copy" href="copy.xhtml" media-type="application/xhtml+xml" />
    <item href="fontes/LinLibertine_RBI.ttf" id="fonte1" media-type="application/x-font-ttf"/>
    <item href="fontes/LinLibertine_RB.ttf" id="fonte2" media-type="application/x-font-ttf"/>
    <item href="fontes/LinLibertine_RI.ttf" id="fonte3" media-type="application/x-font-ttf"/>
    <item href="fontes/LinLibertine_R.ttf" id="fonte4" media-type="application/x-font-ttf"/>
    '''

debutspine = '''  <spine toc="ncx">
      <itemref idref="cover" linear="yes" />
      <itemref idref="title_page" linear="yes" />
      '''

finspine = '''
<itemref idref="copy" linear="yes" />
<itemref idref="cred" linear="yes" />
</spine>
  <guide>
    <reference href="page_de_titre.xhtml" type="cover" title="Cover"/>
  </guide>
</package>'''

debutncx = '''<?xml version="1.0"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
<head>
<meta name="dtb:uid" content="inpennylane-123456" />
<meta name="dtb:depth" content="2" />
<meta name="dtb:totalPageCount" content="0" />
<meta name="dtb:maxPageNumber" content="0" />
</head>
<docTitle>
<text>*******</text>
</docTitle>
<docAuthor>
<text>*********</text>
</docAuthor>
<navMap>
<navPoint class="cover" id="cover" playOrder="1">
<navLabel><text>Couverture</text></navLabel>
<content src="couverture.xhtml" />
</navPoint>
<!-- page de titre -->
<navPoint class="titlepage" id="title_page" playOrder="2">
<navLabel><text>Title</text></navLabel>
<content src="page_de_titre.xhtml" />
'''

finncx = '''</navPoint>

<navPoint class="other" id="copy" playOrder="*">
<navLabel>
<text>Copyright</text>
</navLabel>
<content src="copy.xhtml"/>
</navPoint>

<navPoint class="other" id="cred" playOrder="*">
<navLabel>
<text>Credits</text>
</navLabel>
<content src="credits.xhtml"/>
</navPoint>
</navMap>
</ncx>'''

newline = "\n"


def traitement():
    a1 = os.listdir('.')
    a0 = [x for x in a1 if fnmatch.fnmatch(x,"*.xhtml")]
    fichiers = a0[:]
    fichiers.sort()
    chemins = ['textes/'+x for x in fichiers]
    cheminsopf  = fichiers
    id_fichiers = [x[0:5] for x in fichiers]
    entetes = getEntetes(id_fichiers)
    creationOpf(id_fichiers,cheminsopf)
    creationNcx(id_fichiers,entetes,chemins)


def creationNcx(numid,intitule,source):
    trame = "<navPoint class=\"other\" id=\"%s\" playOrder=\"%i\">\n<navLabel>\n<text>%s</text>\n</navLabel>\n<content src=\"%s\"/>\n</navPoint>"
    fichier = open('toc.ncx','w')
    fichier.write(debutncx)
    fichier.write(newline)
    for x in range(len(numid)):
        texte = trame % (numid[x],x+3,intitule[x],source[x])
        fichier.write(texte)
        fichier.write(newline)
    fichier.write(finncx)
    fichier.write(newline)
    fichier.close() 


def creationOpf(identites,source):
    fichier = open('content.opf','w')
    fichier.write(enteteopf)
    fichier.write(newline)
    for x in range(len(identites)):
        texte = trame2 % (identites[x],source[x])
        fichier.write(texte)
        fichier.write(newline)
    fichier.write("</manifest>")
    fichier.write(newline)

    fichier.write(debutspine)

    for x in range(len(identites)):
        texte = trame3 % (identites[x])
        fichier.write(texte)
        fichier.write(newline)
    fichier.write(finspine)
    fichier.close()


def getEntetes(envoi):
    centaine = [int(float(x[-3:])) for x in envoi]
    dizaine = [int(float(x[-2:])) for x in envoi]
    retour = []
    for x in range(len(envoi)):
        if dizaine[x] == 0:
            numero = centaine[x]/100
            nom = "Book "+str(numero)+"\n"
            retour.append(nom)
        else:
            nom = "Ch. " + str(dizaine[x]) + "\n"
            retour.append(nom)
    return retour
    
    

def ecriture_fichier(nom): 
    for x in range(len(fichiers)): print trame1 %(fichiers[x][0:5],x+3,section[x],fichiers[x]);
    for x in range(len(a0)): print trame2 % (a[x][0:5],a[x])
    for x in range(len(a0)): print trame3 % (a[x][0:5]);


if __name__ == '__main__':
    #u = sys.argv
    traitement()
