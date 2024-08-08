from collect_data.crawler.crawler import Repository


class DummyStorage(Repository):

    def save_data(self, data):
        pass
