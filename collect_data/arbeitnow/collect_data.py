from abc import ABC
from selenium import webdriver


class ICollectBySelenium(ABC):
    def __init__(self, site_root, search_keyword):
        self.site_root = site_root
        self.driver = webdriver.Firefox()
        self.driver.get(site_root)
        self.search_keyword = search_keyword
        self.advertisements = []
        self.payload = []

    def _login_by_selenium(self):
        pass

    def _set_search_data(self):
        pass

    def _collect_list_data(self):
        pass

    def _collect_data_detail(self):
        pass

    def _complete_advertisement(self):
        pass

    def _insert_collect_data(self):
        pass

    def _logout(self):
        self.driver.close()

    def crawl(self):
        self._login_by_selenium()
        self._set_search_data()
        self._collect_list_data()
        self._collect_data_detail()
        self._complete_advertisement()
        self._insert_collect_data()
        self._logout()
