from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys


# Replace 'your_driver_path' with the actual path to your webdriver executable
# For example, if you are using Chrome, you need to download chromedriver: https://sites.google.com/chromium.org/driver/
driver = webdriver.Firefox()

# Replace 'your_url' with the actual URL where your HTML is located
driver.get('https://www.arbeitnow.com')
username = driver.find_element(By.XPATH, "//input[@id='search_jobs_desktop']")
username.send_keys('django')
driver.find_element(By.XPATH, "//select[@name='search_sort_by']/option[text()='Newest']").click()
# Define the XPath to select all <li> elements within the <ul> element
xpath_expression = "//ul[@id='results']/li"
advertisements = []

time.sleep(3) #sleep for 1 sec

# Use find_elements_by_xpath to get a list of all matching elements
list_items = driver.find_elements(By.XPATH, xpath_expression)

# Iterate through the list_items and extract relevant information
for item in list_items:
    # Example: Extracting the href attribute from the first <a> element within each <li>
    link_element = item.find_element(By.XPATH, ".//a")
    link_url = link_element.get_attribute("href")
    link_text = link_element.get_attribute("aria-label")
    city = item.find_element(By.XPATH, ".//div[contains(@class, 'self-center')]/p")
    advertisment_datetime = item.find_element(By.XPATH, ".//div[contains(@class, 'self-center')]//time")
    advertisement_datetime = advertisment_datetime.text
    advertisements.append({
        "city": city.text,
        "advertise_url": link_url,
        "advertisement_datetime": advertisement_datetime,
        "link_text": link_text
    })

for job_position in advertisements:
    driver.get(job_position['advertise_url'])
    print(job_position['advertise_url'])
    time.sleep(3)
    advertise_title = driver.find_element(By.XPATH, "//div[@itemprop='description']")
    print(advertise_title.text)
    print('================================================================')
    # driver.close()


# Close the browser window
# driver.quit()
