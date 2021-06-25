import requests
import telegram_send
from bs4 import BeautifulSoup
import json

send_message_url = 'https://api.telegram.org/bot1605063584:AAHkKpRWg-1joMSayzFwQFq_Mw8Yb1wK15s/sendMessage?chat_id=-516716492&text='

while True:
    url = 'https://hs-consumer-api.espncricinfo.com/v1/pages/matches/live?'
    response = requests.get(url)
    data = response.json()
    value = data['content']['matches']

    for i in value:
        
        if i['state'] == "LIVE" and i['status'] == 'Live'  and i['teams'][0]['team']["slug"] == 'india' or i['teams'][1]['team']["slug"] == 'india':  # or i['series]['name']=='IPL'
            # current_status
            # print(i['status'])
            # current_status=i['status']
            # telegram_send.send(messages=[current_status])

            # match_title
            print(i["slug"])
            match_title = i["slug"]
            telegram_send.send(
                messages=['MATCH : ' + match_title + ' started'])
            msg = 'MATCH : ' + match_title + ' started'
            res = requests.get(send_message_url+'"'+msg+'"')

            # series_name
            print(i['series']['name'])
            series_name = i['series']['name']
            telegram_send.send(messages=['SERIES : '+series_name])
            msg = 'SERIES : '+series_name
            res = requests.get(send_message_url+'"'+msg+'"')

            # toss winner
            toss_winner_id = i['tossWinnerTeamId']
            if toss_winner_id is not None:
                for j in i["teams"]:
                    if j["team"]["id"] == toss_winner_id:
                        toss_winner_name = j['team']['longName']
                        print(toss_winner_name, ' won the toss')
                        telegram_send.send(
                            messages=[toss_winner_name + ' Won the toss'])
                        msg = toss_winner_name + ' Won the toss'
                        res = requests.get(send_message_url+'"'+msg+'"')

            # choice
            if i["tossWinnerChoice"] is not None:
                if i["tossWinnerChoice"] == 1:
                    batting = toss_winner_name
                    print(toss_winner_name, ' chose to BAT')
                    telegram_send.send(
                        messages=[toss_winner_name+' chose to BAT'])
                    msg = toss_winner_name+' chose to BAT'
                    res = requests.get(send_message_url+'"'+msg+'"')

                else:
                    print(toss_winner_name, ' chose to FIELD')
                    telegram_send.send(
                        messages=[toss_winner_name+' chose to FIELD'])
                    msg = toss_winner_name+' chose to FIELD'
                    res = requests.get(send_message_url+'"'+msg+'"')

            # current_update
            

            # detail_info_url = 'https://hs-consumer-api.espncricinfo.com/v1/pages/match/details?seriesId=' + \
            #     str(i["series"]["objectId"]) + '&matchId=' + str(i["objectId"])
            # print(detail_info_url)
            # detail_response = requests.get(detail_info_url)
            # details = detail_response.json()
            para = 1
            temp0=''
            temp1=''
            temp2=''
            temp3=''
            temp4=''
            count=1
            while True:
                # current_update
                current_update = i["statusText"]
                if current_update is not None and temp0!=current_update:
                    print(current_update)
                    telegram_send.send(messages=['STATUS : '+current_update])
                    msg = 'STATUS : '+current_update
                    res = requests.get(send_message_url+'"'+msg+'"')
                    temp0=current_update
                
                detail_info_url = 'https://hs-consumer-api.espncricinfo.com/v1/pages/match/details?seriesId=' + \
                    str(i["series"]["objectId"]) + \
                    '&matchId=' + str(i["objectId"])
                # print(detail_info_url)
                detail_response = requests.get(detail_info_url)
                details = detail_response.json()
                
                #scores and score info
                for num in range(2):
                    if details['match']['teams'][num]['isLive'] == True:

                        scores = details['match']['teams'][num]['score']
                        score_info = details['match']['teams'][num]['scoreInfo']

                if temp1 != scores :
                    print('SCORES : ', scores)
                    telegram_send.send(messages=['SCORES : ' + scores])
                    msg = 'SCORES : ' + scores
                    res = requests.get(send_message_url+'"'+msg+'"')
                    temp1=scores
                if temp2 != score_info:    
                    print('SCORE INFO : ', score_info)    
                    telegram_send.send(messages=['SCORE INFO : ' + score_info])
                    msg = 'SCORE INFO : ' + score_info
                    res = requests.get(send_message_url+'"'+msg+'"')
                    temp2=score_info
                    count=1
                
                # is_six,is_four,_iswicket.byes,wide,noball
                info = details['recentBallCommentary']["ballComments"][0]
                if info['isSix'] == True and count>0:
                    print(info['title'], ' SIX RUNS')
                    telegram_send.send(
                        messages=[info['title'] + ' , SIX RUNS'])
                    msg = info['title'] + ' , SIX RUNS'
                    res = requests.get(send_message_url+'"'+msg+'"')
                    count=-1
                if info['isFour'] == True and count>0:
                    print(info['title'], ' FOUR RUNS')
                    telegram_send.send(
                        messages=[info['title'] + ' , FOUR RUNS'])
                    msg = info['title'] + ' , FOUR RUNS'
                    res = requests.get(send_message_url+'"'+msg+'"')
                    count=-1
                if info['isWicket'] == True and count>0:
                    print(info['title'], ' , OUT')    # print(info['title'].split('to')[1], ' , OUT')
                    telegram_send.send(
                        messages=[info['title'] + ' , OUT'])
                    msg = info['title'] , ' , OUT'
                    res = requests.get(send_message_url+'"'+msg+'"')
                    count=-1

                # run_rate
                current_run_rate=details['supportInfo']['liveInfo']['currentRunRate']
                if current_run_rate is not None and temp3!=current_run_rate:
                    print('Current Run Rate : ',
                          current_run_rate)
                    telegram_send.send(messages=[
                                       'Current Run Rate => '+str(current_run_rate)])
                    msg = 'Current Run Rate => ' + \
                        str(current_run_rate)
                    res = requests.get(send_message_url+'"'+msg+'"')
                    temp3=current_run_rate
                
                required_run_rate=details['supportInfo']['liveInfo']['requiredRunrate']
                if required_run_rate is not None and temp4!=required_run_rate:
                    print('Required Run Rate : ',
                          required_run_rate)
                    telegram_send.send(messages=[
                                       'Required Run Rate => '+str(required_run_rate)])
                    msg = 'Required Run Rate => ' + \
                        str(required_run_rate)
                    res = requests.get(send_message_url+'"'+msg+'"')
                    temp4=required_run_rate
                
                # super_over
                if details['supportInfo']['superOver'] == True and para != 0:
                    print('****SUPER OVER****')
                    msg = '****SUPER OVER****'
                    res = requests.get(send_message_url+'"'+msg+'"')
                    para = 0

                # result
                if details['supportInfo']["playersOfTheMatch"] is not None:
                    print('Player of the match => ',
                          details['supportInfo']["playersOfTheMatch"])
                    telegram_send.send(
                        messages=['Player of the match => '+details['supportInfo']["playersOfTheMatch"]])
                    msg = 'Player of the match => ' + \
                        details['supportInfo']["playersOfTheMatch"]
                    res = requests.get(send_message_url+'"'+msg+'"')

                if details['supportInfo']['matchSeriesResult'] is not None:
                    print('RESULT => ',
                          details['supportInfo']['matchSeriesResult'])
                    telegram_send.send(
                        messages=['RESULT => '+details['supportInfo']["matchSeriesResult"]])
                    msg = 'RESULT => ' + \
                        details['supportInfo']["matchSeriesResult"]
                    res = requests.get(send_message_url+'"'+msg+'"')

                if i['state'] != "LIVE" or i['status'] != 'Live':
                    break
