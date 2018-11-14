import pandas

from sqlalchemy import create_engine

from src import settings


#########################################
# Reader class                          #
#########################################
class Loader(object):

    def __init__(self, model, connection, path):
        self.model = model
        self.con = create_engine(connection)
        self._path = settings.BASEPATH + path

    def _open(self):
        # lazy initialization
        self._dataset = pandas.read_json(self._path)

    @staticmethod
    def _list_to_string(x):
        if type(x) == list:
            return ', '.join(str(e) for e in x)
        return x.strip()

    def execute(self):
        if not hasattr(self, '_dataset'):
            self._open()

        self._dataset = self._dataset.applymap(self._list_to_string)
        self._dataset.to_sql(name=self.model, con=self.con, if_exists='append', index=False)
#########################################
