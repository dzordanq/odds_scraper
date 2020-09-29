from DEFINITIONS import MARKETS
from difflib import SequenceMatcher

class Parser:
    def __init__(self, match_info):
        self.home_team = match_info['homeName']
        self.away_team = match_info['awayName']

    def parse_bet_offer(self, bet_offer):
        english_label = bet_offer['criterion']['englishLabel']
        if 'by' in english_label:
            english_label = english_label.split(' by ')
            if english_label[0] == 'Total Goals':
                market_name = 'goalsTotal'
            elif english_label[0] == 'Total Corners':
                market_name = 'cornersTotal'
            

            if self.home_team == english_label[1]:
                market_name += 'HomeTeam'
            elif self.away_team == english_label[1]:
                market_name += 'AwayTeam'
            else:
                home_team_ratio = SequenceMatcher(a=self.home_team,b=english_label[1]).ratio()
                away_team_ratio = SequenceMatcher(a=self.away_team,b=english_label[1]).ratio()
                if home_team_ratio > away_team_ratio:
                    market_name += 'HomeTeam'
                else:
                    market_name += 'AwayTeam'
        else:
            market_name = MARKETS[english_label]
        return market_name


    def parse_outcome(self, outcome):
        outcome_name = outcome['englishLabel']
        outcome_odd = outcome['odds'] / 1000
        try:
            line = outcome['line'] / 1000
        except:
            line = None

        if line:
            outcome_name = f"{outcome_name} ({line})"
        
        outcome_dict = {
            'outcomeName': outcome_name,
            'outcomeOdd': outcome_odd
        }

        return outcome_dict