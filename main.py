import json

from kafka import KafkaProducer

from Unibet import Unibet
from DEFINITIONS import COMPETITIONS, MARKETS
from Parser import Parser
from functions import days_diffrence, convert_utc_to_local, convert_utc_to_local_for_nba
from datetime import datetime
import time

producer = KafkaProducer(bootstrap_servers='94.177.203.215:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

start_time = time.time()
local_timezone = datetime.now().astimezone().tzinfo
unibet = Unibet()
parser = Parser()
matches = []
for competition in COMPETITIONS:
    response = unibet.get_competition(COMPETITIONS[competition])
    events = parser.get_events(response, competition)
    for event in events[1:]:
        if competition == 'NBA':
            date, hour = convert_utc_to_local_for_nba(local_timezone, event['event']['start'])
        else:
            date, hour = convert_utc_to_local(local_timezone, event['event']['start'])
        match_info = {
            'homeName' : event['event']['homeName'],
            'awayName' : event['event']['awayName'],
            'date' : date,
            'hour' : hour,
            'competition': competition,
            'markets' : {}
        }
        if days_diffrence(match_info['date']) <= 2 and event['event']['state'] == 'NOT_STARTED':
            try:
                event_id = parser.get_event_id(event)
            except:
                continue
            event_details = unibet.get_event_details(event_id)

            if event_details.headers['content-type'] == 'application/json':
                event_details = event_details.json()
            else:
                pause_time = int(event_details.headers['Retry-After'])
                print(f'Too many requests, pausing for {pause_time}')
                time.sleep(pause_time)
                event_details = unibet.get_event_details(event_id)
                event_details = event_details.json()
            parser.set_event_info(event)
            markets = parser.parse(event_details)
            match_info['markets'] = markets
            # Kafka producer here
            # matches.append(match_info)
            producer.send('unibet_topic', match_info)
            # print(json.dumps(match_info))
producer.flush()

# print(time.time() - start_time)
# print(json.dumps(matches))

