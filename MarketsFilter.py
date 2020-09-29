from DEFINITIONS import MARKETS
class MarketFilter:

    @staticmethod
    def FilterMarkets(markets):
        markets = [bet_offer for bet_offer in markets
                        if bet_offer['criterion']['englishLabel'] in MARKETS.keys()
                        or ('by' in bet_offer['criterion']['englishLabel'] and 'Odd/Even' not in bet_offer['criterion']['englishLabel'])]
        return markets
        


