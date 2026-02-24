# Standard library imports
import os
import logging
from pathlib import Path
import smtplib
from email.message import EmailMessage

# Third-party libraries
import requests
import xml.etree.ElementTree as ET
import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv(
    dotenv_path="/home/runner/workspace/web_scraper_report_generator/.env",
    override=True)

# Read email credentials
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
APP_PASSWORD = os.getenv("EMAIL_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# Validate required environment variables
if not SENDER_EMAIL or not APP_PASSWORD or not RECEIVER_EMAIL:
  logging.error(
      "Missing .env variables. Check: SENDER_EMAIL, EMAIL_PASSWORD, RECEIVER_EMAIL"
  )
  exit(1)

# commit : project setup with requirements gitignore and environment template

# Federal Reserve XML feed URL
url = "https://www.federalreserve.gov/feeds/press_all.xml"

# Fetch XML feed with timeout
try:
  response = requests.get(url, timeout=15)
except Exception as e:
  logging.error(f"Request failed: {e}")
  exit(1)

# Check HTTP response
if response.status_code == 200:
  # Parse XML content
  try:
    root = ET.fromstring(response.content)
  except Exception as e:
    logging.error(f"XML parse failed: {e}")
    exit(1)

  # Store parsed news items
  news_list = []

  # Extract top 10 items from feed
  try:
    for item in root.findall('.//item'):
      news_data = {
          'title': item.find('title').text,
          'link': item.find('link').text,
          'guid': item.find('guid').text,
          'description': item.find('description').text,
          'category': item.find('category').text,
          'pubDate': item.find('pubDate').text,
      }

      news_list.append(news_data)

      if len(news_list) == 10:
        break
  except Exception as e:
    logging.error(f"Item extraction failed: {e}")
    exit(1)

else:
  logging.error(f"Connection error: {response.status_code}")
  exit(1)

#commit: implement Fed XML feed fetch and parsing logic

# Convert data to DataFrame
try:
  df = pd.DataFrame(news_list)
except Exception as e:
  logging.error(f"DataFrame creation failed: {e}")
  exit(1)

print(df)

#commit: map Fed XML items to structured dataframe schema

# Export DataFrame to Excel
try:
  df.to_excel("web_scraper_report_generator/reports/fed_news.xlsx",
              index=False)
except Exception as e:
  logging.error(f"Excel export failed: {e}")
  exit(1)

# commit: generate Excel report from Fed dataframe

# EMAIL SENDING
# SMTP configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

EXCEL_PATH = "web_scraper_report_generator/reports/fed_news.xlsx"

# Create email message
try:
  msg = EmailMessage()
  msg["From"] = SENDER_EMAIL
  msg["To"] = RECEIVER_EMAIL
  msg["Subject"] = "Fed Press Releases – Latest 10 Updates"

  msg.set_content("""
Hi,

Please find attached the latest Federal Reserve press releases report.

The attached Excel file includes the 10 most recent items from the Fed’s official XML feed, including publication date, category, title, link, and description.

Best regards,
Alper
""")
except Exception as e:
  logging.error(f"Email message creation failed: {e}")
  exit(1)

# Attach Excel file
file_path = Path(EXCEL_PATH)

try:
  with open(file_path, "rb") as f:
    msg.add_attachment(
        f.read(),
        maintype="application",
        subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=file_path.name)
except Exception as e:
  logging.error(f"Attachment failed: {e}")
  exit(1)

# Send email via SMTP
try:
  with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
    server.starttls()
    server.login(SENDER_EMAIL, APP_PASSWORD)
    server.send_message(msg)
except Exception as e:
  logging.error(f"Email sending failed: {e}")
  exit(1)

print("📧 Email sent successfully!")

# commit: add automated email delivery with Excel attachment