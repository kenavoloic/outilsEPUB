#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import fnmatch
"""
06 01 2012
mod 9.01.2012
mod 28.01.2012
mod 22.06.2012
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
format des entetes des fichiers du dossier textes:
bk0X000Y
où X = Livre
où Y = Chapitre
Todo: prise en compte de fichiers tels que Notes.xhtml
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
  </metadata>
  <manifest>
    <item id="style" href="css/cca.css" media-type="text/css" />
    <item id="cover-image" href="images/cover.png" media-type="image/png"/>
    <item id="tdm" href="tdm.xhtml" media-type="application/xhtml+xml" />
    <item id="cover" href="couverture.xhtml" media-type="application/xhtml+xml" />
    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml" />
    <item id="title_page" href="page_de_titre.xhtml" media-type="application/xhtml+xml" />
    <item id="titrepage" href="images/titre.png" media-type="image/png"/>
    <item id="logo" href="images/logo.png" media-type="image/png"/>
    <item id="cred" href="credits.xhtml" media-type="application/xhtml+xml" />
    <item id="copy" href="copyright.xhtml" media-type="application/xhtml+xml" />
    '''

debutspine = '''  <spine toc="ncx">
      <itemref idref="cover" linear="yes" />
      <itemref idref="title_page" linear="yes" />
      <itemref idref="tdm" linear="yes" />
      '''

finspine = '''<itemref idref="copy" linear="yes" />
<itemref idref="cred" linear="yes" />
</spine>
  <guide>
    <reference href="couverture.xhtml" type="cover" title="Cover"/>
    <reference href="tdm.xhtml" type="toc" title="Contents"/>
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
<navLabel><text>Cover</text></navLabel>
<content src="couverture.xhtml" />
</navPoint>

<navPoint class="titlepage" id="title_page" playOrder="2">
<navLabel><text>Title Page</text></navLabel>
<content src="page_de_titre.xhtml" />

<navPoint class="other" id="tdm" playOrder="3">
<navLabel>
<text>Contents</text>
</navLabel>
<content src="tdm.xhtml"/>
</navPoint>
'''

finncx = '''</navPoint>

<navPoint class="other" id="copy" playOrder="%i">
<navLabel>
<text>Copyright</text>
</navLabel>
<content src="copyright.xhtml"/>
</navPoint>

<navPoint class="other" id="cred" playOrder="%i">
<navLabel>
<text>Credits</text>
</navLabel>
<content src="credits.xhtml"/>
</navPoint>

</navMap>
</ncx>'''

newline = "\n"

xhtml_header='''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
   "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml"  xml:lang="en">
<head>
<title> </title>
<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
<link rel="stylesheet" href="css/cca.css" type="text/css" />
</head>
<body>
'''

xhtml_footer='''
</body>
</html>
'''

tdm_top='''<p class="matieres"><a href="couverture.xhtml">Cover</a></p>
<p class="matieres"><a href="tdm.xhtml">Contents</a></p>'''

tdm_bottom='''<p class="matieres"><a href="copyright.xhtml">Copyright</a></p>
<p class="matieres"><a href="credits.xhtml">Credits</a></p>'''

credits='''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
   "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml"  xml:lang="en">
<head>
<title>Credits</title>
<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
<style type="text/css">
body{
margin-left:13px;
margin-right:13px;
margin-top:1em;
}

p {
text-indent:0;
text-align:center;
font-family:serif,sans-serif;
font-size:1.25em;
line-height:1.74em;
margin-top:1em;
margin-bottom:1em;
}
.image{text-indent:0;text-align:center;}
</style>
</head>
<body>

<p>Ouvrage réalisé par</p>
<p class="image"><img src="images/logo.png" class="ego" alt="logotype" /></p>
<p><a href="mailto:jeroboam.n@gmail.com">jeroboam.n@gmail.com</a></p>
</body>
</html>
'''

xhtml_credits = '''<p class="credits">Designed by <a href="mailto:jeroboam.n@gmail.com">jeroboam.n@gmail.com</a></p>'''

xhtml_copyright = '''<p class="credits">Copyright © 2012 by </p>'''

couv='''<html xmlns="http://www.w3.org/1999/xhtml" xmlns:ops="http://www.idpf.org/2007/ops" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<head>
<title></title>
<style type="text/css">
</style>
<meta content="application/xhtml+xml; charset=utf-8" http-equiv="Content-Type"/>
</head>
<body style="margin-top: 0px; margin-left: 0px; margin-right: 0px; margin-bottom: 0px; text-align: center;">
<div class="cover">
<img alt="-*-*-" src="images/cover.png" height="100%"/>
</div>
</body>
</html>
'''

page_titre='''<html xmlns="http://www.w3.org/1999/xhtml" xmlns:ops="http://www.idpf.org/2007/ops" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<head>
<title></title>

<style type="text/css">
</style>
<meta content="application/xhtml+xml; charset=utf-8" http-equiv="Content-Type"/>
</head>
<body style="margin-top: 0px; margin-left: 0px; margin-right: 0px; margin-bottom: 0px; text-align: center;">
<div class="cover">
<img alt="-*-*-" src="images/titre.png" height="100%"/>
</div>
</body>
</html>
'''

def traitement():
    a1 = os.listdir('.')
    a0 = [x for x in a1 if fnmatch.fnmatch(x,"*.xhtml")]
    b0 = a0[:]
    b0.sort()
    #Manipulations pour avoir toujours:
    #D'abord les fichiers commençant par b: bj0001, bk01000, bk01001
    #Puis les autres
    b1 = [x for x in b0 if x.startswith('b')]
    b2 = [x for x in b0 if not x.startswith('b')]

    for x in b2:
        b1.append(x)

    fichiers = b1[:]

    # fichiers = a0[:]
    # fichiers.sort()

    chemins = ['textes/'+x for x in fichiers]
    cheminsopf  = fichiers
    id_fichiers = [x[:-6] for x in fichiers]
    entetes = getEntetes(id_fichiers)
    # heads = getHeads(id_fichiers)
    # for x in heads: print x;
    creationOpf(id_fichiers,cheminsopf)
    creationNcx(id_fichiers,entetes,chemins)
    # creationTdmPartielle(id_fichiers,chemins)
    getTdm(id_fichiers,chemins)
    creationCredits()
    creationCopyright()
    creationCouvTitre()

def creationCouvTitre():
    couverture = open('couverture.xhtml','w')
    couverture.write(couv)
    couverture.write(newline)
    couverture.close()

    pagetitre = open('page_de_titre.xhtml','w')
    pagetitre.write(page_titre)
    pagetitre.write(newline)
    pagetitre.close()

def creationCredits():
    fichier = open('credits.xhtml','w')
    fichier.write(credits)
    fichier.write(newline)
    fichier.close()

def creationCopyright():
    fichier = open('copyright.xhtml','w')
    fichier.write(xhtml_header)
    fichier.write(newline)
    fichier.write(xhtml_copyright)
    fichier.write(newline)
    fichier.write(xhtml_footer)
    fichier.close()

def getTdm(envoiId,chemins):
    indexC = 0
    indexB = 0
    patronC='''<p class="matieres">Chapter <a href="%s" id="%s">%d</a></p>'''
    patronB='''<p class="matieres"><a href="%s" id="%s"></a>Book %d</p>'''
    patronMisc='''<p class="matieres"><a href="%s" id="%s">%s</a></p>'''
    misc = []
    retour = []
    retour.append(xhtml_header)
    retour.append(newline)
    retour.append('<h1 class\"matieres\">Contents</h1>')
    retour.append(newline)

    for x in range(len(envoiId)):
        tx = envoiId[x][-3:]
        if (tx.isdigit()):
            if (int(float(envoiId[x][-3:])) == 0):
                indexB += 1
                retour.append('<p class="vide"> </p>')
                retour.append(newline)
                texte = patronB%(chemins[x],envoiId[x],indexB)
                retour.append(texte)
                retour.append(newline)
                indexC = 0
            else:
                indexC += 1
                texte = patronC%(chemins[x],envoiId[x],indexC)
                retour.append(texte)
                retour.append(newline)
        else:
            texte = patronMisc%(chemins[x],envoiId[x].lower(),envoiId[x])
            misc.append(texte)
            misc.append(newline)

    for x in misc:
        retour.append('<p class="vide"> </p>')
        retour.append(newline)
        retour.append(x)
        retour.append(newline)

    fichier = open('tdm.xhtml','w')
    for x in range(len(retour)):
        fichier.write(retour[x])
    fichier.write(xhtml_footer)
    fichier.close()


def creationTdmPartielle(envoiId,chemins):
    indexC = 0
    indexB = 0
    patronC='''<p class="matieres">Chapter <a href="%s" id="%s">%d</a></p>'''
    patronB='''<p class="matieres"><a href="%s" id="%s"></a>Book %d</p>'''
    patronMisc='''<p class="matieres"><a href="%s" id="%s">%s</a></p>'''
    fichier = open('tdm.xhtml','w')
    fichier.write(xhtml_header)
    fichier.write(newline)
    fichier.write('<h1 class\"matieres\">Contents</h1>')
    fichier.write(newline)
    # for x in range(len(envoiId)):
    #     val = int(float(envoiId[x][-3:]))
    #     if val == 0:
    #         indexB += 1
    #         fichier.write('<p class="vide"> </p>')
    #         fichier.write(newline)
    #         texte = patronB%(chemins[x],envoiId[x],indexB)
    #         fichier.write(texte)
    #         fichier.write(newline)
    #         indexC = 0
    #     else:
    #         indexC += 1
    #         texte = patronC%(chemins[x],envoiId[x],indexC)
    #         fichier.write(texte)
    #         fichier.write(newline)
    # fichier.write(xhtml_footer)
    # fichier.close()

    for x in range(len(envoiId)):
        tx = envoiId[x][-3:]
        if (tx.isdigit()):
            if int(float(envoiId[x][-3:])) == 0:
                indexB += 1
                fichier.write('<p class="vide"> </p>')
                fichier.write(newline)
                texte = patronB%(chemins[x],envoiId[x],indexB)
                fichier.write(texte)
                fichier.write(newline)
                indexC = 0
            else:
                indexC += 1
                texte = patronC%(chemins[x],envoiId[x],indexC)
                fichier.write(texte)
                fichier.write(newline)
        else:
            texte = patronMisc%(chemins[x],envoiId[x],envoiId[x])
            fichier.write(texte)
            fichier.write(newline)

        fichier.write(xhtml_footer)
        fichier.close()



def creationNcx(numid,intitule,source):
    trame = "<navPoint class=\"other\" id=\"%s\" playOrder=\"%i\">\n<navLabel>\n<text>%s</text>\n</navLabel>\n<content src=\"%s\"/>\n</navPoint>\n"
    fichier = open('toc.ncx','w')
    fichier.write(debutncx)
    fichier.write(newline)
    for x in range(len(numid)):
        texte = trame % (numid[x].lower(),x+4,intitule[x],source[x])
        fichier.write(texte)
        fichier.write(newline)
    nb = len(numid)
    fin = finncx % (nb+4,nb+5)
    fichier.write(fin)
    fichier.write(newline)
    fichier.close()

def creationOpf(identites,source):
    fichier = open('content.opf','w')
    fichier.write(enteteopf)
    fichier.write(newline)
    for x in range(len(identites)):
        texte = trame2 % (identites[x].lower(),source[x])
        fichier.write(texte)
        fichier.write(newline)
    fichier.write("</manifest>")
    fichier.write(newline)

    fichier.write(debutspine)

    for x in range(len(identites)):
        texte = trame3 % (identites[x].lower())
        fichier.write(texte)
        fichier.write(newline)
    fichier.write(finspine)
    fichier.close()

def _getEntetes(envoi):
    retour = []
    index = 0
    for x in range(len(envoi)):
        val = int(float(envoi[x][-3:]))
        if val == 0 :
            index += 1
            nom = "Book " + str(index) + "\n"
            retour.append(nom)
        else:
            nom = "Chapitre " +str(val) + "\n"
            retour.append(nom)
    return retour

def getEntetes(envoi):
    retour = []
    index = 0
    for x in range(len(envoi)):
        tx = envoi[x][-3:]
        if (tx.isdigit()):
            if int(float(tx)) == 0:
                index += 1
                nom = "Book " + str(index) + "\n"
                retour.append(nom)
            else:
                nom = "Chapitre " + str(int(float(tx))) + "\n"
                retour.append(nom)
        else:
            nom = tx.lower() + "\n"
            retour.append(nom)
    return retour

def getHeads(envoi):
    retour = []
    index = 0
    for x in range(len(envoi)):
        tx = envoi[x][-3:]
        if (tx.isdigit()):
            # narval == int(float(tx))
            if int(float(tx)) == 0:
                index += 1
                nom = "Book " + str(index) + "\n"
                retour.append(nom)
            else:
                nom = "Chapitre " + str(int(float(tx))) + "\n"
                retour.append(nom)
        else:
            nom = tx + "\n"
            retour.append(nom)
    return retour



def ecriture_fichier(nom):
    for x in range(len(fichiers)): print trame1 %(fichiers[x][0:5],x+3,section[x],fichiers[x]);
    for x in range(len(a0)): print trame2 % (a[x][0:5],a[x])
    for x in range(len(a0)): print trame3 % (a[x][0:5]);


if __name__ == '__main__':
    #u = sys.argv
    traitement()
