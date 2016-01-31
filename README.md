# backup-scripts 

Basic python & bash script for remote backup.  Written pretty much for me.

Rsync is used to create a snapshot of the current system so that I'm not trying to backup files that may change.  The 'excludes' file lists all directories that shouldn't be backed up, one per line.  A backup is then created with tar using the snapshot directory as a source, piped through gpg and encrypted using the public key specified with 'gpgKey'.  This key has to first be imported and trusted before this works.  Could probably host the pubkey somewhere and have the script import it but I haven't taken the time to do that yet.
