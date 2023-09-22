#!/bin/bash
LOG_PATH="/var/log/mail.log"


echo "
Sep 22 04:04:15 mail postfix/cleanup[50522]: QueueID: message-id=<MsgID>
Sep 22 04:04:15 mail postfix/qmgr[861]: QueueID: from=<user@test.ro>, size=7028, nrcpt=1 (queue active)
Sep 22 04:04:15 mail postfix/local[50524]: QueueID: to=<user@test.ro>, relay=local, delay=0.12, delays=0.12/0/0/0, dsn=2.0.0, status=sent
Sep 22 04:04:15 mail postfix/qmgr[861]: QueueID: removed
" >> $LOG_PATH
# output:
# *************************** 1. row ***************************
#               id: 681
#            month: Sep
#              day: 22
#             hour: 04
#          mail_to: user
#   mail_to_domain: test.ro
#        mail_from: user
# mail_from_domain: test.ro
#           status: sent
#            msgid: MsgID



echo "
Sep 22 04:02:55 mail dovecot: auth-worker(2506): conn unix:auth-worker (pid=2420,uid=0): auth-worker<48865241>: sql(user1@test.ro,192.168.1.23,<tgBHif/3pJReNHGH>): Password mismatch
Sep 22 02:05:00 mail dovecot: imap-login: Login: user=<user@test.ro>, method=PLAIN, rip=192.168.123, lip=192.168.1.3, pid=48597, TLS
Sep 22 04:05:19 mail dovecot: pop3-login: Login: user=<user@test.ro>, method=PLAIN, rip=192.168.123, lip=192.168.1.3, pid=52386, TLS
" >> $LOG_PATH
# output:
# *************************** 1. row ***************************
#     id: 185214
#  month: Sep
#    day: 22
#   hour: 04
# domain: test.ro
#     ip: 192.168.1.23
#  email: user1
#    log: Password mismatch
# *************************** 2. row ***************************
#     id: 185215
#  month: Sep
#    day: 22
#   hour: 02
# domain: test.ro
#     ip: 192.168.123
#  email: user
#    log: logged in imap-login
# *************************** 3. row ***************************
#     id: 185216
#  month: Sep
#    day: 22
#   hour: 04
# domain: test.ro
#     ip: 192.168.123
#  email: user
#    log: logged in pop3-login



echo "
Sep 22 04:02:44 mail dovecot: pop3(user@test.ro)<16586><fffff>: expunge: box=INBOX, uid=216970, msgid=<MsdID>, size=271290
Sep 22 04:02:55 mail dovecot: imap(user@test.ro)<51452><fffff>: delete: box=Drafts, uid=2942, msgid=<MsgID>, size=3122
Sep 22 04:02:55 mail dovecot: imap(user@test.ro)<51452><fffff>: expunge: box=Drafts, uid=2942, msgid=<MsgID>, size=3122
" >> $LOG_PATH
# output:
# *************************** 1. row ***************************
#     id: 2476
#  month: Sep
#    day: 22
#   hour: 04
# domain: test.ro
#  email: user
#  msgid: MsdID
#    log: expunge: box=INBOX
# *************************** 2. row ***************************
#     id: 2477
#  month: Sep
#    day: 22
#   hour: 04
# domain: test.ro
#  email: user
#  msgid: MsgID
#    log: delete: box=Drafts
# *************************** 3. row ***************************
#     id: 2478
#  month: Sep
#    day: 22
#   hour: 04
# domain: test.ro
#  email: user
#  msgid: MsgID
#    log: expunge: box=Drafts


mysql -p maillog <<'EOF'
select * from postfix_logs \G 
select * from auth_logs \G
select * from dovecot_logs \G
EOF

