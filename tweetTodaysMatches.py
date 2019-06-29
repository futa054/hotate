import os
import json
import config
import requests
from requests_oauthlib import OAuth1Session
import matchEntity
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

def getTweet():
    matches = getTodaysMatches()
    if not matches:
        text = '本日、J1開催の試合はありません。'
        return text
    
    texts = []
    texts.append('本日、J1開催の試合')
    for match in matches:
        texts.append(match.startTime + ',' + match.stadium + ',' + match.homeTeam + 'VS' + match.awayTeam)
        text = '\n'.join(texts)
    return text
    
# def lambda_handler(event, context):
session = OAuth1Session(CK, CS, AT, ATS)
params = {"status": getTweet() }
req = session.post(URL, params = params)
