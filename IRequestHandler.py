from DataBaseManager import DataBaseManager
import abc
class IRequestHandler:
    def __init__(self,app):
        self.database = DataBaseManager()
