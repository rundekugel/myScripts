#from: https://askubuntu.com/questions/969238/samsung-m2070w-scanner-no-longer-working-in-17-10

sudo ln -s /opt/smfp-common/scanner/lib/libsane-smfp.so.1.0.1 /usr/lib/x86_64-linux-gnu/sane/libsane-smfp.so.1
sudo apt install libusb-0.1-4
scanimage -L


