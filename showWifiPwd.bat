@echo off
echo Copyright 2022 by lifesim.de
echo Show WIFI key

set /p ssid="Type SSID and hit [ENTER]: "
echo %ssid%
echo -------------------------
echo siehe "Sicherheitseinstellungen/Schluesselinhalt"
echo look at "Security settings/Key Content"

netsh wlan show profile name="%ssid%" key=clear

pause

