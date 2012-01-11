#!/bin/env python
''''
mysql-lvm-backup.py

Does a lvm snapshot on the lvm Logical Volume where the mysql database are
stored, and mounts the snapshot. This gives the possibility to tar/cp/rsync all
database files from the snapshot mount.

REQUIREMENTS
============

This file needs to be created, to do it possilbe for the mysql client can login
to mysql database without expose the mysql password on command line (ps aux) or
in this script.

#/root/.my.cnf
[client]
user=root
password="<password>"

RSNAPSHOT
=========

If you are going to use rsnapshot to create the backup, add the following lines
to /etc/rsnapshot.conf. Remember to setup the ssh-keys.

backup_script   /usr/bin/ssh root@example.com "/opt/syco/var/mysql/mysql-lvm-backup.py snapshot" unused0/
backup          root@example.com:/mnt/mysqlbackup/                      			     	     example.com/
backup_script   /usr/bin/ssh root@example.com "/opt/syco/var/mysql/mysql-lvm-backup.py clean"    unused1/

READ MORE
=========

http://poller.se/2010/12/rsnapshot-and-mysqldump/
http://rsnapshot.org/rsnapshot.html
http://www.mysqlperformanceblog.com/2006/08/21/using-lvm-for-mysql-backup-and-replication-setup/

'''

__author__ = "daniel.lindh@cybercow.se"
__copyright__ = "Copyright 2011, The System Console project"
__maintainer__ = "Daniel Lindh"
__email__ = "syco@cybercow.se"
__credits__ = ["???"]
__license__ = "???"
__version__ = "1.0.0"
__status__ = "Production"

# Folder where the snapshot will be mounted.
backupMountPath="/mnt/mysqlbackup"

# Volgroup where the lvm Logical Volume are stored. (find with lvdisplay)
# ie. VolGroup00 in /dev/VolGroup00/var
vgName = "VolGroup00"

# Logical Volume where the backup is stored. (find with lvdisplay)
# ie. var in /dev/VolGroup00/var
lvName = "var"

# Size of snapshot Logical Volume. Need to be able to store all changes
# that are done in the partion during the time the snapshot exists.
snapshotSize = "2G"

# Import used python modules.
import os
import subprocess
from optparse import OptionParser

# String codes affecting output to shell.
BOLD = "\033[1m"
RESET = "\033[0;0m"

# Globals set with set_global_options_and_args. Contains all arguments set
# from command line.
OPTIONS = None
ARGS = None

def main():
	'''
	Starts the script.

	'''
	set_global_options_and_args()

	# Handle the dynamic arguments on from the command line.
	commands = {'snapshot' : snapshot, 'clean': clean}
	command = ARGS[0].lower()
	if command in commands:
		commands[command]()

def set_global_options_and_args():
    '''
    Set cmd line arguments in global vars OPTIONS and ARGS.

    '''
    global OPTIONS, ARGS
    parser = OptionParser(usage="usage: %prog {snapshot|clean}")
    (OPTIONS, ARGS) = parser.parse_args()

    if len(ARGS) != 1:
        parser.error("incorrect number of arguments")

def snapshot():
	'''
	Flush mysql tables, do the snapshot and mount the snapshot.

	'''
	clean()
	print "Do snapshot"
	x("modprobe dm-snapshot")
	x("""mysql -uroot << EOF
flush tables;
FLUSH TABLES WITH READ LOCK;
system lvcreate -L%s -s -n %sbackup /dev/%s/%s
UNLOCK TABLES;
EOF""" % (snapshotSize, lvName, vgName, lvName))
	x("mkdir -p %s" % backupMountPath)
	x("mount /dev/%s/%sbackup %s" % (vgName, lvName, backupMountPath))

def clean():
	'''
	Remove mounts and snapshots.

	'''
	print "Remove last snapshot."

	if (os.path.ismount(backupMountPath)):
		x("umount %s" % backupMountPath)

	backupPath = "/dev/%s/%sbackup" % (vgName, lvName)
	if (os.path.exists(backupPath)):
		x("lvremove -f %s" % backupPath)

def x(cmd):
    '''
    Execute the shell command CMD.

    '''
    print(BOLD + "Command: " + RESET + cmd)

    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdout, stderr) = p.communicate()
    (stdout, stderr, p.pid)
    if (stdout):
        print(stdout)
    if (stderr):
        print(stderr)

if __name__ == "__main__":
    main()