#!/bin/bash
#22.06.2012
#creation d'un fichier epub a partir du shell
#parametres singletonEpub nomFichier.xhtml nomEpub.epub

metainf="<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<container version=\"1.0\" xmlns=\"urn:oasis:names:tc:opendocument:xmlns:container\">
  <rootfiles>
    <rootfile full-path=\"OEBPS/content.opf\" media-type=\"application/oebps-package+xml\" />
  </rootfiles>
</container>
"

cssbase="
body {margin-top:1em;margin-left:13px;margin-right:13px;}
p {font-family:serif,sans-serif;font-size:1em;font-style:normal;text-indent:1em;text-align:justify;margin-top:0.3em;margin-bottom:0.3em;}
h1 {font-size:1.25em;text-indent:0;text-align:left;}
"

opf="<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<package version=\"2.0\" xmlns=\"http://www.idpf.org/2007/opf\" unique-identifier=\"BookId\">
  <metadata xmlns:dc=\"http://purl.org/dc/elements/1.1/\" xmlns:opf=\"http://www.idpf.org/2007/opf\">
    <dc:title>monodoc</dc:title>
    <dc:language>fr</dc:language>
    <dc:identifier id=\"BookId\">urn:uuid:inpennylane-123456</dc:identifier>
    <dc:creator opf:role=\"aut\">monodoc</dc:creator>
    <dc:date opf:event=\"original-publication\">2012</dc:date>
    <dc:date opf:event=\"ops-publication\">2012</dc:date>
    <dc:publisher>Jéroboam N.</dc:publisher>
    <dc:subject>monodoc</dc:subject>
  </metadata>
  <manifest>
    <item id=\"ncx\" href=\"toc.ncx\" media-type=\"application/x-dtbncx+xml\" />
<item id=\"bk001\" href=\"$1\" media-type=\"application/xhtml+xml\" />
</manifest>
  <spine toc=\"ncx\">
      <itemref idref=\"bk001\" linear=\"yes\" />
</spine>
</package>
"


ncx="<?xml version=\"1.0\"?>
<ncx xmlns=\"http://www.daisy.org/z3986/2005/ncx/\" version=\"2005-1\">
<head>
<meta name=\"dtb:uid\" content=\"inpennylane-123456\" />
<meta name=\"dtb:depth\" content=\"2\" />
<meta name=\"dtb:totalPageCount\" content=\"0\" />
<meta name=\"dtb:maxPageNumber\" content=\"0\" />
</head>

<docTitle>
<text>monodoc</text>
</docTitle>

<docAuthor>
<text>monodoc</text>
</docAuthor>

<navMap>
<navPoint class=\"other\" id=\"bk001\" playOrder=\"1\">
<navLabel>
<text>Texte</text>
</navLabel>
<content src=\"$1\"/>
</navPoint>
</navMap>
</ncx>
"

mkdir META-INF;
echo -ne "$metainf" > META-INF/container.xml;
echo -ne 'application/epub+zip' > mimetype;

mkdir OEBPS;
cp $1 OEBPS/;

echo "$opf" > OEBPS/content.opf;
echo "$ncx" > OEBPS/toc.ncx;

zip -X $2 mimetype;
zip -rg $2 META-INF;
zip -rg $2 OEBPS;
