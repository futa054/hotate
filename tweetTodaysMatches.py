import os
import json
import config
import requests
from requests_oauthlib import OAuth1Session
import matchEntity
from datetime import date
from getTodaysMatches import getTodaysMatches

CK      = config.CONSUMER_KEY
CS      = config.CONSUMER_SECRET
AT      = config.ACCESS_TOKEN
ATS     = config.ACCESS_TOKEN_SECRET
# CK      = os.environ['CONSUMER_KEY']
# CS      = os.environ['CONSUMER_SECRET']
# AT      = os.environ['ACCESS_TOKEN']
# ATS     = os.environ['ACCESS_TOKEN_SECRET']
twitter = OAuth1Session(CK, CS, AT, ATS)

URL = 'https://api.twitter.com/1.1/statuses/update.json'

def getTweet(category):
    todayStr = date.today().strftime('%Y%m%d')
    matches = getTodaysMatches(category[0], todayStr)
    texts = []
    if not matches:
        return texts
    header = '本日、{}の試合一覧'.format(str.upper(category[1]))
    text = ''
    for match in matches:
        text += '\r\n' + match.startTime + ',' + match.stadium + ',' + match.homeTeam + 'VS' + match.awayTeam
        if len(text) > 100:
            texts.append(header + text)
            text = ''
    if text:
        texts.append(header + text)
    return texts
    
def lambda_handler(event, context):
    categories = {'j1': 'J1', 'j2': 'J2', 'j3': 'J3', 'emperor': '天皇杯', 'acl': 'ACL', 'leaguecup': 'ルヴァン'}
    tweets = []
    for category in categories.items():
        tweets += getTweet(category)
    session = OAuth1Session(CK, CS, AT, ATS)
    if not tweets:
        tweets = ['本日、開催の試合はありません']
    for tweet in tweets:
        params = {"status": tweet }
        req = session.post(URL, params = params)
