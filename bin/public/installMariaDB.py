#!/usr/bin/env python
'''
Install a secure mysql server.

Read more
http://dev.mysql.com/doc/refman/5.0/en/security-guidelines.html
http://dev.mysql.com/doc/refman/5.0/en/security-against-attack.html
http://dev.mysql.com/doc/refman/5.0/en/mysqld-option-tables.html
http://www.learn-mysql-tutorial.com/SecureInstall.cfm

'''

__author__ = "matte@elino.se"
__copyright__ = "Copyright 2011, The System Console project"
__maintainer__ = "Mattias Hemmingsson"
__email__ = "syco@cybercow.se"
__credits__ = ["???"]
__license__ = "???"
__version__ = "1.0.0"
__status__ = "Production"

import fileinput
import os
import re
import shutil

from general import x
import app
import config
import general
import iptables
import version


# The version of this module, used to prevent the same script version to be
# executed more then once on the same host.
SCRIPT_VERSION = 1


def build_commands(commands):
  commands.add("install-mariadb",             install_mariadb, help="Install mariadb server on the current server.")
  commands.add("uninstall-mariadb",           uninstall_mariadb, help="Uninstall mariadb server on the current server.")
  
def install_mariadb(args):
	'''
	Installing mariadb by adding new repo file and using yum to install
	'''
	x("echo '[mariadb]' > /etc/yum.repos.d/MariaDB.repo")
	x("echo 'name = MariaDB' >> /etc/yum.repos.d/MariaDB.repo")
	x("echo 'baseurl = http://yum.mariadb.org/5.5/centos5-x86' >> /etc/yum.repos.d/MariaDB.repo")
	x("echo 'gpgkey=https://yum.mariadb.org/RPM-GPG-KEY-MariaDB' >> /etc/yum.repos.d/MariaDB.repo")
	x("echo 'gpgcheck=1' >> /etc/yum.repos.d/MariaDB.repo")
	
	x("yum install MariaDB-server MariaDB-client -y")

def uninstall_mariadb(args):
	'''
	Uninstalling MariaDb server
	'''
	x("yum remove MariaDB-server MariaDB-client MariaDB-common -y")
	x("\\rm /etc/yum.repos.d/MariaDB.repo")