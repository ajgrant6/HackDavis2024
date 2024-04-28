from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_company_job_description_linkedin(url):
    try:
        options = Options()
        options.headless = True
        job_description = None

        # Try 3 times to find the element with class "description__text"
        for _ in range(5):
            try:
                driver = webdriver.Chrome(options=options)
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
                # print("Attempt failed:", e)
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
        options = Options()
        options.headless = True
        job_description = None

        # Try 3 times to find the element with class "jobsearch-jobDescriptionText"
        for _ in range(5):
            try:
                driver = webdriver.Chrome(options=options)
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
    
# Run if this is the main module
if __name__ == "__main__":
    # url = "https://www.linkedin.com/jobs/search?trk=guest_homepage-basic_guest_nav_menu_jobs&original_referer=https%3A%2F%2Fwww.linkedin.com%2F%3Ftrk%3Dguest_homepage-basic_nav-header-logo&currentJobId=3912685323&position=2&pageNum=0"
    # print(get_company_job_description_linkedin(url))

    url = "https://www.indeed.com/q-business-analyst-jobs.html?vjk=443cb2513ce0ebb7"
    print(get_company_job_description_indeed(url))