#!/bin/bash

# Really, really need to replace some paths with variables instead. This really isn't going to work, I have to set multiple excludes and haven't looked up how to do this in bash yet. I'll probably have to just rewrite this in Python.

# The gpg pubkey of the target has to be imported and trusted before this works.
gpgkey=
excludes=
snapsource=/
snap=/snapshot/
tarincr=/var/log/backup.snap
backups=

now=$(date +"%m-%d-%Y"@"%H:%M")

# Here is the snapshot part of the backup:
echo "[*] Performing snapshot"
rsync -ah --delete --exclude $excludes $snapsource $snap

# And now for the incremental tar portion:
echo "[*] Creating backup file for $now"

# If it's Sunday, do a full backup. Otherwise, run incremental based on backup.snap.
today=$(date +"%a")
if [ $today == Sun ]
then
rm -rf $tarincr && cd $snap && tar -g $tarincr -cpzf - . | gpg -e --cipher-algo AES256 -o $backups/backup-$now-full.tgz.gpg -r $gpgkey -
else
cd $snap && tar -g $tarincr -cpzf - . | gpg -e --cipher-algo AES256 -o $backups/backup-$now-inc.tgz.gpg -r $gpgkey -
fi

echo "[*] Completed backup for $now."

# If today is Sunday, delete all incrementals from the prior week, and older full backup

if [ $today == Sun ]
then
echo "[*] It's cleanup time, bitches."
find $backups -mtime +2 -name '*full*' -print | xargs rm
find $backups -name '*inc*' -print | xargs rm
fi