import yahoo_dev_id as yid
import Answers as an
import random
import os
import sys
reload(sys)
sys.setdefaultencoding('latin-1')


def say(message,speakers = False):
    print str(message)
    #return True
    if not speakers:
        os.system('say ' + str(message))
    elif len(speakers) > 1:
        speaker = speakers[random.randint(0,len(speakers)-1)]
        os.system('say -v '+str(speaker)+' '+ str(message))
    else:
        os.system('say -v '+str(speakers[0])+' '+ str(message))
    return True

def build_players(raw_players):
    players = {}
    for player_name in raw_players.split(','):
        players[player_name] = 0
    return players

def print_players(players):
    i = 0
    for player in players:
        print str(i) + ') ' + str(player)
        i += 1

def add_score(winner):
    i = 0
    for player in players:
        if i == int(winner):
            players[player] += 1
            break
        i+=1

def print_scores(players):
    for player in players:
        print str(player)+':'+str(players[player])

def get_winner(players):
    winners = []
    max_score = 0
    for player in players:
        if players[player] > max_score:
            max_score = players[player]
            winners = [player]
        elif players[player] == max_score:
            winners.append(player)
    return winners

speakers = ['Agnes','Albert','Alex','Bad News','Bahh','Bells','Boing','Bruce','Bubbles','Cellos','Deranged','Fred','Good News','Hysterical','Junior','Kathy','Pipe Organ','Princess','Ralph','Trinoids','Vicki','Victoria','Whisper']
say('Dear human, you are a tiny speck dwarfed by even the tiniest objects in the heavens. But I understand you like to play.',['Zarvox'])
say('Please, communicate your names:',['Zarvox'])
raw_players = raw_input().replace(" ","")
players = build_players(raw_players)
say('Okay, little pieces of flesh. I am going to ask you a few questions. You answer them. You vote for the best answer. Good luck!',['Zarvox'])
app = an.Answers()
app.appid = yid.YAHOO_ID
end_game = False
topic = 'sex'
start = random.randint(0,999)
while not end_game:
    params = {
        'query':topic,
        'type':'resolved',
        'start':str(start),
        #'region':'es',
    }
    questions = app.questionSearch(params)
    while len(questions) <= 0:
        start = max(start - 100,1)
        print 'still searching for questions about this topic...'
        if start == 1:
            say('Dear Asimov! No questions about this topic were found.',['Zarvox'])
            break
        params['start'] = str(start)
        questions = app.questionSearch(params)
    if len(questions):
        num_questions = len(questions)
        chosen_question = questions[random.randint(0,num_questions-1)]
        question = chosen_question['Subject']
        say(question,speakers)
        raw_input('Check chosen answer\n')
        chosen_answer = chosen_question['ChosenAnswer']
        try:
            print chosen_answer
            say('Communicate winner:',['Zarvox'])
            print_players(players)
            winner = raw_input()
            while int(winner) < 0 or int(winner) > (len(players)-1):
                print_players(players)
                winner = raw_input()
            add_score(winner)
            print_scores(players)
        except Exception:
            print 'Unable to print answer, probably it has something to do with encoding. Keep trying'
        say('Communicate winner:',['Zarvox'])
        print_players(players)
        winner = raw_input()
        while int(winner) < 0 or int(winner) > (len(players)-1):
            print_players(players)
            winner = raw_input()
        add_score(winner)
        print_scores(players)
        raw_input()
    topic = raw_input('Choose next topic, type "q" to end game:')
    while topic == '':
        topic = raw_input('Choose next topic, type "q" to end game:')
    end_game = topic == 'q'
    start = random.randint(0,999)
winners = get_winner(players)
if len(winners) > 1:
    say('The winners are: '+(',').join(winners),['Zarvox'])
else:
    say('The winner is: '+ winners[0],['Zarvox'])
say('Good bye!',['Zarvox'])
os.system('say -f spice.txt')


    
