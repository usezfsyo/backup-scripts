#!/usr/bin/env python

import pexpect
import datetime
from datetime import datetime
import sys
import subprocess
from subprocess import Popen, PIPE

def cleanUp(directory):
	doW = datetime.now().weekday()
	if doW == 6:
		print "[+] It's Sunday. Cleaning old backup files."
		p1 = Popen(["find", directory, "-name", "*inc*", "-print"], stdout=PIPE)
		p2 = Popen(["xargs", "rm", "-rf"], stdin=p1.stdout, stdout=PIPE)
		p1.stdout.close()
		p2.communicate()[0]
		p1 = Popen(["find", directory, "-name", "*full*", "-mtime", "+14", "-print"], stdout=PIPE)
		p2 = Popen(["xargs", "rm", "-rf"], stdin=p1.stdout, stdout=PIPE)
		p1.stdout.close()
		p2.communicate()[0]

def syncBackup(key, keyPass, source, dest):
	ssh_cmd = '-e "ssh -i %s"' % (key)
	cmd = 'rsync -ah %s %s %s' % (ssh_cmd, source, dest)
	child = pexpect.spawn(cmd, timeout=600)
	child.expect('passphrase')
	child.sendline(keyPass)
	index = child.expect([pexpect.EOF, pexpect.TIMEOUT])
	if index == 0:
		now = datetime.strftime(datetime.now(), '%H:%M')
		print "[+] Completed syncing from %s at %s" % (source, now)
	elif index == 1:
		print "[-] Timeout reached."
	child.close()

def main():
	key = ''
	keyPass = ''
	source = ''
	dest = ''
	syncBackup(key, keyPass, source, dest)
	cleanUp(dest)

if __name__ == "__main__":
	main()

