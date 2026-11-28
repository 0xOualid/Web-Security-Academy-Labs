## Lab: Username enumeration via response timing

This lab is vulnerable to username enumeration using its response times. To solve the lab, enumerate a valid username, brute-force this user's password, then access their account page.

- Your credentials: `wiener:peter`
- [Candidate usernames](https://portswigger.net/web-security/authentication/auth-lab-usernames)
- [Candidate passwords](https://portswigger.net/web-security/authentication/auth-lab-passwords)

---

## Notes

1/ Intercept the POST request via `Burp`.

2/ Notice that your IP will be blocked if you make too many invalid login attempts. Then identify that the `X-Forwarded-For` header is supported, which allows you to spoof your IP address and bypass the IP-based brute-force protection. So we have to add the `X-Forwarded-For` header and change its value frequently.

3/ Notice that when we enter a valid username `wiener` with a very long password the response time is increased. But if we change to invalid username the response time stays normal.

4/ Enumerate the username using the wordlist `Candidate usernames` via `Burp Intruder`, then select `Pitchfork attack` and select the value of `X-Forwarded-For` using a number wordlist `from 10 to 110`, then select the username using the `Candidate usernames` wordlist. With a very long password. Then start the attack. After that, filter the results with the `Response received` column.

5/ Set the correct username and brut force the password using the wordlist `Candidate passwords` via `Burp Intruder`. Then select `Pitchfork attack` and select the value of `X-Forwarded-For` using a number wordlist `from 110 to 210`, then select the password using the `Candidate passwords` wordlist, and filtering the results by status code searching for 302.

