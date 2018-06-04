# Miscellaneous things

## da_installer.py

A python script to compile and install the MATE dock applet from Github. It will also install any missing dependencies. 

Untunt 16.04 and 18.04 are supported, as is Linux Mint 18.3. On Ubuntu you get the very latest applet code from git, whereas on Mint you get V0.80. which is the latest version of the applet that will work on that distro.

To use da_installer.py simply git clone this repository or download directly from [this link](https://raw.githubusercontent.com/robint99/misc/master/da_installer.py) (right click and do 'save as'). Once you have the file, open up a terminal, cd to the directory where you saved the file and do python3 da_installer.py. 

After using da_installer, you can revert to the version of the dock applet supplied by your disto by running `sudo apt install mate-dock-applet`
