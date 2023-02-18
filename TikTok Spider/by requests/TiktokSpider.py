import requests
import traceback
import re


def request(url, allow_redirects=True):
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36 Edg/87.0.664.66',
        'Referer': 'https://www.douyin.com/',
    }
    cookies = {
        'msToken':
        'tsQyL2_m4XgtIij2GZfyu8XNXBfTGELdreF1jeIJTyktxMqf5MMIna8m1bv7zYz4pGLinNP2TvISbrzvFubLR8khwmAVLfImoWo3Ecnl_956MgOK9kOBdwM=',
        'odin_tt':
        '6db0a7d68fd2147ddaf4db0b911551e472d698d7b84a64a24cf07c49bdc5594b2fb7a42fd125332977218dd517a36ec3c658f84cebc6f806032eff34b36909607d5452f0f9d898810c369cd75fd5fb15',
        'ttwid':
        '1%7CfhiqLOzu_UksmD8_muF_TNvFyV909d0cw8CSRsmnbr0%7C1662368529%7C048a4e969ec3570e84a5faa3518aa7e16332cfc7fbcb789780135d33a34d94d2'
    }
    res = requests.get(
        url=url,
        headers=headers,
        cookies=cookies,
        allow_redirects=allow_redirects,
    )
    return res


def get_share_url(share_text):
    match = re.search(r'https://v.douyin.com/\S+?/', share_text)
    if match is None:
        return None
    return match.group(0)


def get_uid(share_url):
    res = request(share_url).url
    uid = re.findall('/video/(.*?)/', res)[0]
    return uid


def get_src_json(uid):
    src_url = 'https://www.iesdouyin.com/aweme/v1/web/aweme/detail/?aweme_id={}&aid=1128&version_name=23.5.0&device_platform=android&os_version=2333&Github=Evil0ctal&words=FXXK_U_ByteDance'.format(
        uid)
    src_json = request(src_url).json()['aweme_detail']
    return src_json


def get_video_url(src_json):
    raw_url_list = src_json["video"]["play_addr"]["url_list"]
    return raw_url_list[0]


def get_images_url(src_json):
    url_list = []
    raw_images = src_json["images"]
    for img in raw_images:
        url_list.append(img['url_list'][0])
    return url_list


def spider(share_text):
    try:
        share_url = get_share_url(share_text)
        if share_url is None:
            return None
        print(share_url)
        uid = get_uid(share_url)
        print(uid)
        src_json = get_src_json(uid)
        if src_json is None:
            return {'is_error': True, 'error_msg': 'src_json is None'}
        if src_json["images"] is None:
            return {
                'is_error': False,
                'is_images': False,
                'video_url': get_video_url(src_json)
            }
        return {
            'is_error': False,
            'is_images': True,
            'images_url': get_images_url(src_json)
        }

    except:
        return {'is_error': True, 'error_msg': traceback.format_exc()}


if __name__ == "__main__":
    images_share_text = '0.51 foQ:/ 新年快乐🎆🎉。# 10后 # 185大帅哥 # 少年感 # 骗你生儿子  https://v.douyin.com/kB41ebQ/ 复制此链接，打开Dou音搜索，直接观看视频！'
    video_share_text = '4.61 MJv:/ 他本是隐世高手，却受尽欺辱，十八分钟看完甄子丹《武侠》 # 大片即视感 # 我的观影报告  https://v.douyin.com/kkkAa2E/ 复制此链接，打开Dou音搜索，直接观看视频！'

    print(spider(images_share_text))
