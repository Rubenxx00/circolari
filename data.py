import pickle

class Data:
    db = 'app.db'

    def __init__(self):
        self._latest_id = -1
        self._latest_url = ''

    @staticmethod
    def load():
        try:
            with open(Data.db, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return Data()

    def save(self):
        with open(self.db, 'wb+') as f:
            pickle.dump(self, f)

    @property    
    def latest_url(self):
        return self._latest_url

    @latest_url.setter
    def latest_url(self, value):
        self._latest_url = value
        self.save()

    @property    
    def latest_id(self):
        return self._latest_id

    @latest_id.setter
    def latest_id(self, value):
        self._latest_id = value
        self.save()
