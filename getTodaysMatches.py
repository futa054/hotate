import requests
import matchEntity
from bs4 import BeautifulSoup


def getTodaysMatches(category, todayStr):
    url = 'https://www.jleague.jp/match/search/{}/{}/'.format(category, todayStr)
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')

    matchList = []
    matchTable = soup.find('table', attrs={'class': 'matchTable'})
    if not matchTable:
        return matchList
    matches = matchTable.find('tbody').find_all('tr')
    for m in matches:
        timeAndStadium = m.find('td', attrs={'class': 'stadium'})
        if timeAndStadium:
            time =timeAndStadium.get_text()[:5]
            stadium = timeAndStadium.find('a').get_text()
            homeTeam = m.find('td', attrs={'class': 'clubName leftside'}).get_text()[1:][:-1]
            awayTeam = m.find('td', attrs={'class': 'clubName rightside'}).get_text()[1:][:-1]
            match = matchEntity.Match(time, stadium, homeTeam, awayTeam)
            matchList.append(match)
    
    return matchList
