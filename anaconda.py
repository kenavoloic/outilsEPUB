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
mod 25.09.2012
mod 20.11.2012
mod 04.02.2013
mod 13.02.2013
mod 21.11.2013
mod 20.03.2014
mod 04.02.2015
mod 05.02.2016

ce script gère la création de content.opf et toc.ncx.
Pour qu'il fonctionne,c-à-d, pour ne pas avoir à tout réécrire à la main,
voici la structure du dossier OEBPS
OEBPS/css
OEBPS/images
OEBPS/textes --> c'est dans ce dossier que se trouvent tous les fichiers xhtml.
OEBPS/fontes
Après la création des deux fichiers, il faut les mettre à la racine,c-à-d dans OEBPS avec
couverture.xhtml
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
    <dc:language>fr</dc:language>
    <dc:identifier id="BookId" opf:scheme="ISBN">978-2-36938-</dc:identifier>
    <dc:creator opf:role="aut"></dc:creator>
    <dc:rights>©</dc:rights>
    <dc:source></dc:source>
    <dc:date opf:event="original-publication"></dc:date>
    <dc:date opf:event="ops-publication"></dc:date>
    <dc:publisher>Jéroboam N. (jeroboam.n@gmail.com)</dc:publisher>
    <dc:subject></dc:subject>
  </metadata>
  <manifest>
    <item id="style" href="css/cca.css" media-type="text/css" />
    <item id="cover-image" href="images/cover.svg" media-type="image/svg+xml"/>
    <item id="cover" href="couverture.xhtml" media-type="application/xhtml+xml" />
    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml" />
    <item id="logo" href="images/logo.png" media-type="image/png"/>
    <item id="cred" href="credits.xhtml" media-type="application/xhtml+xml" />
    <item id="copy" href="copyright.xhtml" media-type="application/xhtml+xml" />
    <item id="titre" href="titre.xhtml" media-type="application/xhtml+xml" />
    <item id="tdm" href="tdm.xhtml" media-type="application/xhtml+xml" />
    '''

debutspine = '''  <spine toc="ncx">
      <itemref idref="cover" linear="yes" />
      <itemref idref="titre" linear="yes" />
      <itemref idref="tdm" linear="yes" />
      '''

finspine = '''<itemref idref="copy" linear="yes" />
<itemref idref="cred" linear="yes" />
</spine>
  <guide>
    <reference href="couverture.xhtml" type="cover" title="Cover"/>
  </guide>
</package>'''

debutncx = '''<?xml version="1.0"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
<head>
<meta name="dtb:uid" content="978-2-36938-" />
<meta name="dtb:depth" content="2" />
<meta name="dtb:totalPageCount" content="0" />
<meta name="dtb:maxPageNumber" content="0" />
</head>

<docTitle>
<text></text>
</docTitle>

<docAuthor>
<text></text>
</docAuthor>

<navMap>
<navPoint class="cover" id="cover" playOrder="1">
<navLabel><text>Couverture</text></navLabel>
<content src="couverture.xhtml" />
</navPoint>

<navPoint class="titlepage" id="titre" playOrder="2">
<navLabel><text>Page de titre</text></navLabel>
<content src="titre.xhtml" />
</navPoint>


<navPoint class="toc" id="tdm" playOrder="3">
<navLabel><text>Sommaire</text></navLabel>
<content src="tdm.xhtml" />
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
<text>Crédits</text>
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


credits='''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
   "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml"  xml:lang="en">
<head>
<title>Credits</title>
<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
<link rel="stylesheet" href="css/cca.css" type="text/css" />
<style type="text/css">

body{
margin-left:20pt;
margin-right:20pt;
margin-top:1em;
}

p {
text-indent:0;
text-align:center;
font-family:serif,sans-serif;
margin:1em 0 1em 0;
}

.isbn {
font-weight:bold;
}


.logo {
margin:1em 0 1em 0;
text-align:center;
}

.bordeaux {
font-style:italic;
text-align:right;
}

.url {
font-family:sans-serif,serif;
}

.courriel {
font-family:sans-serif,serif;
}

.erratum {
font-style:italic;
text-align:justify;
}

</style>
</head>
<body>
<p class="isbn">ISBN : 978-2-36938-</p>

<p class="logo"><img src="images/logo.png"  alt="logotype" /></p>

<p class="erratum">Merci de nous signaler toute étourderie typographique ou légèreté grammaticale qui ne devrait jamais nous échapper lors d’une relecture.</p>

<p class="bordeaux">Bordeaux,  2016.</p>

<p class="url"><a href="http://jeroboamn.wordpress.com">jeroboamn.wordpress.com</a></p>
<p class="courriel"><a href="mailto:jeroboam.n@gmail.com">jeroboam.n@gmail.com</a></p>
</body>
</html>
'''

# xhtml_copyright = '''<p class="credits">Copyright © 2012  </p>'''

xhtml_copyright = '''<p class="credits"> , 2016.</p>
<p class="credits">Domaine public.</p>
<p class="credits">Source : <a href=""></a></p>

<p class="credits">Livre électronique réalisé à partir de l’ouvrage publié en .</p>
'''

couv='''<html xmlns="http://www.w3.org/1999/xhtml" xmlns:ops="http://www.idpf.org/2007/ops" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<head>
<title></title>

<style type="text/css">
</style>
<meta content="application/xhtml+xml; charset=utf-8" http-equiv="Content-Type"/>
</head>
<body style="margin-top: 0px; margin-left: 0px; margin-right: 0px; margin-bottom: 0px; text-align: center;">

<div>
    <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" height="100%" preserveAspectRatio="xMidYMid meet" version="1.1" viewBox="0 0 600 800" width="100%">
      <image height="800" width="600" xlink:href="images/cover.svg" />
    </svg>
 </div>
</body>
</html>
'''

titre='''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN"
   "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
<html xmlns="http://www.w3.org/1999/xhtml"  xml:lang="en">
<head>
<title> </title>
<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />
<link rel="stylesheet" href="css/cca.css" type="text/css" />
</head>

<body>

<h5>titre</h5>

<h6>auteur</h6>

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
    creationCredits()
    creationCopyright()
    creationCouvTitre()
    creationPageTitre()

def creationPageTitre():
    fichier = open('titre.xhtml','w')
    fichier.write(titre)
    fichier.write(newline)
    fichier.close()

def creationCouvTitre():
    couverture = open('couverture.xhtml','w')
    couverture.write(couv)
    couverture.write(newline)
    couverture.close()

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



def creationNcx(numid,intitule,source):
    trame = "<navPoint class=\"other\" id=\"%s\" playOrder=\"%i\">\n<navLabel>\n<text>%s</text>\n</navLabel>\n<content src=\"%s\"/>\n</navPoint>\n"
    fichier = open('toc.ncx','w')
    fichier.write(debutncx)
    fichier.write(newline)
    for x in range(len(numid)):
        texte = trame % (numid[x].lower(),x+2,intitule[x],source[x])
        fichier.write(texte)
        fichier.write(newline)
    nb = len(numid)
#    fin = finncx % (nb+1,nb+2)
    fin = finncx % (nb+2,nb+3)
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
