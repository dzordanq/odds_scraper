from .Strategy import Strategy
from DEFINITIONS import MARKETS
from difflib import SequenceMatcher


class Football(Strategy):
    

    def parse(self, bet_offers):
        markets = {}
        for bet_offer in bet_offers:
            market_name = self._get_market_name(bet_offer)
            if not market_name in markets.keys():
                markets[market_name] = []
            
            for outcome in bet_offer['outcomes']:
                if outcome['status'] == 'OPEN':
                    outcome_dict = self._parse_outcome(outcome)
                    markets[market_name].append(outcome_dict)
        return markets

    def filter_markets(self, markets):
        return [bet_offer for bet_offer in markets
                        if bet_offer['criterion']['englishLabel'] in MARKETS.keys()
                        or ('Total Corners' in bet_offer['criterion']['englishLabel'] and 'Odd/Even' not in bet_offer['criterion']['englishLabel'])
                        or ('Total Cards' in bet_offer['criterion']['englishLabel'] and 'Odd/Even' not in bet_offer['criterion']['englishLabel'])
                        or ('Total Offsides' in bet_offer['criterion']['englishLabel'] and 'Odd/Even' not in bet_offer['criterion']['englishLabel'])
                        or ('Total Fouls' in bet_offer['criterion']['englishLabel'] and 'Odd/Even' not in bet_offer['criterion']['englishLabel'])
                        or ('Total Shots on Target' in bet_offer['criterion']['englishLabel'] and 'Odd/Even' not in bet_offer['criterion']['englishLabel'])
                        or ('Total Ball possession' in bet_offer['criterion']['englishLabel'])
            ]

    def get_events(self, response):
        return response['layout']['sections'][1]['widgets'][0]['matches']['events']

    def get_event_id(self, event):
        return event['mainBetOffer']['eventId']

    def set_event_info(self, event):
        self.home_team = event['event']['homeName']
        self.away_team = event['event']['awayName']
        self.event_id = event['event']['id']

    def _get_market_name(self, bet_offer):
        english_label = bet_offer['criterion']['englishLabel']
        if ' by ' in english_label or ' - ' in english_label:
            if ' by ' in english_label:
                english_label = english_label.split(' by ')
            elif ' - ' in english_label:
                english_label = english_label.split(' - ')

            market_name = MARKETS[english_label[0]]

            if self.home_team == english_label[1]:
                market_name += 'HomeTeam'
            elif self.away_team == english_label[1]:
                market_name += 'AwayTeam'
            elif english_label[1] == 'Away Team':
                market_name += 'AwayTeam'
            elif english_label[1] == 'Home Team':
                market_name += 'HomeTeam'
            elif english_label[1] == '2nd Half':
                market_name += 'SecondHalf'
            elif english_label[1] == '1st Half':
                market_name += 'FirstHalf'
            else:
                home_team_ratio = SequenceMatcher(a=self.home_team,b=english_label[1]).ratio()
                away_team_ratio = SequenceMatcher(a=self.away_team,b=english_label[1]).ratio()
                if home_team_ratio > 0.50 or away_team_ratio > 0.50:
                    if home_team_ratio > away_team_ratio:
                        market_name += 'HomeTeam'
                    else:
                        market_name += 'AwayTeam'
                else:
                    market_name = 'COS POSZLO NIE TAK PANIE JANIE'
        else:
            market_name = MARKETS[english_label]
        return market_name


    def _parse_outcome(self, outcome):
        outcome_name = outcome['englishLabel']
        outcome_odd = outcome['odds'] / 1000
        outcome_id = outcome['id']

        if "line" in outcome.keys():
            line = outcome['line'] / 1000
            outcome_name = f"{outcome_name} ({line})"
        
        outcome_dict = {
            'outcomeName': outcome_name,
            'outcomeOdd': outcome_odd,
            'outcomeId': f"{self.event_id}|{outcome_id}"
        }

        return outcome_dict