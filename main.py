from urllib import request, parse
from bs4 import BeautifulSoup
import json

__author__ = 'Eugen'


class CrawlerOfWOWS(object):
    def __init__(self):
        self.data = {}
        self.url = 'http://rank.kongzhong.com/wows/index.html'
        self.url_get_user_info = 'http://rank.kongzhong.com/Data/action/WowsAction/getLogin'
        self.usr_get_data_info = 'http://rank.kongzhong.com/Data/action/WowsAction/getShipInfo'

        self.user_agent = ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
                                         ' AppleWebKit/537.36'
                                         ' (KHTML, like Gecko)'
                                         ' Chrome/54.0.2840.99 '
                                         'Safari/537.36')

        print('Step 1... init')

    def get_user_info(self):
        req_url = self.url_get_user_info + '?name=' + self.data['player'] + '&zone=' + self.data['zone']

        req = request.Request(req_url)
        req.add_header(self.user_agent[0], self.user_agent[1])

        with request.urlopen(req) as f:
            got_json = json.loads(f.read().decode('utf-8'))
            self.data['aid'] = got_json['account_db_id']
            self.data['name'] = got_json['nick']
            print('Aid of User \'%s\' is %s' % (self.data['name'], self.data['aid']))

    def get_data_info(self):
        req_url = self.usr_get_data_info + '?aid=' + self.data['aid']

        req = request.Request(req_url)
        req.add_header(self.user_agent[0], self.user_agent[1])

        with request.urlopen(req) as f:
            self.data['ship_json'] = json.loads(f.read().decode('utf-8'))
            #print(self.data['ship_json'])

    def input_player(self, name, zone):
        self.data['player'] = name
        self.data['zone'] = zone

        self.get_user_info()
        self.get_data_info()

        req_url = self.url + '?name=' + self.data['player'] + '&zone=' + self.data['zone']

        req = request.Request(req_url)
        req.add_header(self.user_agent[0], self.user_agent[1])

        with request.urlopen(req) as f:
            self.data['data'] = f.read()
            print('Status:', f.status, f.reason)
            self.soup_match()

    def soup_match(self):
        soup = BeautifulSoup(self.data['data'], 'html.parser', from_encoding='utf-8')
        content = soup.find('div', id='total').findAll('span', {'class': 'value'})
        for i in content:
            print(i.string)


if __name__ == '__main__':
    crawler = CrawlerOfWOWS()
    # name = input('玩家昵称:')
    input_name = 'pnq-Ar196-欧根亲王'
    url_name = parse.quote(input_name)
    # zone = input('分区：')
    input_zone = 'south'
    crawler.input_player(url_name, input_zone)