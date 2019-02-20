#!/bin/bash

mkdir portrait;
mkdir paysage;
for image in *.*; 
do
export hauteur=`identify -format %h "$image"`
export largeur=`identify -format %w "$image"`

if [  $hauteur -ge $largeur ]
then
cp "$image" portrait;

else

cp "$image" paysage;

fi

done
