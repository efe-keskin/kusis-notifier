import time
import smtplib
import winsound
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def check_website_and_alert():
    service = Service("PATH_TO_CHROMEDRIVER")
    chrome_options = Options()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 10)

    login_url = "https://kusis.ku.edu.tr/psp/ps/?cmd=login&languageCd=ENG&"
    driver.get(login_url)

    try:
        english_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "English"))
        )
        english_link.click()
        time.sleep(2)
    except Exception as e:
        print("Could not find or click the English link:", e)

    try:
        email_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "i0116"))
        )
        email_field.send_keys("YOUR_EMAIL_HERE")
        email_field.send_keys(Keys.ENTER)

        password_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "i0118"))
        )
        password_field.send_keys("YOUR_PASSWORD_HERE")
        password_field.send_keys(Keys.ENTER)

        yes_field = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "idSIButton9"))
        )
        yes_field.click()
    except Exception as e:
        print("Error during login process:", e)
        driver.quit()
        return

    time.sleep(5)
    driver.get("https://kusis.ku.edu.tr/psp/ps/EMPLOYEE/SA/c/SA_LEARNER_SERVICES.SSS_MY_CRSEHIST.GBL")
    time.sleep(5)

    try:
        driver.switch_to.frame("ptifrmtgtframe")
    except Exception as e:
        print("iFrame error:", e)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    rows = soup.select('tr[id^="trCRSE_HIST"]')

    new_data_dict = {
        row.select_one('span[id^="CRSE_NAME"]').get_text(strip=True):
            row.select_one('span[id^="CRSE_GRADE"]').get_text(strip=True)
        for row in rows if row.select_one('span[id^="CRSE_NAME"]')
    }

    driver.quit()

    file_path = "scraped_data.txt"
    old_data_dict = {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            old_data_dict = dict(line.strip().split(":") for line in f if line.strip())
    except FileNotFoundError:
        pass

    changed_courses = [
        (course, old_data_dict.get(course, ""), grade)
        for course, grade in new_data_dict.items()
        if old_data_dict.get(course, "") != grade
    ]

    if changed_courses:
        with open(file_path, "w", encoding="utf-8") as f:
            for course, grade in new_data_dict.items():
                f.write(f"{course}:{grade}\n")

        body = "\n".join([
            f"{course} changed from '{old}' to '{new}'"
            for course, old, new in changed_courses
        ])

        send_email("KUSIS Course Grade Changed",
                   f"Changes detected:\n\n{body}\n\nCheck KUSIS for details.")

        winsound.Beep(1000, 1000)
    else:
        print("No changes detected.")


def send_email(subject, body):
    sender_email = "SENDER_EMAIL"
    password = "SENDER_PASSWORD"  # I recommend you use application of 2FA password
    recipient = "RECIPIENT_EMAIL"

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
