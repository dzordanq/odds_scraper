from DEFINITIONS import MARKETS
from Strategies.Football import Football
from Strategies.Basketball import Basketball


class Parser:
    def __init__(self):
        self._strategy = None
        self._strategies = {
            "Football": Football(),
            "Basketball": Basketball()
        }


    @property
    def strategy(self):
        return self._strategy
    
    @strategy.setter
    def strategy(self, sport_name):
        self._strategy = self._strategies[sport_name]


    def parse(self, event_details):
        bet_offers = self._strategy.filter_markets(event_details['betOffers'])
        return self._strategy.parse(bet_offers)

    
    def get_events(self, response, competition):
        if competition == "NBA":
            self.strategy = "Basketball"
        else:
            self.strategy = "Football"

        return self._strategy.get_events(response)


    def get_event_id(self, event):
        return self._strategy.get_event_id(event)

    def set_event_info(self, event):
        self._strategy.set_event_info(event)
        
    