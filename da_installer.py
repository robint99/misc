#!/usr/bin/env python3

""" Install the latest version of the MATE dock applet from github on
    Ubuntu, and Linux Mint distros

"""

# Copyright (C) 1997-2003 Free Software Foundation, Inc.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
# 02110-1301, USA.
#
# Author:
#     Robin Thompson

import platform
import subprocess
import os
import sys

class AppletInstaller(object):
    """ Class to query the Linux distribution being used"""

    def __init__(self):
        """ Set everything up, get the distro
        """

        vendor, release, name = platform.linux_distribution()

        self.distro = "Not supported"
        if vendor == "Ubuntu":
            if release == "16.04":
                self.distro = "Ubuntu 16.04"
            elif release == "17.10":
                self.distro = "Ubuntu 17.10"
            elif release == "18.04":
                self.distro = "Ubuntu 18.04"
        elif vendor == "LinuxMint":
            if release == "18.3":
                self.distro = "Mint 18.3"
            elif release == "19":
                self.distro = "Mint 19"

        self.workdir = os.path.expanduser("~/dock_applet/")

    def get_applet_version(self):
        """ Return the version of the applet that will be installed for the
            current distribution

            Returns:
                    "current" : the very latest code i.e. do a git clone
                    "Vx.xx"   : a specific version number. The version must have
                                been tagged as a release on git so that the source
                                can be downloaded
                    ""        : we can't do anything for this distro
        """

        if self.distro in ["Ubuntu 16.04", "Ubuntu 17.10", "Ubuntu 18.04", "Mint 19"]:
            return "current"
        elif self.distro == "Mint 18.3":
            return ("V0.80")
        else:
            return ""

    def get_dependencies(self):
        """Return a list of dock applet dependencies for the distro"
        """

      
        if self.distro in ["Ubuntu 18.04", "Mint 19"]:
            return ["git", "automake", "autoconf", "libglib2.0-dev", "bamfdaemon", "gir1.2-bamf-3",
                    "python-gi-cairo", "python3-pil", "python3-xlib"]
        elif self.distro == "Ubuntu 16.04":
            return ["git", "automake", "autoconf", "libglib2.0-dev", "bamfdaemon", "gir1.2-bamf-3",
                    "python-gi-cairo", "python3-pil", "python3-xlib"]
        elif self.distro == "Mint 18.3":
                  return ["git", "automake", "autoconf", "libglib2.0-dev", "bamfdaemon", "gir1.2-bamf-3",
                    "python-gi-cairo", "python3-pil", "python3-xlib", "wget", "tar"]
        else:
          return []

    def get_installed_packages(self):
        """ Returns a list of all installed packages """

        dpkg_cmd = subprocess.Popen("dpkg --get-selections", shell=True, stdout=subprocess.PIPE)
        dpkg_line = None
        package_list = []
        for dpkg_line in dpkg_cmd.stdout:
            package_name = dpkg_line.decode("utf-8").split("\t")[0]
            package_name = package_name.split(":")[0]
            package_list.append(package_name)

        return package_list

    def package_installed (self, pkg_name, package_list):
        """
            Checks to see if the specified package is in the list of
            installed packages
        """

        try:
            i = package_list.index(pkg_name)
        except ValueError:
            i = -1

        return i != -1

    def get_deps_to_install(self, dependencies):
        """ Check which dependencies are installed and which are not.
           
            Returns : a list of dependencies which need to be installed
        """

        to_install = []
        package_list = self.get_installed_packages()
        for package in dependencies:
            if not self.package_installed(package, package_list):
                to_install.append(package)

        return (to_install)

    def install_packages(self, packages):
        """ Use the apt command to install a list of packages
        """

        apt_command = "sudo apt-get --assume-yes install"
        for package in packages:
            apt_command += " " + package

        apt_cmd = subprocess.Popen(apt_command, shell=True, stdout=subprocess.PIPE)
        apt_line = None
        for apt_line in apt_cmd.stdout:
            print (apt_line.decode("utf-8"), end="")
            pass

    def run_shell_command(self, command, wd = None):
        """ Run a command in a shell (using a working dir if specfied) and print the output """

        if wd is None:
            cmd = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        else:
            cmd = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, cwd=wd)

        output_line = None
        for output_line in cmd.stdout:
            print (output_line.decode("utf-8"), end="")
            pass

    def get_distro(self):
        """ Return the distro type
        """
        return self.distro    

    def create_working_dir(self):
        """ Create a dir in the user's home where the source can be 
            downloaded and compiled """
        if not os.path.exists(self.workdir):
            os.mkdir(self.workdir)

    def get_source(self):
        """ Get the source for the dock applet. 
        
            If we're getting the source from git do a git clone if we don't already have 
            any source code, otherwise do go pull origin master.

            If we're getting a specific version, hmmmm...

            Note: the working directory must have been created before calling this ....
        """
            
        wd = self.workdir + "mate-dock-applet"
        if self.get_applet_version() == "current":
            if not os.path.exists(wd):
                # git clone
                self.run_shell_command("git clone https://github.com/robint99/mate-dock-applet.git",
                                        self.workdir)
            else:
                self.run_shell_command("git pull origin master", wd)

        else:
            if not os.path.exists(wd):
                os.makedirs(wd)
            av = self.get_applet_version()

            # get a tarball of the required version and unzip it
            self.run_shell_command("wget https://github.com/robint99/mate-dock-applet/tarball/%s" %av, self.workdir)
            self.run_shell_command("tar -xvf %s%s -C %s --strip-components=1" %(self.workdir, av, wd))

    def make_source(self):
        """ Make the applet ...."""

        wd = self.workdir + "/mate-dock-applet"
        self.run_shell_command("aclocal", wd)
        self.run_shell_command("automake --add-missing", wd)
        self.run_shell_command("autoreconf", wd)
        if self.distro != "Ubuntu 16.04":
            # all but Ubuntu 16.04 require Gtk3
            self.run_shell_command("./configure --prefix=/usr --with-gtk3", wd)
        else:
            self.run_shell_command("./configure --prefix=/usr", wd)

        self.run_shell_command("make", wd)
   
        
    def install_source(self):
        """ sudo make install ... """
        wd = self.workdir + "/mate-dock-applet"
        self.run_shell_command("sudo make install", wd)

    def uninstall(self):
        """ sudo make uninstall """
        wd = self.workdir + "/mate-dock-applet"
        if os.path.exists(wd):
            self.run_shell_command("sudo make uninstall", wd)
        
def main():

    ver ="0.01"
    print("\nMATE dock applet installer V%s\n" %ver)
    print("This program will install the latest version of the dock applet")
    print("supported by your distribution. For most users this will typically")
    print("For most users this will typically be the latest development")
    print("version from GitHub\n")

    print("The program will install any addtional software it needs to compile")
    print("the dock applet, download the source code, compile and then install")
    print("it. You may be required to enter the sudo password during this")
    print("process.\n")
    
    print("Note 1: this supports Ubuntu and Linux Mint distributions only.\n")

    print("Note 2: a directory named 'dock_applet' will be created under your")
    print("home directory and will contain the applet source code. You should")
    print("keep this directory if you want to uninstall the applet later.\n")

    print("Note 3: to undo what this program does and revert to the version of")
    print("the dock applet supplied by your distribution run ")
    print("'python3 da_installer.py uninstall' followed by 'sudo apt")
    print("install mate-dock-applet'\n")   

    print("Note 4: this program should work reliably but is not robust. Use at")
    print("your own discretion.\n")

    input("Press Enter to continue or Ctrl-C to abort: ")

    ai = AppletInstaller()

    if len (sys.argv) == 1:
        # default action is to install
        deps = ai.get_dependencies()
        install_pkgs = ai.get_deps_to_install(deps)
        if install_pkgs != []:
            print("\n\n Installing dependencies \n\n")
            ai.install_packages(install_pkgs)

        ai.create_working_dir()
        print("\n\nGetting source code \n\n")
        ai.get_source()

        print ("\n\nMaking the applet...\n\n")
        ai.make_source()

        print ("\n\n Installing ....\n\n")
        ai.install_source()

        print ("\n\nDone - to be safe, log out and back in before trying your")
        print ("new applet.\n\n")
    elif len (sys.argv)==2 and sys.argv[1] == "uninstall":
        ai.uninstall()

    # create dir
    # git clone the dir / download a tarball and unzip it

    return
if __name__ == "__main__":
    main()
