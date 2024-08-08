from typing import List

from bs4 import BeautifulSoup

from collect_data.crawler.crawler import CrawlerBaseByRequests


class ArbeitnowCrawler(CrawlerBaseByRequests):
    _site_root = "https://www.arbeitnow.com/"
    _search_keyword_format = '?search=%s&tags=%s&sort_by=%s&page=%d'
    _search_by_category = 'jobs/%s/' + _search_keyword_format
    _current_page_num = 1
    _category = ""
    _tags = []
    _sorted_by = "newest"

    def set_current_page_num(self, number: int):
        self._current_page_num = number
        return self

    def set_sorted_by(self, sort: str):
        self._sorted_by = sort
        return self

    def set_category(self, category: str):
        self._category = category
        return self

    def set_tags(self, tags: List):
        if not tags:
            self._tags = '[]'
        if len(tags) == 1:
            self._tags = '["%s", ""]' % tags[0]

        template = '['
        for i in range(len(tags) - 1):
            template += '"%s",' % tags[i]
        template += '"%s"]' % tags[len(tags) - 1]
        self._tags = template

        return self

    def _get_crawl_link(self):
        link_template = self._site_root

        if self._category:
            link_template += self._search_by_category
            link_template = link_template % (self._category, self._search_keyword, self._tags, self._sorted_by,
                                             self._current_page_num)
            self._current_page_num += 1
        else:
            link_template += self._search_keyword_format
            link_template = link_template % (self._search_keyword, self._tags, self._sorted_by, self._current_page_num)
            self._current_page_num += 1

        print(link_template)

        return link_template

    @staticmethod
    def _find_links(html_doc):
        soup = BeautifulSoup(html_doc, 'html.parser')

        noscript_data = soup.find("noscript")
        all_a_tag = noscript_data.find_all("a", attrs={"class": "flex"})
        if not all_a_tag:
            return []

        old_len, new_len = len(all_a_tag[0].get("href")), len(all_a_tag[0].get("href").replace("page=", ""))
        if old_len > new_len:
            return []

        clean_links = list()

        for a in all_a_tag[:len(all_a_tag)]:
            clean_links.append((a.get("href")))

        return clean_links

    def _crawl_links(self) -> None:
        while True:
            response = self._get(get_url=self._get_crawl_link())
            new_links = self._find_links(response.text)
            if not new_links:
                return None
            self._links.extend(new_links)
