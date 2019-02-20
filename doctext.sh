#!/bin/bash

for fichier in *.doc; do
antiword "$fichier" > "${fichier%.doc}.txt"
done

