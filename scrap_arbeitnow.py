from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys


driver = webdriver.Firefox()

driver.get('https://www.arbeitnow.com')
username = driver.find_element(By.XPATH, "//input[@id='search_jobs_desktop']")
username.send_keys('django')
driver.find_element(By.XPATH, "//select[@name='search_sort_by']/option[text()='Newest']").click()
xpath_expression = "//ul[@id='results']/li"
advertisements = []

time.sleep(3)

list_items = driver.find_elements(By.XPATH, xpath_expression)

for item in list_items:
    link_element = item.find_element(By.XPATH, ".//a")
    link_url = link_element.get_attribute("href")
    link_text = link_element.get_attribute("aria-label")
    city = item.find_element(By.XPATH, ".//div[contains(@class, 'self-center')]/p")
    advertisment_datetime = item.find_element(By.XPATH, ".//div[contains(@class, 'self-center')]//time")
    advertisement_datetime = advertisment_datetime.get_attribute("datetime")
    advertisements.append({
        "city": city.text,
        "advertise_url": link_url,
        "advertisement_datetime": advertisement_datetime,
        "link_text": link_text
    })

for job_position in advertisements:
    driver.get(job_position['advertise_url'])
    print(job_position['advertise_url'])
    print(job_position['city'])
    print(job_position['advertisement_datetime'])
    time.sleep(3)
    advertise_title = driver.find_element(By.XPATH, "//div[@itemprop='description']")
    print(advertise_title.text)
    print('================================================================')
    break
    # driver.close()


# Close the browser window
# driver.quit()
