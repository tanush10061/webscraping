from selenium import webdriver
from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import csv
import logging
import time

# Configuration
BASE_URL = "https://scraping-trial-test.vercel.app/search"
DEFAULT_SEARCH_TERM = "LLC"
WAIT_TIME = 15
PAGINATION_WAIT_TIME = 5

# Logging setup
logging.basicConfig(
    filename="scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Browser setup
driver = webdriver.Firefox(service=Service())
driver.maximize_window()

try:
    # Open site and wait for CAPTCHA
    driver.get(BASE_URL)
    input("Solve the CAPTCHA manually, then press ENTER here...")

    # Search input with validation
    search_input = driver.find_element(By.TAG_NAME, "input")

    while True:
        search_term = input(
            f"Enter search term (min 3 chars) [default: {DEFAULT_SEARCH_TERM}]: "
        ).strip()

        if not search_term:
            search_term = DEFAULT_SEARCH_TERM
            break

        if len(search_term) < 3:
            print("Search term must be at least 3 characters.")
            continue

        break

    search_input.send_keys(search_term)
    driver.find_element(By.TAG_NAME, "button").click()

    # Wait for first results page
    WebDriverWait(driver, WAIT_TIME).until(
        EC.presence_of_element_located(
            (By.XPATH, "//a[contains(@href, '/business/')]")
        )
    )

    all_records = []

    # Pagination loop
    while True:
        # Collect unique business profile URLs on the current page
        links = driver.find_elements(By.XPATH, "//a[contains(@href, '/business/')]")
        business_urls = list({link.get_attribute("href") for link in links})

        for url in business_urls:
            try:
                # Open business profile in a new tab
                driver.execute_script("window.open(arguments[0]);", url)
                driver.switch_to.window(driver.window_handles[1])

                # Wait for Business Profile section
                WebDriverWait(driver, PAGINATION_WAIT_TIME).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//div[text()='Business Profile']")
                    )
                )

                # Extract business details
                business_name = driver.find_element(By.XPATH, "//h2").text

                meta = driver.find_element(
                    By.XPATH,
                    "//div[contains(@class,'small') and contains(text(),'Registration')]"
                ).text
                registration_id = meta.split(" - ")[0].replace("Registration ", "").strip()

                status = driver.find_element(
                    By.XPATH, "//span[contains(@class,'status')]"
                ).text

                filing_date = driver.find_element(
                    By.XPATH, "//div[text()='Filing Date']/following-sibling::div"
                ).text

                agent_name = driver.find_element(
                    By.XPATH, "//div[text()='Registered Agent']/following-sibling::div[1]"
                ).text

                agent_address = driver.find_element(
                    By.XPATH, "//div[text()='Registered Agent']/following-sibling::div[contains(@class,'small')]"
                ).text

                try:
                    agent_email = driver.find_element(By.XPATH, "//code").text
                except NoSuchElementException:
                    agent_email = ""

                all_records.append({
                    "business_name": business_name,
                    "registration_id": registration_id,
                    "status": status,
                    "filing_date": filing_date,
                    "agent_name": agent_name,
                    "agent_address": agent_address,
                    "agent_email": agent_email
                })

                # Close profile tab and return to results
                driver.close()
                driver.switch_to.window(driver.window_handles[0])

                # Polite delay to reduce load and CAPTCHA risk
                time.sleep(0.2)

            except Exception as e:
                logging.error(f"Failed to scrape {url}: {e}")
                if len(driver.window_handles) > 1:
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])

        # Pagination handling
        try:
            current_page = driver.find_element(
                By.CSS_SELECTOR,
                ".table-meta .small.muted:last-child"
            ).text
        except NoSuchElementException:
            break

        next_buttons = driver.find_elements(By.XPATH, "//button[text()='Next']")
        if not next_buttons:
            break

        next_buttons[0].click()

        try:
            WebDriverWait(driver, PAGINATION_WAIT_TIME).until(
                lambda d: d.find_element(
                    By.CSS_SELECTOR,
                    ".table-meta .small.muted:last-child"
                ).text != current_page
            )
        except TimeoutException:
            break

    # Save JSON output
    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(all_records, f, indent=2)

    # Save CSV output
    with open("output.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "business_name",
                "registration_id",
                "status",
                "filing_date",
                "agent_name",
                "agent_address",
                "agent_email"
            ]
        )
        writer.writeheader()
        writer.writerows(all_records)

    print(f"Done. Scraped {len(all_records)} records.")
    logging.info(f"Scraped {len(all_records)} records.")

finally:
    driver.quit()