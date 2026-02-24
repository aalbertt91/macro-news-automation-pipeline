# Macro News Automation Pipeline (Federal Reserve XML → Excel → Email)

## Project Objective

This project automates the extraction, transformation, and reporting of macroeconomic news releases from the official Federal Reserve XML feed. The system retrieves the latest press releases, parses structured XML data, transforms it into a clean tabular format using Pandas, generates an Excel report, and automatically delivers the report via email. The objective is to simulate a lightweight macro monitoring pipeline similar to workflows used by research, macro strategy, and investment teams that track high-impact central bank announcements.

## Technologies Used

**Python:** Core programming language used for orchestration and automation.

**Requests:** Retrieves structured XML data from the Federal Reserve’s official feed.

**ElementTree (XML):** Parses and extracts relevant fields from XML items.

**Pandas:** Structures and transforms raw XML data into a clean DataFrame.

**Openpyxl:** Generates Excel reports for structured news tracking.

**Smtplib** / EmailMessage: Handles secure automated email delivery with attachment.

**Dotenv:** Manages sensitive email credentials via environment variables.

**Logging:** Tracks execution flow and captures runtime errors.

## How to Run

1. Ensure the required Python libraries are installed:

pip install -r requirements.txt

2. Create a .env file in the project root:

SENDER_EMAIL=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
RECEIVER_EMAIL=receiver_email@gmail.com

3. Run the script:

python src/news_report_bot.py

4. After execution, check the /reports directory for the generated Excel file, confirm successful email delivery in the terminal output

## Why This Is Valuable for a Hedge Fund

- Automates monitoring of Federal Reserve press releases and policy communications

- Demonstrates structured XML ingestion and transformation workflow

- Builds a clean reporting pipeline (data → transformation → Excel → email)

- Reduces manual macro news tracking effort

- Simulates operational tooling used in macro, research, and strategy teams

- Provides a scalable foundation for multi-source news aggregation
