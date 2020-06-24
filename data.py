

class HeadData:
    def __init__(self, **kwargs):
        self.title = kwargs.get('title', '')
        self.description = kwargs.get('description', '')
        self.keywords = kwargs.get('keywords', [])
        self.author = kwargs.get('author', '')
        self.keywords_string = ''

    def make_keywords(self):
        num_keywords = len(self.keywords)
        index = 0
        last_index = num_keywords - 1
        while index < num_keywords:
            add_string = self.keywords[index]
            if index != last_index:
                add_string += ', '
            self.keywords_string += add_string
            index += 1


class Link:
    def __init__(self, name, url):
        self.name = name
        self.url = url




