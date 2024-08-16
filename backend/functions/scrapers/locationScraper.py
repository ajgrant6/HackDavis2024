from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup
import time
import sys

def configure_chrome_driver():
    options = Options()
    options.headless = True  # Run Chrome in headless mode
    options.add_argument("--no-sandbox")  # Bypass OS security model
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    options.add_argument("--disable-gpu")  # Applicable in headless mode, especially for environments without a GPU
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-infobars")
    options.add_argument("--remote-debugging-port=9222")  # Allow remote debugging if needed
    options.add_argument("--start-maximized")  # Start maximized (helps avoid issues with rendering)
    options.add_argument("--disable-software-rasterizer")  # Use CPU for rendering
    options.add_argument("--window-size=1920,1080")  # Set window size to a reasonable default

    # Initialize Chrome WebDriver
    driver = webdriver.Chrome(service=Service('/usr/local/bin/chromedriver'), options=options)
    return driver

#! Selenium approach
# def get_company_location_linkedin(url):
#     try:
#         location = None

#         # Try 5 times to find the element with class "topcard__flavor--bullet"
#         for _ in range(5):
#             driver = None
#             try:
#                 driver = configure_chrome_driver()
#                 driver.get(url)

#                 location_span = WebDriverWait(driver, 2).until(
#                     EC.visibility_of_element_located((By.CLASS_NAME, "topcard__flavor--bullet"))
#                 )
#                 location = location_span.text.strip() if location_span else None
#                 break  # Exit the loop if the location is found

#             except Exception as e:
#                 print("Attempt failed:", e)
                
#             finally:
#                 if driver:
#                     driver.quit()  # Close the WebDriver instance if it's open

#         if not location:
#             print("Maximum retries reached. Element not found.")

#         return location

#     except Exception as e:
#         print("An error occurred:", e)
#         return None

#! BeautifulSoup approach
def get_company_location_linkedin(url):
    try:
        location = None

        # Try 5 times to fetch the location element from the page
        for _ in range(5):
            try:
                # Fetch the HTML content of the page
                response = requests.get(url)
                response.raise_for_status()  # Raise an error for bad status codes

                # Parse the HTML content using BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')

                # Find the element with class "topcard__flavor--bullet"
                location_span = soup.find(class_="topcard__flavor--bullet")
                if location_span:
                    location = location_span.get_text(strip=True)
                    break  # Exit the loop if the location is found

            except Exception as e:
                print("Attempt failed:", e)
                time.sleep(2)  # Wait for 2 seconds before retrying

        if not location:
            print("Maximum retries reached. Element not found.", file=sys.stderr)

        return location

    except Exception as e:
        print("An error occurred:", e, file=sys.stderr)
        return None

#! Selenium approach
# def get_company_location_indeed(url):
#     try:
#         location = None

#         # Try 3 times to find the element with data-testid "job-location"
#         for _ in range(3):
#             driver = None
#             try:
#                 driver = configure_chrome_driver()
#                 driver.get(url)

#                 # Try finding the location using data-testid "job-location"
#                 try:
#                     location_div = WebDriverWait(driver, 2).until(
#                         EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="job-location"]'))
#                     )
#                     location = location_div.text.strip() if location_div else None
#                 except:
#                     # If not found, try finding the location using data-testid "inlineHeader-companyLocation"
#                     location_div = WebDriverWait(driver, 2).until(
#                         EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="inlineHeader-companyLocation"]'))
#                     )
#                     location = location_div.text.strip() if location_div else None

#                 if location:
#                     break  # Exit the loop if the location is found

#             except Exception as e:
#                 print("Attempt failed:", e, file=sys.stderr)
                
#             finally:
#                 if driver:
#                     driver.quit()

#         if not location:
#             print("Maximum retries reached. Element not found.", file=sys.stderr)

#         return location

#     except Exception as e:
#         print("An error occurred:", e, file=sys.stderr)
#         return None

#! BeautifulSoup approach
def get_company_location_indeed(url):
    try:
        location = None

        # Try 3 times to find the element with data-testid "job-location" or "inlineHeader-companyLocation"
        for _ in range(3):
            try:
                # Fetch the HTML content of the page
                response = requests.get(url)
                response.raise_for_status()  # Raise an error for bad status codes

                # Parse the HTML content using BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')

                # Try finding the location using data-testid="job-location"
                location_div = soup.select_one('[data-testid="job-location"]')

                # If not found, try finding the location using data-testid="inlineHeader-companyLocation"
                if not location_div:
                    location_div = soup.select_one('[data-testid="inlineHeader-companyLocation"]')

                if location_div:
                    location = location_div.get_text(strip=True)
                    break  # Exit the loop if the location is found

            except Exception as e:
                print("Attempt failed:", e)
                time.sleep(2)  # Wait for 2 seconds before retrying

        if not location:
            print("Maximum retries reached. Element not found.", file=sys.stderr)

        return location

    except Exception as e:
        print("An error occurred:", e, file=sys.stderr)
        return None

def parse_url(url):
    if "linkedin.com" in url:
        if "linkedin.com/jobs/view/" in url:
            new_url = url
        else:
            job_id = url.split("currentJobId=")[1].split("&")[0]
            new_url = "https://www.linkedin.com/jobs/view/" + job_id

        return get_company_location_linkedin(new_url)
    
    elif "indeed.com" in url:
        if "indeed.com/viewjob?jk=" in url:
            new_url = url
        else:
            job_id = url.split("jk=")[1].split("&")[0]
            new_url = "https://www.indeed.com/viewjob?jk=" + job_id
        return get_company_location_indeed(new_url)
    else:
        print("Invalid URL. Please enter a LinkedIn job listing URL.")  
        return None

def get_location(url):
    company_location = parse_url(url)
    if company_location:
        return company_location
    else:
        return "not found"
