 dpkg --list|grep mysql
 sudo apt-get remove mysql-common
 sudo apt-get autoremove --purge mysql-server-5.7
 dpkg -l|grep ^rc|awk '{print$2}'|sudo xargs dpkg -P
 dpkg --list|grep mysql
 sudo apt-get autoremove --purge mysql-apt-config
 dpkg --list|grep mysql
