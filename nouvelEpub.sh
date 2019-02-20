#!/bin/bash
#25.06.2012
#21.11.2013

metainf="<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<container version=\"1.0\" xmlns=\"urn:oasis:names:tc:opendocument:xmlns:container\">
  <rootfiles>
    <rootfile full-path=\"OEBPS/content.opf\" media-type=\"application/oebps-package+xml\" />
  </rootfiles>
</container>
"

basicCss="
body {
margin-top:1em;
margin-left:15px;
margin-right:13px;
}

p {
font-family:serif,sans-serif;
font-style:normal;
text-indent:1em;
text-align:justify;
margin:0.3em 0 0.3em 0;
} 

p.noindent{
text-indent:0;
}

p.centre {
text-indent:0;
text-align:center;
}

p.credits {
text-indent:0;
text-align:left;
}

p.stella {
font-size:120%;
font-weight:bold;
text-indent:0;
text-align:center;
margin:1em 0 1em 0;
}


p.lignevide {
margin-top:1.3em;
}


em {
font-style:italic;
}

em em {
font-style:normal;
}

sup {
font-size:80%;
line-height:1.2;
vertical-align:top;
}

h1 {
font-family:serif,sans-serif;
font-size:135%;
text-align:center;
text-indent:0;
margin:1em 0 1em 0;
}

hr.bat  {
margin:4.5em 40% 1.5em 40%;
}

hr.bi  {
margin:1.5em 40% 2.5em 40%;
}
"

couverture="<html xmlns=\"http://www.w3.org/1999/xhtml\" xmlns:ops=\"http://www.idpf.org/2007/ops\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">
<head>
<title></title>
<style type=\"text/css\">
</style>
<meta content=\"application/xhtml+xml; charset=utf-8\" http-equiv=\"Content-Type\"/>
</head>
<body style=\"margin-top: 0px; margin-left: 0px; margin-right: 0px; margin-bottom: 0px; text-align: center;\">
 <div>
    <svg xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" height=\"100%\" preserveAspectRatio=\"xMidYMid meet\" version=\"1.1\" viewBox=\"0 0 600 800\" width=\"100%\">
      <image height=\"800\" width=\"600\" xlink:href=\"images/cover.png\"></image>
    </svg>
 </div>
</body>
</html>
"

pagetitre="<html xmlns=\"http://www.w3.org/1999/xhtml\" xmlns:ops=\"http://www.idpf.org/2007/ops\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\">
<head>
<title></title>
<style type=\"text/css\">
</style>
<meta content=\"application/xhtml+xml; charset=utf-8\" http-equiv=\"Content-Type\"/>
</head>
<body style=\"margin-top: 0px; margin-left: 0px; margin-right: 0px; margin-bottom: 0px; text-align: center;\">
 <div>
    <svg xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" height=\"100%\" preserveAspectRatio=\"xMidYMid meet\" version=\"1.1\" viewBox=\"0 0 600 800\" width=\"100%\">
      <image height=\"800\" width=\"600\" xlink:href=\"images/titre.png\"></image>
    </svg>
 </div>
</body>
</html>
"
mkdir OEBPS;
mkdir OEBPS/css;
mkdir OEBPS/images;
mkdir OEBPS/textes;
mkdir META-INF;
echo -ne "$metainf" > META-INF/container.xml;
echo -ne 'application/epub+zip' > mimetype;
echo -ne "$basicCss" > OEBPS/css/cca.css;
#echo -ne "$couverture" > OEBPS/couverture.xhtml;
#echo -ne "$pagetitre" > OEBPS/page_de_titre.xhtml;
