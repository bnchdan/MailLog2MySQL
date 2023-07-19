# MailLog2MySQL
Parse mail logs from Postfix and Dovecot to mysql

# Install

### mysql
```
CREATE DATABASE maillog;
GRANT ALL PRIVILEGES ON maillog.* TO 'sammy'@'localhost' IDENTIFIED BY 'password';
FLUSH PRIVILEGES

```

### install script
```
make install

```

### apache config
enmod mod rewrite
create file MailLog2MySQL.conf
```
Listen 8888
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
```
```
a2ensite MailLog2MySQL.conf
```

### create rc.local
```
#!/bin/sh -e
/etc/init.d/maillog2mysql start
exit 0
```
```
chmod +x /etc/rc.local
```

### run
```
/etc/init.d/maillog2mysql start
```

# Example API
```
curl http://127.0.0.1:8888/api?table=dovecot_logs | jq .
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  3793  100  3793    0     0  1136k      0 --:--:-- --:--:-- --:--:-- 1234k
{
  "number of logs": 710,
  "number of pages": 36,
  "data": [
    {
      "id": 1,
      "month": "Mar",
      "day": "12",
      "hour": "08",
      "domain": "test.ro",
      "email": "dan",
      "msgid": "fdsajfnasfqq123412@mailtest2.ro",
      "log": "delete: box=INBOX"
    },
    {
      "id": 2,
      "month": "Mar",
      "day": "13",
      "hour": "09",
      "domain": "test.ro",
      "email": "dan",
      "msgid": "fdsajfnasfqq123412@mailtest2.ro",
      "log": "expunge: box=INBOX"
    },

curl http://127.0.0.1:8888/api?table=dovecot_logs&page=21
curl http://127.0.0.1:8888/api?table=dovecot_logs&month=Mar&day=12&hour=08&domain=test.ro&email=dan


```
```
curl http://127.0.0.1:8888/api?table=auth_logs | jq .
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  2900  100  2900    0     0   306k      0 --:--:-- --:--:-- --:--:--  314k
{
  "number of logs": 2669,
  "number of pages": 133,
  "data": [
    {
      "id": 1,
      "month": "Mar",
      "day": "12",
      "hour": "10",
      "domain": "test.ro",
      "ip": "192.168.1.1",
      "email": "dan2",
      "log": "unknown user"
    },
    {
      "id": 2,
      "month": "Mar",
      "day": "12",
      "hour": "10",
      "domain": "test.ro",
      "ip": "192.168.1.1",
      "email": "dan",
      "log": "logged in imap-login"
    },
```
```
curl http://127.0.0.1:8888/api?table=postfix_logs | jq .
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  6287  100  6287    0     0   403k      0 --:--:-- --:--:-- --:--:--  409k
{
  "number of logs": 1416,
  "number of pages": 71,
  "data": [
    {
      "id": 1,
      "month": "Mar",
      "day": "13",
      "hour": "00",
      "mail_to": "dan3",
      "mail_to_domain": "test.ro",
      "mail_from": "dan",
      "mail_from_domain": "test.ro",
      "status": "sent",
      "msgid": "jbhfdsan32@mail.test.ro"
    },

```