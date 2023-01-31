#!/bin/bash

echo execute this as sudo
echo install monodevelop...
apt update
sudo apt install dirmngr gnupg apt-transport-https ca-certificates software-properties-common -y

echo install sources...
sudo apt-add-repository 'deb https://download.mono-project.com/repo/ubuntu stable-focal main'
# this was before ubuntu 22: sudo apt-key adv --recv-keys --keyserver keyserver.ubuntu.com 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF  
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF
sudo apt update

echo monodevelop...
sudo apt install mono-complete -y
# sudo apt install monodevelop

echo versioncontrol...
sudo apt install  monodevelop-versioncontrol -y

echo done.
ping ::1 -c 3
