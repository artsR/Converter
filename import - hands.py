from collections import defaultdict
import requests, bs4
import re
import datetime
import os



def check_winner(dictionary):
    '''
        function should get as an argument 'game['status']['player']'.
    '''
    winners   = []
    max_point = max(dictionary.values())
    for player, status in dictionary.items():
        if status == max_point:
            winners.append(player)
    return winners


def gather_player_bets(game):
    bets = {}
    for street in ['Blind', 'Pre-Flop', 'Flop', 'Turn', 'River']:
        for player, size, play in zip(game['hand'][street]['players'],game['hand'][street]['sizes'],game['hand'][street]['plays']):
            if (play != 'All-In Insurance') and (play != 'Insurance Payout'):
                bets.setdefault(player, [])
                if size != '':
                    bets[player].append(float(re.search(r'\d+(\.)*\d*', size).group()))

    return bets


def initial_stacks(nicknames, stacks, game):
    bets = gather_player_bets(game)
    for player in nicknames:
        i = nicknames.index(player)
        stacks[i] = float(re.search(r'\d+(\.)*\d*', stacks[i]).group())
        stacks[i] += sum(bets[player])

    return stacks


def board_cards():
    f_t_r = []
    community_cards = soup.find('section', {'class':'_community-cards'}). \
                           find_all("pokercraft-hh-card")
    if community_cards != None:
        for card in community_cards:
            if card['rabbit'] == 'false':
                f_t_r.append(card['card'])
    return f_t_r


def find_button(soup):
     button = soup.find('i', {'class':'_dealer-button'}).parent.div.text.strip()
     return clear_name(button)

def clear_name(nickname):
    if nickname.isalnum():
        return nickname
    else:
        nickname = re.sub(r'[():]', '', nickname).strip()
        return nickname
#-------------------------------------------------------------------------------
handFile = open('August_2019.txt', 'w')
errorFile = open('errors.txt', 'w')
dat = input()
for file_hand in os.listdir():

    if file_hand.startswith('hand') and file_hand.endswith('.htm'):
        print(str(file_hand))
        hand = open(file_hand, encoding='utf-8')
        soup = bs4.BeautifulSoup(hand)
        try:
            soup.find('strong', {'class':'_title'} ).text
        except:
            errorFile.write(str(file_hand)+'\n')
            continue
            pass
        gameTitle = str(soup.select('._title'))
        gameNAME = soup.find('strong', {'class':'_title'} ).text
        match = re.compile(r'#(\d+)').search(gameTitle)
        gameID = match.group(1)
        gameSTAKES = re.compile(r'\$[\d]+\.[\d]*\s\/\s\$[\d]+\.*[\d]*').search(gameTitle).group()
        gameSTAKES = ''.join(gameSTAKES.split())

        # Identify board players (stack, position and nickname)
        board     = []
        nicknames = []
        positions = []
        stacks    = []
        cards_known = {}
        bets_player = {}
        game      = defaultdict(dict, (('hand', {}), ('status', {} ))) # 'status', player : status
        for item in soup.find_all("pokercraft-hh-table"):
            for card in item.find_all("pokercraft-hh-card"):
                try:
                    check = card['rabbit']
                except KeyError:
                    check = 'false'
                    pass
                if check == 'false':
                    try:
                        board.append(card['card'])
                    except KeyError:
                        pass
            for player in item.find_all("pokercraft-hh-player"):
                nicknames.append(player.find_all('section')[1] \
                            .find('div') \
                            .get_text() \
                            .strip() )
                stacks.append(player.find_all('section')[1] \
                            .find_all('div')[1] \
                            .get_text() \
                            .strip() )
                positions.append(player.find('pokercraft-hh-avatar')['position'])

                cards_known.setdefault(nicknames[-1],
                            ', '.join([tag['card'] for tag in player.find_all(card=True) if tag != ''])
                            )

        for i in range(len(nicknames)):
            nicknames[i] = clear_name(nicknames[i])

        num_player = len(nicknames)#sum([1 for pos in positions if pos != 'Sitting Out' ])# <---- new added to substruct number of players of sitting out.
        game['status'].setdefault('player', {})
        game['status']['player'] = game['status']['player'].fromkeys(nicknames, 1)
        # Change status Sitted Out players:
        for i, pos in enumerate(positions):
            if pos == 'Sitting Out':
                game['status']['player'][nicknames[i]] = 0
        #--------------
        summary = soup.find('pokercraft-hh-summary')
        #game = {}
        # Preflop action:
        line1 = '***** Hand History for Game %s *****\n' % (gameID)
        line2 = '%s USD NL Texas Hold\'em - Wednesday, August %s, 19:43:40 CET 2019\n' % (gameSTAKES, dat)
        line3 = 'Table%s N (Real Money)\n' % (gameID)
        line4 = 'Seat %s is the button\n' % (nicknames.index(find_button(soup))+1)
        line5 = 'Total number of player : %s/6\n' % (num_player)
        handFile.write(''.join([line1, line2, line3, line4, line5]))
        for i in range(len(positions)):
            handFile.write('Seat '+str(i+1)+': '+str(nicknames[i])+' ( '+str(stacks[i])+' USD )\n')

        for stage in summary.find_all('section', recursive=False):
            f = stage.find('header').text.strip('\n\r ').split()

            game['hand'].setdefault(f[0], {})
            game['hand'][f[0]].update(pot=f[1])
            game['hand'][f[0]].setdefault('players', [])
            game['hand'][f[0]].setdefault('plays', [])
            game['hand'][f[0]].setdefault('sizes', [])

            actions = stage.section.select('._action')

            player = []
            for action in actions:
                if ('_expanded' in action['class']):
                    winner = action.find('div', {'class':'_nickname'}).text.strip()
                    winner = clear_name(winner)#added clear_name
                    game['status']['player'][winner] = 2
                elif ('_spread' in action.find('div', {'class' : '_content'})['class']):
                    pass
                else:
                    if (action.find('div', {'class': '_timebank'}) != None) or (action.find('div', {'class': '_emoticon'}) != None):
                        continue
                    player = [x for x in action.text.strip('\n\r ').split('\n') if x != '']
                    if '_mine' in action['class']:
                        player.insert(0, action.find('pokercraft-hh-avatar')['position'])

                    if player[2].lower() == 'fold':
                        game['status']['player'][clear_name(player[1])] = 0#added clear_name
                    game['hand'][f[0]]['players'].append(clear_name(player[1]))#added clear_name
                    game['hand'][f[0]]['plays'].append(player[2])
                    if len(player) > 3:
                        game['hand'][f[0]]['sizes'].append(' [%s USD]' % player[3])
                    else:
                        game['hand'][f[0]]['sizes'].append('')


        line6 = '%s posts small blind %s.\n' % \
                (game['hand']['Blind']['players'][0],
                 game['hand']['Blind']['sizes'][0])
        line7 = '%s posts big blind %s.\n' % \
                (game['hand']['Blind']['players'][1],
                 game['hand']['Blind']['sizes'][1])
        lineE1 = ''
        if len(game['hand']['Blind']['sizes']) > 2:
            for i in range(2, len(game['hand']['Blind']['sizes'])):
                lineE1 += lineE1 + \
                          '%s posts big blind %s.\n' % \
                            (game['hand']['Blind']['players'][i],
                            game['hand']['Blind']['sizes'][i])

        line8 = '** Dealing down cards **\n'
        line9 = 'Dealt to %s [  %s ]\n' % \
                (nicknames[positions.index('HERO')],
                ''.join(cards_known[nicknames[positions.index('HERO')]].split(',')) )

        handFile.write(''.join([line6, line7, lineE1, line8, line9]))
        for i in range(len(game['hand']['Pre-Flop']['players'])):
            handFile.write(''.join([
                        game['hand']['Pre-Flop']['players'][i]+' ',
                        game['hand']['Pre-Flop']['plays'][i].lower()+'s',
                        game['hand']['Pre-Flop']['sizes'][i]
                        ]) +'\n'
            )
        comm_cards = board_cards()
        if len(comm_cards) > 2:
            line10 = '** Dealing Flop ** [ %s, %s, %s ]\n' % \
                    (comm_cards[0], comm_cards[1], comm_cards[2])
            handFile.write(line10)
            for i in range(len(game['hand']['Flop']['players'])):
                handFile.write(''.join([
                            game['hand']['Flop']['players'][i]+' ',
                            game['hand']['Flop']['plays'][i].lower()+'s',
                            game['hand']['Flop']['sizes'][i]
                            ]) +'\n'
                )
            if len(comm_cards) > 3:
                line11 = '** Dealing Turn ** [ %s ]\n' % comm_cards[3]
                handFile.write(line11)
                for i in range(len(game['hand']['Turn']['players'])):
                    handFile.write(''.join([
                                game['hand']['Turn']['players'][i]+' ',
                                game['hand']['Turn']['plays'][i].lower()+'s',
                                game['hand']['Turn']['sizes'][i]
                                ]) +'\n'
                    )
                if len(comm_cards) > 4:
                    line12 = '** Dealing River ** [ %s ]\n' % comm_cards[4]
                    handFile.write(line12)
                    for i in range(len(game['hand']['River']['players'])):
                        handFile.write(''.join([
                                    game['hand']['River']['players'][i]+' ',
                                    game['hand']['River']['plays'][i].lower()+'s',
                                    game['hand']['River']['sizes'][i]
                                    ]) +'\n'
                        )
        # the winning amount I may take from River unless showdown was true.
        # If the max of status is 1, then hands finished w/o showdown.
        # If there was showdown at least one player has 'status'=2.
        # pot_final = float(re.search(r'\d+(\.)*\d*', game['hand']['River']['pot']).group()) * 1.5# write func summing all bets and calls
        # pot_final = round(pot_final, 2)
        pot_final = list(gather_player_bets(game).values())
        pot_final = sum([sum(x) for x in pot_final])

        for player, hand in cards_known.items():
            if hand != '':
                lineShowdown = '%s shows [ %s ].\n' % (player, hand)
                handFile.write(lineShowdown)
        winners = check_winner(game['status']['player'])
        for winner in winners:
            pot_final = pot_final / len(winners)
            pot_final = 0.90 * pot_final
            lineSummary = '%s wins $%s USD\n' % \
                        (winner, pot_final)
            handFile.write(lineSummary)
        handFile.write('\n\n')
handFile.close()
errorFile.close()
#--------------
