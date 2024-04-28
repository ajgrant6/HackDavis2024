from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_company_location_linkedin(url):
    try:
        options = Options()
        options.headless = True
        location = None

        # Try 3 times to find the element with class "topcard__flavor--bullet"
        for _ in range(5):
            try:
                driver = webdriver.Chrome(options=options)
                driver.get(url)

                location_span = WebDriverWait(driver, 2).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, "topcard__flavor--bullet"))
                )
                location = location_span.text.strip() if location_span else None
                break  # Exit the loop if the location is found

            except Exception as e:
                print("Attempt failed:", e)
                
            finally:
                if driver:
                    driver.quit()  # Close the WebDriver instance if it's open

        if not location:
            print("Maximum retries reached. Element not found.")

        return location

    except Exception as e:
        print("An error occurred:", e)
        return None
    



def get_company_location_indeed(url):
    try:
        options = Options()
        options.headless = True
        location = None

        # Try 3 times to find the element with data-testid "job-location"
        for _ in range(3):
            try:
                driver = webdriver.Chrome(options=options)
                driver.get(url)

                # Try finding the location using data-testid "job-location"
                try:
                    location_div = WebDriverWait(driver, 2).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="job-location"]'))
                    )
                    location = location_div.text.strip() if location_div else None
                except:
                    # If not found, try finding the location using data-testid "inlineHeader-companyLocation"
                    location_div = WebDriverWait(driver, 2).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, '[data-testid="inlineHeader-companyLocation"]'))
                    )
                    location = location_div.text.strip() if location_div else None

                if location:
                    break  # Exit the loop if the location is found

            except Exception as e:
                print("Attempt failed:", e)
                
            finally:
                if driver:
                    driver.quit()

        if not location:
            print("Maximum retries reached. Element not found.")

        return location

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


# Example usage
# url = "https://www.linkedin.com/jobs/view/3911217559"
# company_location = get_company_location(url)
# if company_location:
#     print("Company location:", company_location)
# else:
#     print("Location information not found.")


# indeed
#linkedin
#glassdoor
while True:
    url = input("Enter a job listing URL (or 'q' to quit): ")
    if url == 'q':
        break
    
    company_location = parse_url(url)
    print(url)

    if company_location:
        print("Company location:", company_location)
    else:
        print("Location information not found.")

def get_location(url):
    if company_location:
        return company_location
    else:
        return "Location information not found."

