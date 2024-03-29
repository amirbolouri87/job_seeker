from collect_data.arbeitnow.collect_data import ICollectBySelenium
from selenium.webdriver.common.by import By
import time, json
import requests
from django.conf import settings
from django.core.cache import cache


class CollectArbeitnow(ICollectBySelenium):

    def _set_search_data(self):
        search_job = self.driver.find_element(By.XPATH, "//input[@id='search_jobs_desktop']")
        search_job.send_keys(self.search_keyword)
        time.sleep(5)

    def _collect_list_data(self):
        self.driver.find_element(By.XPATH, "//select[@name='search_sort_by']/option[text()='Newest']").click()
        xpath_expression = "//ul[@id='results']/li"
        time.sleep(3)
        self.list_items = self.driver.find_elements(By.XPATH, xpath_expression)

    def _collect_data_detail(self):
        for item in self.list_items:
            link_element = item.find_element(By.XPATH, ".//a")
            company = item.find_element(By.XPATH, ".//a[@itemprop='hiringOrganization']")
            link_url = link_element.get_attribute("href")
            link_text = link_element.get_attribute("aria-label")
            title = item.find_element(By.XPATH, ".//h2")
            city = item.find_element(By.XPATH, ".//div[contains(@class, 'self-center')]/p")
            advertisement_datetime = item.find_element(By.XPATH, ".//div[contains(@class, 'self-center')]//time")
            datetime = advertisement_datetime.get_attribute("datetime")

            self.advertisements.append({
                "title": title.text,
                "company": company.text,
                "city": city.text,
                "advertise_url": link_url,
                "datetime": datetime,
                "link_text": link_text
            })

    def _complete_advertisement(self):
        for job_position in self.advertisements:
            self.driver.get(job_position['advertise_url'])
            time.sleep(3)
            advertise_title = self.driver.find_element(By.XPATH, "//div[@itemprop='description']")
            job_position["content"] = advertise_title.text
            job_position["is_translate"] = False
            job_position['pk'] = job_position['advertise_url'].split('/')[-1] if job_position['advertise_url'] else None
            last_url = cache.get('last_url_arbeitnow')
            print('check advertise_url= ', job_position['advertise_url'])
            print('check last_url= ', last_url)
            if last_url == job_position['advertise_url']:
                print('breaked advertisement >>>>', last_url)
                break
            self.payload.append(job_position)
            # print(job_position)

    def _insert_collect_data(self):
        for job_position in self.payload:
            json_data = json.dumps(job_position)
            headers = {'content-type': 'application/json', 'charset': 'UTF-8'}
            r = requests.post(F'{settings.ELASTICSEARCH_HOST}/arbeitnow/_doc/{job_position["pk"]}', data=json_data, headers=headers)
            # print('================================================================')

        if self.payload:
            print('set cache....')
            cache.set('last_url_arbeitnow', self.payload[0]['advertise_url'], timeout=None)
        # print(cache.get('last_url_arbeitnow'))

