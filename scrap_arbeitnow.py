from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time, json
from selenium.webdriver.common.keys import Keys
import requests
from django.conf import settings

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
    company = item.find_element(By.XPATH, ".//a[@itemprop='hiringOrganization']")
    link_url = link_element.get_attribute("href")
    link_text = link_element.get_attribute("aria-label")
    title = item.find_element(By.XPATH, ".//h2")
    city = item.find_element(By.XPATH, ".//div[contains(@class, 'self-center')]/p")
    advertisement_datetime = item.find_element(By.XPATH, ".//div[contains(@class, 'self-center')]//time")
    datetime = advertisement_datetime.get_attribute("datetime")
    advertisements.append({
        "title": title.text,
        "company": company.text,
        "city": city.text,
        "advertise_url": link_url,
        "datetime": datetime,
        "link_text": link_text
    })

for job_position in advertisements:
    driver.get(job_position['advertise_url'])
    time.sleep(3)
    advertise_title = driver.find_element(By.XPATH, "//div[@itemprop='description']")
    job_position["content"] = advertise_title.text
    payload = job_position

    print(payload)
    json_data = json.dumps(payload)
    headers = {'content-type':'application/json', 'charset':'UTF-8'}
    r = requests.post(F'{settings.ELASTICSEARCH_HOST}/arbeitnow/_doc', data=json_data, headers=headers)
    print('================================================================')

    # driver.close()

# Close the browser window
# driver.quit()
