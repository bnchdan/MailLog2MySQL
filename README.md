# MailLog2MySQL
Parse mail logs to mysql


# apache config
enmod mod rewrite
<VirtualHost *:8888>
        DocumentRoot /var/www/MailLog2MySQL

        <Directory /var/www/MailLog2MySQL>
            Options Indexes FollowSymLinks MultiViews
            AllowOverride All
            Order allow,deny
            allow from all
        </Directory>

        ErrorLog ${APACHE_LOG_DIR}/error.log
        CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>




##create rc.local 
#!/bin/sh -e
/etc/init.d/maillog2mysql start
exit 0

chmod +x /etc/rc.local