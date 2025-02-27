from bs4 import BeautifulSoup


class AdvertisementParser:
    def __init__(self):
        self.soup = None

    @property
    def title(self):
        title_element = self.soup.find("a", attrs={"itemprop": "url"})
        if title_element:
            return title_element.get("title")

    @property
    def company(self):
        company_element = self.soup.find("a", attrs={"itemprop": "hiringOrganization"})
        if company_element:
            return company_element.text.replace("\n", "")

    @property
    def city(self):
        city_elem = self.soup.find("span", attrs={"class": "text-gray-600"})
        if city_elem:
            return city_elem.text

    @property
    def advertise_url(self):
        advertise_url_element = self.soup.find("a", attrs={"itemprop": "url"})
        if advertise_url_element:
            return advertise_url_element.get("href")

    @property
    def datetime(self):
        datetime_elem = self.soup.find("time")
        if datetime_elem:
            return datetime_elem.get("datetime")

    @property
    def content(self):
        content_elem = self.soup.find("div", attrs={"itemprop": "description"})
        if content_elem:
            return content_elem.text
        raise ValueError

    @property
    def tags(self):
        tags = self.soup.find("div", attrs={"class": "hidden sm:flex mt-4 ml-4 sm:col-span-2"})
        if tags:
            tag_buttons = tags.find_all("button")
            tag_list = list()
            for tag in tag_buttons:
                tag_list.append(tag.text.replace("\n", ""))

            return tag_list

    @property
    def salary(self):
        salary_elem = self.soup.find("div", attrs={"title": "Salary Information"})
        if salary_elem:
            return salary_elem.text.replace("Salary Icon", "").replace("\n", "")

    @property
    def company_link(self):
        company_link_elem = self.soup.find("a", attrs={"class": "text-primary-700 font-medium hover:text-primary-800 hover:underline"})
        if company_link_elem:
            return company_link_elem.get("href")

    def parse(self, html_doc):
        self.soup = BeautifulSoup(html_doc, 'html.parser')

        data = dict(
            title=self.title,
            company=self.company,
            city=self.city,
            advertise_url=self.advertise_url,
            datetime=self.datetime,
            content=self.content,
            tags=self.tags,
            salary=self.salary,
            company_link=self.company_link,
        )

        return data
