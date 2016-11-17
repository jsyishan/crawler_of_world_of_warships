from urllib import request, parse
from bs4 import BeautifulSoup
import json

__author__ = 'Eugen'


class PlayerInfo(object):
    def __init__(self, name, zone):
        self.data = {'player': name, 'zone': zone}
        self.url = 'http://182.18.61.50/wows/index.html'
        self.url_get_user_info = 'http://182.18.61.50/Data/action/WowsAction/getLogin'
        self.usr_get_data_info = 'http://182.18.61.50/Data/action/WowsAction/getShipInfo'

        self.user_agent = ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
                                         ' AppleWebKit/537.36'
                                         ' (KHTML, like Gecko)'
                                         ' Chrome/54.0.2840.99 '
                                         'Safari/537.36')

        print('Step 1 ... init')
        self.get_info()

    def get_user_info(self):
        req_url = self.url_get_user_info + '?name=' + self.data['player'] + '&zone=' + self.data['zone']

        req = request.Request(req_url)
        req.add_header(self.user_agent[0], self.user_agent[1])

        with request.urlopen(req) as f:
            got_json = json.loads(f.read().decode('utf-8'))
            if 'errno' not in got_json.keys():
                self.data['aid'] = got_json['account_db_id']
                self.data['name'] = got_json['nick']
                print('Aid of User \'%s\' is %s' % (self.data['name'], self.data['aid']))
                return True
            print('Error: Check for the information that you input!')
            return False


    def get_data_info(self):
        req_url = self.usr_get_data_info + '?aid=' + self.data['aid']

        req = request.Request(req_url)
        req.add_header(self.user_agent[0], self.user_agent[1])

        with request.urlopen(req) as f:
            self.data['ship_json'] = json.loads(f.read().decode('utf-8'))
            data = self.data['ship_json']
            self.data['ships_info'] = []
            for dt in data:
                self.data['ships_info'].append(dt)  # All ships' information in self.data['ships_info']

            def calc_info(attr):
                self.data[attr] = 0
                i = 0
                for j in range(len(self.data['ships_info'])):
                    self.data[attr] += self.data['ships_info'][i][attr]  # Number of battles
                    i += 1
                print('%s: %s' % (attr, self.data[attr]))

            calc_info('battles')
            calc_info('teambattles')
            calc_info('wins')
            calc_info('teamwins')
            calc_info('damage')

            self.data['singlebattles'] = self.data['battles'] - self.data['teambattles']
            self.data['singlewins'] = self.data['wins'] - self.data['teamwins']
            self.data['winrate'] = self.data['wins'] / self.data['battles']
            self.data['teamwinrate'] = self.data['teamwins'] / self.data['teambattles']
            self.data['singlewinrate'] = self.data['singlewins'] / self.data['singlebattles']

    def get_info(self):
        print('Trying connecting to the server...')
        hasUser = self.get_user_info()
        if hasUser:
            self.get_data_info()

        # req_url = self.url + '?name=' + self.data['player'] + '&zone=' + self.data['zone']
        #
        # req = request.Request(req_url)
        # req.add_header(self.user_agent[0], self.user_agent[1])

        # with request.urlopen(req) as f:
        #     self.data['data'] = f.read()
        #     print('Status:', f.status, f.reason)
        #     self.soup_match()


# def soup_match(self):
#     soup = BeautifulSoup(self.data['data'], 'html.parser', from_encoding='utf-8')
#     content = soup.find('div', id='total').findAll('span', {'class': 'value'})
#     for i in content:
#         print(i.string)

def get_user():
    # name = parse.quote(input('玩家昵称：'))
    name = parse.quote('pnq-Ar196-欧根亲王')
    zone = input('分区(默认南区)： ')
    if not zone == '':
        if not zone == 'south' and not zone == 'north':
            print('请输入正确的分区!')
            return
        players.append(PlayerInfo(name, zone))
    else:
        players.append(PlayerInfo(name, 'south'))


if __name__ == '__main__':
    players = []
    get_user()
