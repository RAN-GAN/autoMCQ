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



chrome_path = 'utils/chromedriver.exe'
options = Options()
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
service = Service(chrome_path)
driver = webdriver.Chrome(service=service, options=options)


def sumbit():
    time.sleep(25)
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
        page_source = driver.page_source
        scripts = re.findall(r'<script.*?>(.*?)</script>', page_source, re.DOTALL)
        match = re.search(r'mcq_questions\s*=\s*(\[\{.*?\}\])', scripts[8], re.DOTALL)
        
        if not match:
            print("No mcq_questions data found")
            return []

        questions_data = match.group(1)
        questions = json.loads(questions_data)

        answers = [question.get('optioncheck') for question in questions]
        return answers
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

def startTest():
    testUrl = input("Enter test url: " )
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
        answers = getAnswer()

        for i in range(1, 26):
            time.sleep(1)
            try:
                button_id = f"quiz{i}-codings"
                button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, button_id))
                )
                button.click()

                radio_inputs = driver.find_elements(By.XPATH, "//input[@type='radio']")
                radio_inputs[(i-1)*4+answers[i-1]-1].click() 

            except Exception as e:
                print(f"Error processing question {i}: {e}")

        time.sleep(1)
        sumbit()

    except Exception as e:
        print(f"Test process failed: {e}")





login()
time.sleep(2)
startTest()
driver.quit()

input("Press Enter to exit...")



