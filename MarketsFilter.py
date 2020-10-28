from DEFINITIONS import MARKETS
class MarketFilter:

    @staticmethod
    def FilterMarkets(markets):
        markets = [bet_offer for bet_offer in markets
                        if bet_offer['criterion']['englishLabel'] in MARKETS.keys()
                        or ('Total Corners' in bet_offer['criterion']['englishLabel'] and 'Odd/Even' not in bet_offer['criterion']['englishLabel'])
                        or ('Total Cards' in bet_offer['criterion']['englishLabel'] and 'Odd/Even' not in bet_offer['criterion']['englishLabel'])
                        or ('Total Offsides' in bet_offer['criterion']['englishLabel'] and 'Odd/Even' not in bet_offer['criterion']['englishLabel'])
                        or ('Total Fouls' in bet_offer['criterion']['englishLabel'] and 'Odd/Even' not in bet_offer['criterion']['englishLabel'])
                        or ('Total Shots on Target' in bet_offer['criterion']['englishLabel'] and 'Odd/Even' not in bet_offer['criterion']['englishLabel'])
                        or ('Total Ball possession' in bet_offer['criterion']['englishLabel'])
            ]
        return markets
        


