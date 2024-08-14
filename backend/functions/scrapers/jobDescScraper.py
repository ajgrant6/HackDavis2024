from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

def get_company_job_description_linkedin(url):
    try:
        job_description = None

        # Try 5 times to find the element with class "description__text"
        for _ in range(5):
            driver = None
            try:
                driver = configure_chrome_driver()
                driver.get(url)

                # Click the "Show more" button
                show_more_button = WebDriverWait(driver, 2).until(
                    EC.visibility_of_element_located((By.XPATH, "//button[@aria-label='i18n_show_more']"))
                )
                show_more_button.click()

                job_description_div = WebDriverWait(driver, 2).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, "description__text"))
                )
                job_description = job_description_div.text.strip() if job_description_div else None
                break 

            except Exception as e:
                print("Attempt failed:", e)
                pass

            finally:
                if driver:
                    driver.quit()

        if not job_description:
            print("Maximum retries reached. Element not found.")
            job_description = "No job description found."

        # Remove "Show less" from the end of the description
        job_description = job_description.replace("Show less", "")
        return job_description

    except Exception as e:
        print("An error occurred:", e)
        return None
    

def get_company_job_description_indeed(url):
    try:
        job_description = None

        # Try 5 times to find the element with id "jobDescriptionText"
        for _ in range(5):
            driver = None
            try:
                driver = configure_chrome_driver()
                driver.get(url)

                job_description_div = WebDriverWait(driver, 2).until(
                    EC.visibility_of_element_located((By.ID, "jobDescriptionText"))
                )
                job_description = job_description_div.text.strip() if job_description_div else None
                break

            except Exception as e:
                print("Attempt failed:", e)

            finally:
                if driver:
                    driver.quit()

        if not job_description:
            print("Maximum retries reached. Element not found.")
            job_description = "No job description found."

        return job_description

    except Exception as e:
        print("An error occurred:", e)
        return None

def parse_url(url):
    if "linkedin.com" in url:
        if "linkedin.com/jobs/view/" in url:
            new_url = url
        else:
            job_id = url.split("currentJobId=")[1].split("&")[0]
            new_url = "https://www.linkedin.com/jobs/view/" + job_id

        return get_company_job_description_linkedin(new_url)
    
    elif "indeed.com" in url:
        if "indeed.com/viewjob?jk=" in url:
            new_url = url
        else:
            job_id = url.split("jk=")[1].split("&")[0]
            new_url = "https://www.indeed.com/viewjob?jk=" + job_id
        return get_company_job_description_indeed(new_url)
    else:
        print("Invalid URL. Please enter a LinkedIn job listing URL.")  
        return None

def get_job_description(url):
    job_description = parse_url(url)

    if job_description:
        return job_description
    else:
        return "not found"
