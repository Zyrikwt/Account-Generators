# OSINT Industries Account Generation

## Description
This script automates the process of email verification on OSINT Industries (https://osint.industries). It generates a temporary email address, listens for incoming verification emails, extracts the 6-digit verification code, and uses it to complete the registration process on the website.

## Installation Guide
### 1. Python Environment
Ensure you have Python 3 installed on your system.

### 2. Dependencies
Install the required Python dependencies using pip:
- pip install selenium mailtm

### 3. WebDriver
You need to download the Microsoft Edge WebDriver compatible with your Microsoft Edge browser version. You can download it from the official Microsoft WebDriver download page:
https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/

Download Microsoft WebDriver
### 4. WebDriver Location
Place the downloaded WebDriver executable in a directory that is included in your system's PATH environment variable. This is essential for Selenium to locate and use the WebDriver.

## Usage
### Run the script
- python main.py

The script will provide you with two options:

### Option 1: 
- Generate and automate the verification process.
### Option 2: 
- Quit the script.

The script will generate a temporary email address and listen for incoming verification emails.

When a verification email is received, it will extract the 6-digit verification code and use it to complete the registration process on the target website.

After successful completion or timeout, the script will display the email address and password used for registration, and output to credentials.txt.
