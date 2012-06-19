#!/usr/bin/env python
'''
Remove packages listed in hardening/config.cfg - part of the hardening.

'''

__author__ = "mattias@fareoffice.com"
__copyright__ = "Copyright 2011, The System Console project"
__maintainer__ = "Daniel Lindh"
__email__ = "syco@cybercow.se"
__credits__ = ["???"]
__license__ = "???"
__version__ = "1.0.0"
__status__ = "Production"


import app
import config
from scopen import scOpen
from general import x


def setup_common():
    yum_update()
    customize_shell()
    disable_usb()
    forward_root_mail()
    general_cis()


def yum_update():
  '''
  yum update is the first thing that is done when hardening the server,
  to minimize the risk that an updated package revert any hardening mods.
  '''
  app.print_verbose("Update with yum")
  x("yum update -y")


def customize_shell():
    app.print_verbose("Customize shell")

    app.print_verbose("  Add Date And Time To History Output")
    scOpen("/etc/bashrc").replace_add(
        "^export HISTTIMEFORMAT=.*$",
        "export HISTTIMEFORMAT=\"%h/%d - %H:%M:%S \""
    )

    app.print_verbose("  Add Color To Grep")
    root = scOpen("/root/.bash_profile")
    root.replace_add("^export GREP_COLOR=.*$",   "export GREP_COLOR='1;32'")
    root.replace_add("^export GREP_OPTIONS=.*$", "export GREP_OPTIONS=--color=auto")

    skel = scOpen("/etc/skel/.bash_profile")
    skel.replace_add("^export GREP_COLOR=.*$",   "export GREP_COLOR='1;32'")
    skel.replace_add("^export GREP_OPTIONS=.*$", "export GREP_OPTIONS=--color=auto")


def disable_usb():
    # Currently need usb dvd reader for installation.
    return
    app.print_verbose("Disable usb")
    scOpen("/etc/modprobe.d/syco.conf").replace_add(
        "^blacklist usb-storage$", "blacklist usb-storage"
    )
    x("chcon system_u:object_r:modules_conf_t:s0 /etc/modprobe.d/syco.conf")


def forward_root_mail():
    app.print_verbose("Forward all root email to " + config.general.get_admin_email())
    scOpen("/etc/aliases").replace(
        ".*root[:].*", "root:     " + config.general.get_admin_email()
    )
    x("/usr/bin/newaliases")

def general_cis():
    '''General CIS hardenings'''
    #
    app.print_verbose("1.1.17 Set Sticky Bit on All World-Writable Directories")
    x("find / -type d -perm -0002 -exec chmod a+t {} \; 2>/dev/null")

    #
    app.print_verbose("1.1.18 Disable Mounting of cramfs Filesystems")
    scOpen("/etc/modprobe.d/syco.conf").replace_add(
        "^install cramfs /bin/true$", "install cramfs /bin/true"
    )

    #
    app.print_verbose("1.1.19 Disable Mounting of freevxfs Filesystems")
    scOpen("/etc/modprobe.d/syco.conf").replace_add(
        "^install freevxfs /bin/true$", "install freevxfs /bin/true"
    )

    #
    app.print_verbose("1.1.20 Disable Mounting of jffs2 Filesystems")
    scOpen("/etc/modprobe.d/syco.conf").replace_add(
        "^install jffs2 /bin/true$", "install jffs2 /bin/true"
    )

    scOpen("/etc/modprobe.d/syco.conf").replace_add(
        "^install zlib_deflate /bin/true$", "install zlib_deflate /bin/true"
    )

    #
    app.print_verbose("1.1.21 Disable Mounting of hfs Filesystems")
    scOpen("/etc/modprobe.d/syco.conf").replace_add(
        "^install hfs /bin/true$", "install hfs /bin/true"
    )

    #
    app.print_verbose("1.1.22 Disable Mounting of hfsplus Filesystems")
    scOpen("/etc/modprobe.d/syco.conf").replace_add(
        "^install hfsplus /bin/true$", "install hfsplus /bin/true"
    )

    #
    app.print_verbose("1.1.23 Disable Mounting of squashfs Filesystems")
    scOpen("/etc/modprobe.d/syco.conf").replace_add(
        "^install squashfs /bin/true$", "install squashfs /bin/true"
    )

    #
    app.print_verbose("1.1.24 Disable Mounting of udf Filesystems")
    scOpen("/etc/modprobe.d/syco.conf").replace_add(
        "^install udf /bin/true$", "install udf /bin/true"
    )

    #
    app.print_verbose("1.6.1 SetUser/GroupOwneron/etc/grub.conf")
    x("chown root:root /etc/grub.conf")

    #
    app.print_verbose("1.6.2 Set Permissions on /etc/grub.conf")
    x("chmod og-rwx /etc/grub.conf")

    #
    app.print_verbose("1.6.5 Disable Interactive Boot")
    scOpen("/etc/sysconfig/init").replace_add(
        "^PROMPT=.*", "PROMPT=no"
    )

    #
    app.print_verbose("1.7.1 Restrict Core Dumps")
    scOpen("/etc/security/limits.conf").replace_add(
        "^\* hard core 0", "* hard core 0"
    )

    #
    app.print_verbose("3.1 Set Daemon umask")
    scOpen("/etc/sysconfig/init").replace_add(
        "^umask.*", "umask 027"
    )

    #
    app.print_verbose("4.4.1 Disable IPv6")
    scOpen("/etc/modprobe.d/syco.conf").replace_add(
        "^options ipv6.*$", 'options ipv6 "disable=1"'
    )

    #
    app.print_verbose("4.5 Install TCP Wrappers")
    x("yum install tcp_wrappers")

    #
    app.print_verbose("4.8.1 Disable DCCP")
    scOpen("/etc/modprobe.d/syco.conf").replace_add(
        "^install dccp /bin/true$", "install dccp /bin/true"
    )

    #
    app.print_verbose("4.8.2 Disable SCTP")
    scOpen("/etc/modprobe.d/syco.conf").replace_add(
        "^install sctp /bin/true$", "install sctp /bin/true"
    )

    #
    app.print_verbose("4.8.3 Disable RDS")
    scOpen("/etc/modprobe.d/syco.conf").replace_add(
        "^install rds /bin/true$", "install rds /bin/true"
    )

    #
    app.print_verbose("4.8.4 Disable TIPC")
    scOpen("/etc/modprobe.d/syco.conf").replace_add(
        "^install tipc /bin/true$", "install tipc /bin/true"
    )

    #
    app.print_verbose("6.1.4 Set User/Group Owner and Permission on /etc/crontab")
    x("chown root:root /etc/crontab")
    x("chmod og-rwx /etc/crontab")

    #
    app.print_verbose("6.1.5 Set User/Group Owner and Permission on /etc/cron.hourly")
    x("chown root:root /etc/crontab")
    x("chmod og-rwx /etc/crontab")

    #
    app.print_verbose("6.1.6 Set User/Group Owner and Permission on /etc/cron.daily")
    x("chown root:root /etc/cron.daily")
    x("chmod og-rwx /etc/cron.daily")

    #
    app.print_verbose("6.1.7 Set User/Group Owner and Permission on /etc/cron.weekly")
    x("chown root:root /etc/cron.weekly")
    x("chmod og-rwx /etc/cron.weekly")

    #
    app.print_verbose("6.1.8 Set User/Group Owner and Permission on /etc/cron.monthly")
    x("chown root:root /etc/cron.monthly")
    x("chmod og-rwx /etc/cron.monthly")

    #
    app.print_verbose("6.1.9 Set User/Group Owner and Permission on /etc/cron.d")
    x("chown root:root /etc/cron.d")
    x("chmod og-rwx /etc/cron.d")

    #
    app.print_verbose("6.1.10 Restrict at Daemon")
    x("rm /etc/at.deny")
    x("touch /etc/at.allow")
    x("chown root:root /etc/at.allow")
    x("chmod og-rwx /etc/at.allow")

    #
    app.print_verbose("6.1.11 Restrict at/cron to Authorized Users")
    x("/bin/rm /etc/cron.deny")
    x("/bin/rm /etc/at.deny")
    x("chmod og-rwx /etc/cron.allow")
    x("chmod og-rwx /etc/at.allow")
    x("chown root:root /etc/cron.allow")
    x("chown root:root /etc/at.allow")

    #
    app.print_verbose("9.2.13 Check That Defined Home Directories Exist")
    x("mkdir /var/adm")
    x("mkdir /var/spool/uucp")
    x("mkdir /var/gopher")
    x("mkdir /var/ftp")
    x("mkdir /var/empty/saslauth")


    #
    # After match
    #

    x("/sbin/sysctl -p")
