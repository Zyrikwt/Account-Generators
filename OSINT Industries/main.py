import mailtm
import random
import string
import time
import re
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options

def extract_verification_code(text):
    match = re.search(r'(?<!\d)\d{6}(?!\d)', text)
    if match:
        return match.group(0)
    return None

def generate_random_password(length=16):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

random_password = generate_random_password()
verification_code = None

def clear_terminal():
    if os.name == 'posix':
        os.system('clear')
    elif os.name == 'nt':
        os.system('cls')

def automate_web_actions(sender_email, password):
    driver = None

    try:
        options = Options()
        options.add_argument("headless")
        options.add_argument("--log-level=3")
        options.add_argument("--disable-logging")

        driver = webdriver.Edge(options = options)

        driver.get("https://auth.osint.industries/ui/registration")

        email_input = driver.find_element("css selector", 'input[name="traits.email"]')
        email_input.send_keys(sender_email)

        password_input = driver.find_element("css selector", 'input[name="password"]')
        password_input.send_keys(password)

        checkbox = driver.find_element("css selector", 'input[name="traits.tos"]')
        checkbox.click()

        signup_button = driver.find_element("xpath", '//button[contains(text(), "Sign up")]')
        signup_button.click()

        while True:
            if verification_code:
                break
            else:
                time.sleep(1)

        code_input = driver.find_element("css selector", 'input[name="code"]')
        code_input.send_keys(verification_code)

        submit_button = driver.find_element("xpath", '//button[contains(text(), "Submit")]')
        submit_button.click()

    except Exception as e:
        print("An error occurred:", str(e))

    finally:
        if driver:
            driver.quit()
            
        with open("credentials.txt", "a") as file:
            file.write(f"{sender_email}\n")
            file.write(f"{password}\n\n")

        print("\nEmail:", sender_email)
        print("Password:", password)

def listener(message):
    global verification_code
    subject = message['subject']
    body = message['text'] if message['text'] else message['html']

    verification_code = extract_verification_code(body)

    if verification_code:

        random_password = generate_random_password()

        sender_email = message['from']
    else:
        print("No 6-digit verification code found in the email body")

def main():
    
    clear_terminal()
    while True:
        print("Choose an option:")
        print("1. Generate")
        print("2. Quit")

        choice = input("Enter your choice (1/2): ")

        if choice == "1":
            run_once()
            break
        elif choice == "2":
            print("Quitting...")
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")

def run_once():
    test = mailtm.Email()
    test.register()

    email_address = test.address
    print("\nGenerating account, please wait...")

    try:
        test.start(listener)

        automate_web_actions(email_address, random_password)

        timeout_seconds = 30
        start_time = time.time()

        while verification_code is None:
            if time.time() - start_time > timeout_seconds:
                print("Timeout: No verification code received within the timeout period.")
                break

        test.stop()
    except KeyboardInterrupt:
        print("Stopping script...")
        test.stop()

if __name__ == "__main__":
    main()