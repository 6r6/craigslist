# encoding: utf-8
# last_modified: 2020/3/10

import re
import requests

craigslist_cookies = {
    'cl_b': '4|6cf80008dcffd9a21c9c8d525300740a33004a7f|1583805322nEg-8',
    'cl_def_hp': 'toronto',
    'cl_tocmode': 'hhh%3Agrid',
    'cl_session': 'H500n2PTDvNR9MAJj2bfsDTo0000JY5mEvVlYN33m2JtCMaDAUqxNOufp2X00k2s',
    'cl_login': '1'
}


class Craigslist:

    def __init__(self, cookies):
        self.headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'DNT': '1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.37 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36 Edg/81.0.360.55',
            'Sec-Fetch-Dest': 'document',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'X-Forwarded-For': '208.82.237.6',
        }
        self.cookies = cookies

    @staticmethod
    def get_cryptedStepCheck(html_raw):
        try:
            # subarea type page 
            cryptedStepCheck = re.findall(
                r'cryptedStepCheck" value="(.\S+)"', html_raw)[0]
            return cryptedStepCheck
        except:
            # hcat page
            raw_line = html_raw.split('cryptedStepCheck')[1]
            cryptedStepCheck = raw_line.lstrip('"\n  value="').rstrip('"\n  class="')
            return cryptedStepCheck

    @staticmethod
    def get_params(x):
        """
        step1 n = 1 means Toronto
        step2 id = ho means housing
        step3 id = 18 means rooms&shares
        """
        return{
            'subarea': {'n': 1},
            'type': {'id': 'ho'},
            'hcat': {'id': 18},
        }.get(x, 0)

    def login(self):
        """
        in cookies-existed mode , login is not necessary
        success = True of False
        """
        login_url = 'https://accounts.craigslist.org/login/home'
        r = requests.get(login_url, headers=self.headers, cookies=self.cookies)
        success = 'billing' in r.text
        return success

    def creat_post(self):
        """
        path is like /k/ELIJkH1nnhGNt8z3PIyhDw/A4c6e
        """
        creat_post_url = 'https://post.craigslist.org/c/tor'
        r = requests.get(creat_post_url, headers=self.headers,
                         cookies=self.cookies, allow_redirects=False)
        path = r.headers.get('Location')
        return path

    def set_params(self, path, param_type):
        """
        n = 1 means Toronto
        success = True of False
        """
        subarea_url = 'https://post.craigslist.org' + path
        params_dict = Craigslist.get_params(param_type)
        params = {'s':param_type}
        r = requests.get(subarea_url, headers=self.headers,
                         params=params, cookies=self.cookies)
        cryptedStepCheck = Craigslist.get_cryptedStepCheck(r.text)
        print('cryptedStepCheck(csrf-token):' + cryptedStepCheck)
        params_dict['cryptedStepCheck'] = cryptedStepCheck
        r = requests.post(subarea_url, headers=self.headers, params=params,
                          data=params_dict, cookies=self.cookies)
        success = 'logged in as' in r.text
        return success


if __name__ == "__main__":
    account1 = Craigslist(craigslist_cookies)
    # print(account1.login())
    post_path = account1.creat_post()
    print('generated a new post: ' + post_path)
    print(account1.set_params(post_path, 'subarea'))
    print('subarea setted')
    print(account1.set_params(post_path, 'type'))
    print('type setted')
    print(account1.set_params(post_path, 'hcat'))
    print('hcat setted')
