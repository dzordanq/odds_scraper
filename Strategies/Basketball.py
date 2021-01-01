from .Strategy import Strategy

class Basketball(Strategy):
    

    def parse(self, bet_offers):
        markets = {}
        for bet_offer in bet_offers:
            market_name = self._get_market_name(bet_offer)
            if not market_name in markets.keys():
                markets[market_name] = []
            
            player_outcomes = {}
            for outcome in bet_offer['outcomes']:
                if outcome['status'] == 'OPEN':
                    if 'participant' in outcome.keys():
                        player_name_parts = outcome['participant'].split(",")
                        player_name = f"{player_name_parts[0]} {'.'.join(map(lambda x: x.strip()[0], player_name_parts[1:]))}."
                        player_outcomes[player_name] = []
                    player_outcomes[player_name].append(self._parse_outcome(outcome))


            markets[market_name].append({
                "playerName": player_name,
                "bets": player_outcomes[player_name]
            })
            
        return markets

    def filter_markets(self, markets):
        return [bet_offer for bet_offer in markets if
                        ('Points scored by the player' in bet_offer['criterion']['englishLabel'])
                        or ('Rebounds by the player' in bet_offer['criterion']['englishLabel'])
                        or ('Assists by the player' in bet_offer['criterion']['englishLabel'])]
            

    def get_events(self, response):
        return response['events']

    def get_event_id(self, event):
        return event['event']['id']

    def set_event_info(self, event):
        self.home_team = event['event']['homeName']
        self.away_team = event['event']['awayName']
        self.event_id = event['event']['id']


    def _get_market_name(self, bet_offer):
        english_label = bet_offer['criterion']['englishLabel']
        if "Points" in english_label:
            return "pointsTotal"
        elif "Rebounds" in english_label:
            return "reboundsTotal"
        elif "Assists" in english_label:
            return "assistsTotal"


    def _parse_outcome(self, outcome):
        outcome_name = outcome['englishLabel'].replace(" ", " (")
        outcome_name += ")"
        outcome_odd = outcome['odds'] / 1000
        outcome_id = outcome['id']

        return {
            'outcomeName': outcome_name,
            'outcomeOdd': outcome_odd,
            'outcomeId': f"{self.event_id}|{outcome_id}"
        }
