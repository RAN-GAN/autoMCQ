from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import json
import re

 
print('---------------------------------------------------------------\n')
print('get the test url before entering the credentials!\n')
print('---------------------------------------------------------------\n')

userId = input("Enter your mailId: ")
password = input("Enter your password: ")

testUrl = input("Enter your test URL: ")


chrome_path = 'utils/chromedriver.exe'
options = Options()
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
service = Service(chrome_path)
driver = webdriver.Chrome(service=service, options=options)


def sumbit():
    WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "userEnd"))
            ).click()
    time.sleep(0.3)
    WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "endAuth"))
        ).send_keys("CONFIRM")
    time.sleep(0.3)
    WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[@id='closeEnd']/div[2]/button[2]"))
        ).click()
    
def getAnswer():
    try:
        driver.get(testUrl)
        try:
            button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Start Test')]"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", button)
            button.click()
            print("Start Test button clicked.")
        except Exception as e:
            print("Start Test button click failed:", e)

        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "agreeButton"))
            ).click()
        except Exception as e:
            print("Agree button click failed:", e)

        time.sleep(7)
        page_source = driver.page_source
        scripts = re.findall(r'<script.*?>(.*?)</script>', page_source, re.DOTALL)

        pattern = re.compile(r'test_cases = (\[\[.*?\]\]);', re.DOTALL)
        match = pattern.search(scripts[19])

        if match:
            js_data = match.group(1)
            test_cases = json.loads(js_data)
            
            for i, question_test_cases in enumerate(test_cases):
                print(f"Question {i + 1}:")
                for j, test_case in enumerate(question_test_cases):
                    print(f"  Test Case {j + 1}:")
                    print(f"    Input: {test_case['input']}")
                    print(f"    Output: {test_case['output']}")
        else:
            print("Test cases not found")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return []
    except Exception as e:
        print(f"Error extracting answers: {e}")
        return []

def login():
    try:
        url = 'https://skcet.amypo.com/login'
        driver.get(url)
        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "acceptCookiesButton"))
            ).click()
            print("Cookie consent banner closed.")
        except Exception as e:
            print("No cookie consent banner found or could not be clicked:", e)

        email_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='Email']"))
        )
        email_input.send_keys(userId)

        password_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "input[placeholder='Password']"))
        )
        password_input.send_keys(password)

        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'bg-indigo-500')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", button)
        button.click()
        print("Login button clicked.")
    except Exception as e:
        print(f"Login process failed: {e}")




login()
time.sleep(2)
getAnswer()
driver.quit()
