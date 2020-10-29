import json

import requests
from kafka import KafkaProducer

from Unibet import Unibet
from DEFINITIONS import COMPETITIONS, MARKETS
from MarketsFilter import MarketFilter
from Parser import Parser
from functions import days_diffrence, convert_utc_to_local
from datetime import datetime
import time

start_time = time.time()
local_timezone = datetime.now().astimezone().tzinfo
unibet = Unibet()
matches = []
for competition in COMPETITIONS:
    response = unibet.get_competition(COMPETITIONS[competition])
    events = response['layout']['sections'][1]['widgets'][0]['matches']['events']
    for event in events:
        date, hour = convert_utc_to_local(local_timezone, event['event']['start'])
        match_info = {
            'homeName' : event['event']['homeName'],
            'awayName' : event['event']['awayName'],
            'date' : date,
            'hour' : hour,
            'competition': competition,
            'markets' : {}
        }
        if days_diffrence(match_info['date']) <= 2:
            parser = Parser(match_info)
            
            event_details = unibet.get_event_details(event['mainBetOffer']['eventId'])
            try:
                event_details = event_details.json()
            except:
                pause_time = int(event_details.headers['Retry-After'])
                print(f'Too many requests, pausing for {pause_time}')
                time.sleep(int(event_details.headers['Retry-After']))
                event_details = unibet.get_event_details(event['mainBetOffer']['eventId'])
                event_details = event_details.json()

            bet_offers = MarketFilter.FilterMarkets(event_details['betOffers'])
            for bet_offer in bet_offers:
                market_name = parser.parse_bet_offer(bet_offer)

                if not market_name in match_info['markets'].keys():
                    match_info['markets'][market_name] = []
                
                for outcome in bet_offer['outcomes']:
                    if outcome['status'] == 'OPEN':
                        outcome_dict = parser.parse_outcome(outcome)
                        match_info['markets'][market_name].append(outcome_dict)

            # Kafka producer here
            # matches.append(match_info)
            producer = KafkaProducer(bootstrap_servers='94.177.203.215:9092',
                                     value_serializer=lambda v: json.dumps(v).encode('utf-8'))
            producer.send('unibet_topic', match_info)
            producer.flush()

# print(time.time() - start_time)
# print(json.dumps(matches))

