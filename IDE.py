from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium import webdriver
import pyautogui
import random
import time
import json
import re

print('---------------------------------------------------------------\n')
print('get the test url before entering the credentials!\n')
print('---------------------------------------------------------------\n')

# userId = input("Enter your mailId: ")
userId = '727723euci035@skcet.ac.in'
# password = input("Enter your password: ")
password = 'skcet@2024'

testUrl = 'https://skcet.amypo.com/testpage?course=eyJpdiI6IlFVLysxaTRUWDNpTHIvQzZvbFh1L2c9PSIsInZhbHVlIjoiNTgzaHlpY3BvSDg2b0grS3Z1OS9MUT09IiwibWFjIjoiOWI2OTY0ZjM2ZGQyMmQyM2I4MjFlOTYwOWFkYWYxMzkwMDc0ZmZhYWNjNDZkYjFhNWQwMzIyNjVkN2QyODdhMCIsInRhZyI6IiJ9&topic=eyJpdiI6InNxVE9uem9tVVlCdGhBRnhDcjJqU2c9PSIsInZhbHVlIjoiNmJEcU9SMmFzbUJZRUU2RTZpQUZYZz09IiwibWFjIjoiMzU2Y2RmOTI4ZGYyZTFmZmMyYzFhZDAzMDc5ZDliYmQyMzlhNDAxNzk5OTRlMTE4NTI2MzUzMzc0YTNkYmU2YiIsInRhZyI6IiJ9&subtopic=eyJpdiI6IkpGcUd6QUZYZGFjbDE1MnY2WS94VWc9PSIsInZhbHVlIjoiWW9VSzcwSmhkVm1PYjNJc2s5NG56Zz09IiwibWFjIjoiNDYyMDFmOWM3ZTMxZWY0N2ZhOTJiYjlhMzQ0NGU5ODNhNmY1MjllOTZhMjJmNWI5NTZiY2Q4YTllYmNjMWJmZCIsInRhZyI6IiJ9&type=eyJpdiI6IjRuUnI1ZVpSUU9iL0VYaVlTZkZaeUE9PSIsInZhbHVlIjoicUFVME1tZzdCRUdPaStaNVZPSTlsZz09IiwibWFjIjoiZTU5MDQxZGE5NDg2ZTcxYWU5ZTJjYWU4OGU0MDA4MjRkMjM2Mjk1N2Y4YTFkMTJkMTVjMWZiM2Y2OTZhMTIyOCIsInRhZyI6IiJ9&mode=eyJpdiI6IndjRTZKdkxVRkMxV0Z5RXh1Tjh5Ymc9PSIsInZhbHVlIjoiaHBDV2c4VXcxY2FPcjU0V0JMdUNaUT09IiwibWFjIjoiOGQzMzI0OTA5OGVjYzBjMzhmODQwYWM2NDY4NzAyYTU0MTFhN2Q2OTIwODQ2MDcyMWQxYWQ2NzI4NTMzNjE5ZCIsInRhZyI6IiJ9'

chrome_path = 'utils/chromedriver.exe'
options = Options()
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
service = Service(chrome_path)
driver = webdriver.Chrome(service=service, options=options)


def sumbit():
    time.sleep(20)
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
        match = re.search(r'ide_questions\s*=\s*(\[\{.*?\}\])', scripts[19], re.DOTALL)
        
        if not match:
            print("No IDE_questions data found")
            return []

        questions_data = match.group(1)
        questions = json.loads(questions_data)

        answers = [question.get('solution') for question in questions]
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
        print(answers)
        for i in range(1,6):
            if i==1 or i==2 or i==3 or i==5:
                pass
            else:
                time.sleep(1)
                try:
                    button_id = f"editor{i}-codings"
                    button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.ID, button_id))
                    )
                    button.click()
                    time.sleep(3)
                    print(answers[i-1])
                    main(answers[i-1])

                    runButton = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.ID, f'editor{i}-run'))
                    )
                    runButton.click()
                    time.sleep(10)
                    verifyButton = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.ID, f'editor{i}-compile'))
                    )
                    verifyButton.click()
                    
                    time.sleep(10)
                    submitButton = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.ID, f'editor{i}-submit'))
                    )
                    submitButton.click()
                    time.sleep(10)


                except Exception as e:
                    print(f"Error processing question {i}: {e}")

        time.sleep(1)
        sumbit()
        i+=1

    except Exception as e:
        print(f"Test process failed: {e}")



def main(answer):
    time.sleep(1)
    pyautogui.moveTo(1400,450);
    time.sleep(0.1)
    pyautogui.click();
    time.sleep(0.1)
    pyautogui.press('enter');
    time.sleep(0.1)

    def type_code(code):
        remove_indent = True
        dont_close_brackets = True
        string  = code
        try:
            x=0
            if remove_indent:
                string = '\n'.join(list(map(str.strip, string.split('\n'))))
            if dont_close_brackets:
                for i in string:
                    x+=1
                    if x%4==0:
                        time.sleep(0.076)
                    if i in [')', ']']:
                        # pyautogui.typewrite(i)
                        time.sleep(0.008)
                    if i == '}':
                        pyautogui.press('down')
                    else:
                        if(i=='\n'):
                            pyautogui.typewrite(i)
                            time.sleep(0.02)
                        else:
                            time.sleep(0.008)
                            pyautogui.typewrite(i)
                
            for _ in range(500):
                pyautogui.press('delete')

            print("Successfully Power Pasted")
        except pyautogui.FailSafeException as e:
            print("Stopped Power Pasting |", e)


    type_code(answer.strip())
    time.sleep(10)


login()
time.sleep(2)
startTest()
input("Press Enter to exit...")