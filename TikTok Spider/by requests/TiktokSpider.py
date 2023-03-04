import requests
import traceback
import re
import json
import sys


# 从浏览器控制台获取, 粘贴在此处即可
headerCookie = "__ac_nonce=06402dd0000da91aec05c; __ac_signature=_02B4Z6wo00f01jurmhgAAIDDsv4z-s1LPCI7i56AAOr2soZhC7xn7i3P7xj6s3Whltq4pHh6dzXwb.CBBbLwXNM7ycZtEf6L5NDAM-wCEhcaYtyNpkzCAYPu5578tAv3pUwxFZg1UmU24FVs73; ttwid=1%7C7xnnPBJbHwZV_wOrvtbB77nxTlo4-_zQyWiOzRx0LdA%7C1677909248%7C0e1ae864da3e0eea91aa5a177cf712258c76e4b848579bcc6704b27c31b1e13a; home_can_add_dy_2_desktop=%220%22; strategyABtestKey=%221677909266.305%22; s_v_web_id=verify_letjusmj_c8HwyH5w_u0KB_4Rg9_AYRT_TU6idjVx3lzq; bd_ticket_guard_client_data=eyJiZC10aWNrZXQtZ3VhcmQtdmVyc2lvbiI6MiwiYmQtdGlja2V0LWd1YXJkLWNsaWVudC1jc3IiOiItLS0tLUJFR0lOIENFUlRJRklDQVRFIFJFUVVFU1QtLS0tLVxyXG5NSUlCRFRDQnRRSUJBREFuTVFzd0NRWURWUVFHRXdKRFRqRVlNQllHQTFVRUF3d1BZbVJmZEdsamEyVjBYMmQxXHJcbllYSmtNRmt3RXdZSEtvWkl6ajBDQVFZSUtvWkl6ajBEQVFjRFFnQUVabEh3SDVIRUhPSTZ1QXYrTjd5S2s5NUdcclxuMVZMRGpqaThrM1QwNGhrZGNrMHQrSWtPdDQzRjVFbjloUS9pM0pWcHRWajN3UGtjVGZ6LzcxNlVyb1EyRUtBc1xyXG5NQ29HQ1NxR1NJYjNEUUVKRGpFZE1Cc3dHUVlEVlIwUkJCSXdFSUlPZDNkM0xtUnZkWGxwYmk1amIyMHdDZ1lJXHJcbktvWkl6ajBFQXdJRFJ3QXdSQUlnWDNsNmJHZlMzRlIraUdONGFKY0FFZXhhNGpncGFtcEtDWFY0a2FNaXJJb0NcclxuSUNtTzE0Y211bFhLL08rNlFiT09RQVV4eVlLWXRZS01iZXg4RVphYkhmWUtcclxuLS0tLS1FTkQgQ0VSVElGSUNBVEUgUkVRVUVTVC0tLS0tXHJcbiJ9; passport_csrf_token=ee2f55e87576702c5dfd8578b423c9eb; passport_csrf_token_default=ee2f55e87576702c5dfd8578b423c9eb; msToken=u7mRzpRU1hYUq6GcylKuCT0UFi4F4iJXHUbIcN6Zzwsid05bKxya32sM3wdvyqh5cxaU5be_VIXJ5wjzfBJYmu6oQQ2VQeWmTT-a4DCN37AvWpRG1Lmk; msToken=gMKdwSrlpQ4jzi9ikh_0lkUffcVfi0xq_zIw7nGnDbHe9h5S_bHRPy1ln2ePj5kIE8ZM1qUjEoFOpCbaGh8Cg5uE2gw6fArSDWTVmct7OyvwZNkx2JT3n7vfSehnbw=="
userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"

# 从分享内容中提取分享链接
def get_share_url(share_text):
    match = re.search(r"https://v.douyin.com/\S+?/", share_text)
    if match is None:
        return None
    return match.group(0)


# 从分享链接的重定向链接中提取 uid
def get_uid(share_url):
    res = requests.get(
        url=share_url,
        allow_redirects=True,
    ).url
    uid = re.findall("/video/(.*?)/", res)[0]
    return uid


# 根据 uid 获取信息
# NOTE 接口失效时需要重写
def get_info(uid):
    # 获取 mstoken, ttwid 和 url
    res = requests.post(
        url="https://tiktok-signature-inky.vercel.app/",
        headers={ "Content-Type": "application/json" },
        data=json.dumps({
            "url": "https://www.douyin.com/aweme/v1/web/aweme/detail/?aweme_id={}&aid=1128&version_name=23.5.0&device_platform=android&os_version=2333".format(uid),
            "userAgent": userAgent,
        }),
    ).json()
    mstoken = res['data']['mstoken']
    ttwid = res['data']['ttwid']
    url = res['data']['url']
    
    # 获取 uid 
    res = requests.get(
        url = url,
        headers={
            'User-Agent':userAgent,
            'Referer':'https://www.douyin.com/',
            'cookie': headerCookie,
        },
        cookies={
            'mstoken': mstoken,
            'ttwid': ttwid,
        }
    ).json()
    return res['aweme_detail']


def get_video_url(info):
    raw_url_list = info["video"]["play_addr"]["url_list"]
    return raw_url_list[0]


def get_images_url(info):
    url_list = []
    raw_images = info["images"]
    for img in raw_images:
        url_list.append(img["url_list"][0])
    return url_list


def spider(share_text):
    try:
        share_url = get_share_url(share_text)
        if share_url is None:
            raise Exception("No share url in the content.")
        # print(share_url)

        uid = get_uid(share_url)
        # print(uid)

        info = get_info(uid)
        if info["images"] is None:
            return {
                "is_error": False,
                "is_images": False,
                "desc": info['desc'],
                "video_url": get_video_url(info),
            }
        return {
            "is_error": False,
            "is_images": True,
            "desc": info['desc'],
            "images_url": get_images_url(info),
        }
    except:
        return {"is_error": True, "error_msg": traceback.format_exc()}


def test():
    images_share_text = "2.07 VyG:/ 我又来放图集啦～还有你们要的小可爱大图也放啦～# 原创插画 # 寻找古籍守护人 # 全民晒书 # 山海经   https://v.douyin.com/SkryPed/ 复制此链接，打开Dou音搜索，直接观看视频！"
    video_share_text = "4.61 MJv:/ 他本是隐世高手，却受尽欺辱，十八分钟看完甄子丹《武侠》 # 大片即视感 # 我的观影报告  https://v.douyin.com/kkkAa2E/ 复制此链接，打开Dou音搜索，直接观看视频！"
    print(spider(images_share_text))
    print(spider(video_share_text))


def runByShortCut():
    share_text = sys.argv[1]
    res = json.dumps(spider(share_text))
    print(res) # return data by print


runByShortCut()
