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
