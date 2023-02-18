class CONFIG:
    # ShareSpider args
    start_url = 'https://www.douyin.com/video/6995844232653163806'
    driver_name = 'Edge'
    driver_path = 'msedgedriver.exe'
    spider_duration = 60*60*24*2
    next_after_second = 3
    shares_saved_path = './shares.txt'

    # video_url_spider args
    video_saved_path = './video_urls.txt'
    is_use_proxy = True
    # https://ip.jiangxianli.com/?page=1
    proxies = [{'http': 'http://217.69.176.207:80'}]
    wait_second = 3

    # dowloader args
    saved_dir_path = './videos'
