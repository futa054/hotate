import os
import json
import config
import requests
from requests_oauthlib import OAuth1Session
import matchEntity
from datetime import date
from getTodaysMatches import getTodaysMatches

# CK      = config.CONSUMER_KEY
# CS      = config.CONSUMER_SECRET
# AT      = config.ACCESS_TOKEN
# ATS     = config.ACCESS_TOKEN_SECRET
CK      = os.environ['CONSUMER_KEY']
CS      = os.environ['CONSUMER_SECRET']
AT      = os.environ['ACCESS_TOKEN']
ATS     = os.environ['ACCESS_TOKEN_SECRET']
twitter = OAuth1Session(CK, CS, AT, ATS)

URL = 'https://api.twitter.com/1.1/statuses/update.json'

def getTweet(category):
    todayStr = date.today().strftime('%Y%m%d')
    matches = getTodaysMatches(category, todayStr)
    if not matches:
        text = '本日、{}開催の試合はありません。'.format(str.upper(category))
        return text
    texts = []
    texts.append('本日、{}開催の試合'.format(str.upper(category)))
    for match in matches:
        texts.append(match.startTime + ',' + match.stadium + ',' + match.homeTeam + 'VS' + match.awayTeam)
        text = '\r\n'.join(texts)
    return text
    
def lambda_handler(event, context):
    categories = ['j1', 'j2', 'j3']
    session = OAuth1Session(CK, CS, AT, ATS)
    for category in categories:
        params = {"status": getTweet(category) }
        req = session.post(URL, params = params)
