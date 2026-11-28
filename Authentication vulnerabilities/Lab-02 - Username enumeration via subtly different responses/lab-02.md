## Lab: Username enumeration via subtly different responses

This lab is subtly vulnerable to username enumeration and password brute-force attacks. It has an account with a predictable username and password, which can be found in the following wordlists:

- [Candidate usernames](https://portswigger.net/web-security/authentication/auth-lab-usernames)
- [Candidate passwords](https://portswigger.net/web-security/authentication/auth-lab-passwords)

To solve the lab, enumerate a valid username, brute-force this user's password, then access their account page.

---

## Notes

1/ Intercept the POST request via `Burp`.

2/ Enumerate the username using the wordlist `Candidate usernames` via `Burp Intruder`, then within the Intruder click `Settings` instead of Payloads, and go to `Grep - Extract` click `add` and `Fetch response`, then select the error message `Invalid username or password.` Then start the attack. After that filter with the new `warning` column and notice the subtly different.

3/ Set the correct username and brut force the password using the wordlist `Candidate passwords` via `Burp Intruder`, and filtering the results by status code searching for 302.

