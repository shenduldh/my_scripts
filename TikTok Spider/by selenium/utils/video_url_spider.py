import requests
from json import loads
import re
from time import sleep as wait

from .user_agent import UserAgent


def video_url_spider(tiktok_shares: list,
                     video_saved_path: str = './video_urls.txt',
                     is_use_proxy=False,
                     proxies=None,
                     wait_second=3):
    url_to_get_api = 'http://i.rcuts.com/update/249'
    res = requests.get(url_to_get_api,
                       headers={'User-Agent': UserAgent.iphone_safari})
    res = loads(res.text)
    api_url = res['api']

    total = len(tiktok_shares)
    proxy_count = len(proxies)
    proxy = proxies.pop()
    print('-' * 20 + ' Video URL Crawling ' + '-' * 20)
    with open(video_saved_path, 'a', encoding='utf-8') as log:
        for i, tiktok_share in enumerate(tiktok_shares):
            match = re.search(r'https://v.douyin.com/[a-zA-Z0-9]+?/',
                              tiktok_share)
            tiktok_url = match.group(0)
            headers = {'User-Agent': UserAgent.iphone_safari}
            body_data = {
                'url': tiktok_url,
                'token': api_url,
                'clipboard': tiktok_share,
            }

            if is_use_proxy:
                while proxy_count > 0:
                    try:
                        res = requests.post(api_url,
                                            data=body_data,
                                            headers=headers,
                                            proxies=proxy)
                        break
                    except:
                        proxy = proxies.pop()
                        proxy_count -= 1
            else:
                res = requests.post(api_url, data=body_data, headers=headers)

            res = loads(res.text)
            video_url = res['video_url']
            video_name = res['video_name']
            nickname = res['nickname']

            log.write('%s|--|%s|--|%s|--|0\n' %
                      (nickname, video_name, video_url))

            wait(wait_second)

            if i < total - 1:
                print('progress: %.1f\r' % ((i + 1) * 100 / total), end='')
            else:
                print('progress: %.1f' % ((i + 1) * 100 / total))
    print('Crawling finish.')


if __name__ == '__main__':
    tiktok_shares = [
        '0.23 DhB:/ 外交部回应蓬佩奥与蔡英文会面：有关行径无耻且徒劳。  https://v.douyin.com/N86W6gS/ 复制此链接，打开Dou音搜索，直接观看视频！'
    ]
    video_url_spider(tiktok_shares,
                     proxies=[{
                         'http': 'http://217.69.176.207:80'
                     }])
