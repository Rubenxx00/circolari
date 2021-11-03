class News:
    def __init__(self, id, date, title, link, attachment):
        self.id = id
        self.date = date
        self.title = title
        self.link = link
        self.attachment = attachment

    def __str__(self):
        return f'{self.id} -> {self.title}'