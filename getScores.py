import json
import requests

def getPlayerList(grade: int):
    f = open(f'./data/player/player{grade}.json', encoding='UTF-8')
    return json.loads(f.read())

def getSongList(grade: int):
    f = open(f'./data/songs/songs{grade}.json', encoding='UTF-8')
    return json.loads(f.read())

def getDiff(diffStr: str) -> int:
    if diffStr == 'E+': return 9
    elif diffStr == 'EX': return 7
    elif diffStr == 'HD': return 5
    elif diffStr == 'NM': return 3
    elif diffStr == 'EZ': return 1
    else: return -1

def getScoresBySong(hash: str, diff: str, grade: int) -> dict:
    player = getPlayerList(grade)
    count = len(player['player'])
    ssidList = list()
    scores = dict()
    for p in player['player']:
        ssidList.append(p['ssid'])
    r = requests.get(f'https://scoresaber.com/api/leaderboard/by-hash/{hash}/scores?difficulty={getDiff(diff)}&countries=KR,JP')
    totalPages = ((r.json()['metadata']['total']-1) // r.json()['metadata']['itemsPerPage'])+1
    for page in range(1, totalPages+1):
        r = requests.get(f'https://scoresaber.com/api/leaderboard/by-hash/{hash}/scores?difficulty={getDiff(diff)}&countries=KR,JP&page={page}')
        rjson = r.json()
        for s in rjson['scores']:
            if s['leaderboardPlayerInfo']['id'] in ssidList:
                scores[s['leaderboardPlayerInfo']['id']] = s['baseScore']
                count -= 1
        if count == 0:
            break
    return scores

def calcRank(myAcc: float, totalAccs: dict) -> int:
    vlist = list(totalAccs.values())
    vlist.sort(reverse=True)
    for i in range(0, len(vlist)):
        if myAcc == vlist[i]:
            return i + 1
    return len(vlist) + 1

def getAcc(totalNotes: int, getScore: int) -> float:
    maxScore = (totalNotes - 13) * 115 * 8 + 115 + (115 * 8) + (115 * 32)
    return getScore / maxScore * 100.0

def getScores(grade: int):
    song = getSongList(grade)
    player = getPlayerList(grade)
    for s in song['songs']:
        sdict = getScoresBySong(s['hash'], s['diff'], grade)
        for p in player['player']:
            if p['ssid'] in sdict:
                p[s['code']] = getAcc(s['note'], sdict[p['ssid']])
                p[s['code']+'R'] = calcRank(sdict[p['ssid']], sdict)
            else:
                p[s['code']] = 0
                p[s['code']+'R'] = calcRank(0, sdict)
    return player



