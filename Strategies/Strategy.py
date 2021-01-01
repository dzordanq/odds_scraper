from abc import ABC, abstractmethod

class Strategy(ABC):

    @abstractmethod
    def parse(self, content):
        pass

    @abstractmethod
    def filter_markets(self, markets):
        pass

    @abstractmethod
    def get_events(self, response):
        pass