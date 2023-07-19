install:
	mkdir /usr/lib/MailLog2MySQL
	cp -r lib/* /usr/lib/MailLog2MySQL
	mkdir /var/www/MailLog2MySQL
	cp -r WWW/* /var/www/MailLog2MySQL
	cp WWW/.htaccess /var/www/MailLog2MySQL/.htaccess
	cp etc/MailLog2MySQL.conf /etc/
	cp MailLog2MySQL /usr/local/bin
	chmod +x /usr/local/bin/MailLog2MySQL
	cp init.d/maillog2mysql /etc/init.d/maillog2mysql
	chmod +x /etc/init.d/maillog2mysql

delete:
	rm /usr/local/bin/MailLog2MySQL
	rm -rf /usr/lib/MailLog2MySQL
	rm -rf /var/www/MailLog2MySQL
	rm /etc/MailLog2MySQL.conf
	rm /etc/init.d/maillog2mysql

run: delete install
	nice -19 /usr/local/bin/MailLog2MySQL