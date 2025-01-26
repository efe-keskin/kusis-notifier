# KUSIS Grade Change Notifier

This project is a Python-based automation script that monitors course grades on KUSIS (Koç University's Student Information System) and sends email alerts if any changes are detected. The script also provides real-time audio notifications for detected changes. 
**For Personal Use Only!**

## Features

- **Automated Grade Monitoring**: Logs into KUSIS, scrapes grade information, and detects changes.
- **Email Notifications**: Sends detailed email alerts about any grade changes.
- **Audio Alerts**: Plays a beep sound when changes are detected.
- **Data Persistence**: Maintains a record of previously fetched grades to compare and detect updates.

## Prerequisites

To run this project, you need the following:

- **Python 3.8+**
- **Google Chrome** and **ChromeDriver**
- Required Python libraries:
  - `selenium`
  - `bs4` (BeautifulSoup)
  - `smtplib`
  - `winsound` (Windows only)

Install the required Python libraries using:
```bash
pip install selenium beautifulsoup4
```

## Setup Instructions

1. **Download ChromeDriver**:
   - Ensure the version of ChromeDriver matches your installed Chrome version.
   - Download ChromeDriver from [here](https://chromedriver.chromium.org/downloads).
   - Update the `PATH_TO_CHROMEDRIVER` in the script with the path to your ChromeDriver executable.

2. **Update Login Credentials**:
   - Replace `USERNAME` and `PASSWORD` in the script with your KUSIS login credentials.

3. **Configure Email Settings**:
   - Replace `SENDER_EMAIL` and `PASSWORD` with your email address and application password (for Gmail, you may need to generate an app password).
   - Set the `RECIPIENT_EMAIL` to the email address where you want to receive notifications.

4. **Run the Script**:
   Execute the script in your terminal or IDE:
   ```bash
   python kusis_notifier.py
   ```

## How It Works

1. The script logs into KUSIS and navigates to the grade history page.
2. It scrapes the course names and grades, storing them in a dictionary.
3. The grades are compared with a local file (`scraped_data.txt`) to detect changes.
4. If any changes are found:
   - The local file is updated with the new grades.
   - An email notification is sent detailing the changes.
   - An audio alert is played.
5. The script runs continuously, checking for updates every 15 minutes.

## Example Email Notification

**Subject**: KUSIS Course Grade Changed  
**Body**:
```
Changes detected:

Course COMP 132 changed from 'B' to 'A'
Course CHBI 300 changed from 'C' to 'B'

Check KUSIS for details.
```

## Notes

- The script is intended for personal use and requires storing your information in plaintext. Use it cautiously.
- Audio notifications (using `winsound`) work only on Windows. You can replace this with other alert mechanisms for cross-platform compatibility.
- Ensure you follow Koç University's acceptable use policies while using this script(KUSIS does not have a robots.txt at the time of upload[26.01.2025]).

