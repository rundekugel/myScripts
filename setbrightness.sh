#!/bin/bash
echo set brightness 2021 by rundekugel

echo -n "max brightness: "
cat /sys/class/backlight/acpi_video0/max_brightness 
echo set brightness to $1.
echo $1 > /sys/class/backlight/acpi_video0/brightness
