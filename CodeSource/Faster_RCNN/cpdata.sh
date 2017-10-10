#!/bin/bash

dhome='/home/cuong-nguyen/2017/Projets/New_driver_lisence_project/Data/Noveaupermis'
i=0
mkdir Annotations
mkdir Images
mkdir ImageSets
while [ $i -lt 2 ]
do
    echo "processing folder $dhome/$i"
    cp $dhome/$i/*.png Images
    cp $dhome/$i/*.xml Annotations
    let "i=i+1"
done
ls Annotations/ -m | sed s/\\s/\\n/g | sed s/.xml//g | sed s/,//g > ImageSets/train.txt