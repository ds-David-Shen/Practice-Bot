import requests
import bs4 as bs
from time import time


class UserSuggester(object):

    def __init__(self, handle):
        self.handle = handle
        self.points_min = 1
        self.points_max = 50
        self.update_pp_range()
        self.expand_up = True
    
    def update_pp_range(self):
        response = requests.get('https://dmoj.ca/user/%s/solved' % self.handle)
        if response.status_code != 200:
            return
        self.time = time()
        soup = bs.BeautifulSoup(response.text, 'lxml')
        points = soup.findAll('div', attrs={'class': 'pp'})
        if len(points) == 0:
            self.points_min = 1
            self.points_max = 3
            return
        points_len = min(len(points), 30)

        def point_to_int(point):
            return int(point.find('a').contents[0].replace('p', ''))

        self.points_max = 2*sum(map(point_to_int, points[0:points_len//2]))//points_len
        self.points_min = 2*sum(map(point_to_int, points[points_len//2:points_len]))//points_len

    def get_pp_range(self):
        return tuple(map(str, (self.points_min, self.points_max)))

    def expand_pp_range(self):
        if self.points_max != 50 and self.expand_up:
            self.points_max = min(self.points_max+2, 50)
            self.expand_up = False
        else:
            self.points_min = max(0, self.points_min-1)
            self.expand_up = True
