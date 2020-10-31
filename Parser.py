from DEFINITIONS import MARKETS
from difflib import SequenceMatcher

class Parser:
    def __init__(self, match_info):
        self.home_team = match_info['homeName']
        self.away_team = match_info['awayName']

    def parse_bet_offer(self, bet_offer):
        english_label = bet_offer['criterion']['englishLabel']
        if ' by ' in english_label or ' - ' in english_label:
            if ' by ' in english_label:
                english_label = english_label.split(' by ')
            elif ' - ' in english_label:
                english_label = english_label.split(' - ')

            if english_label[0] == 'Total Corners':
                market_name = 'cornersTotal'
            elif english_label[0] == 'Total Offsides':
                market_name = 'offsidesTotal'
            elif english_label[0] == 'Total Cards':
                market_name = 'cardsTotal'
            elif english_label[0] == 'Total Fouls committed':
                market_name = 'foulsTotal'
            elif english_label[0] == 'Total Shots':
                market_name = 'shotsTotal'
            elif english_label[0] == 'Total Shots on Target':
                market_name = 'shotsTotal'
            elif english_label[0] == 'Total Ball possession (%)':   
                market_name = 'ballPossesionTotal'
                

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
                if home_team_ratio > 0.70 or away_team_ratio > 0.70:
                    if home_team_ratio > away_team_ratio:
                        market_name += 'HomeTeam'
                    else:
                        market_name += 'AwayTeam'
                else:
                    market_name = 'COS POSZLO NIE TAK PANIE JANIE'
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