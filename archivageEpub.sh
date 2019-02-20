#!/bin/bash
#28.12.2011


zip -X $1 mimetype;
zip -rg $1 META-INF;
zip -rg $1 OEBPS;


