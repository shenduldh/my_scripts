from utils import video_url_spider, ShareSpider, downloader
from config import CONFIG


share_spider = ShareSpider(CONFIG.start_url, CONFIG.driver_name, CONFIG.driver_path, CONFIG.spider_duration,
                           CONFIG.next_after_second, shares_saved_path=CONFIG.shares_saved_path)
share_spider.run()


# with open('shares.txt', 'r', encoding='utf-8') as f:
#     share_msgs = f.read()
# share_msgs = share_msgs.split('\n')
# video_url_spider(share_msgs, CONFIG.video_saved_path,
#                  CONFIG.is_use_proxy, CONFIG.proxies, CONFIG.wait_second)


# with open('video_urls.txt', 'r', encoding='utf-8') as f:
#     share_msgs = f.read()
# share_msgs = [i.split('|--|') for i in share_msgs.split('\n')]
# urls = [(i[1], i[2]) for i in share_msgs if len(i) == 4]
# downloader(urls, CONFIG.saved_dir_path)
