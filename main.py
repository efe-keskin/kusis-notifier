import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
import smtplib
import winsound

def check_website_and_alert():
    """
    Checks course grades on KUSIS and sends email alerts if changes are detected.
    """
    service = Service("PATH_TO_CHROMEDRIVER")
    chrome_options = Options()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 10)

    try:
        driver.get("https://kusis.ku.edu.tr/psp/ps/?cmd=login&languageCd=ENG&")
        username_field = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#login__username")))
        password_field = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "#login__password")))
        username_field.send_keys("USERNAME")
        password_field.send_keys("PASSWORD")
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'input[name="Submit"]'))).click()
        time.sleep(5)
    except Exception as e:
        print("Login error:", e)
        driver.quit()
        return

    driver.get("https://kusis.ku.edu.tr/psp/ps/EMPLOYEE/SA/c/SA_LEARNER_SERVICES.SSS_MY_CRSEHIST.GBL")
    time.sleep(5)

    try:
        driver.switch_to.frame("ptifrmtgtframe")
    except Exception as e:
        print("iFrame error:", e)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    rows = soup.select('tr[id^="trCRSE_HIST"]')
    new_data_dict = {row.select_one('span[id^="CRSE_NAME"]').get_text(strip=True): row.select_one('span[id^="CRSE_GRADE"]').get_text(strip=True) for row in rows if row.select_one('span[id^="CRSE_NAME"]')}
    driver.quit()

    file_path = "scraped_data.txt"
    old_data_dict = {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            old_data_dict = dict(line.strip().split(":") for line in f if line.strip())
    except FileNotFoundError:
        pass

    changed_courses = [(course, old_data_dict.get(course, ""), grade) for course, grade in new_data_dict.items() if old_data_dict.get(course, "") != grade]

    if changed_courses:
        with open(file_path, "w", encoding="utf-8") as f:
            for course, grade in new_data_dict.items():
                f.write(f"{course}:{grade}\n")

        body = "\n".join([f"{course} changed from '{old}' to '{new}'" for course, old, new in changed_courses])
        send_email("KUSIS Course Grade Changed", f"Changes detected:\n\n{body}\n\nCheck KUSIS for details.")

        winsound.Beep(1000, 1000)
    else:
        print("No changes detected.")

def send_email(subject, body):
    """
    Sends email alerts using SMTP.
    """
    sender_email = "SENDER_EMAIL"
    password = "PASSWORD" #I recommend you use application password
    recipient = "RESCIPIENT_EMAIL"

    msg = MIMEMultipart()
    msg['From'] = "KUSIS Bot <robot@kusis.com>"
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, recipient, msg.as_string())
    print("Email sent.")

if __name__ == "__main__":
    while True:
        check_website_and_alert()
        time.sleep(15 * 60)
