import requests

from .user_agent import UserAgent


def downloader(urls: list, saved_dir_path='./videos'):
    print('-'*20 + ' Downloading '+'-'*20)
    for url in urls:
        file_name = url[0]+'.mp4'
        res = requests.get(url[1], stream=True, headers={
            'User-Agent': UserAgent.pc_chrome})
        with open(saved_dir_path+'/'+file_name, 'wb') as f:
            for chunk in res.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

        print("%s is OK." % file_name)
    print("All videos are downloaded.")


if __name__ == '__main__':
    downloader([('test', 'https://v26-web.douyinvod.com/5d1c27d4e6aa5a35aeff6c6fb20b9996/6221c768/video/tos/cn/tos-cn-ve-15/aa908a9fa0aa4790bef9dc60ae9314a1/?a=6383&br=705&bt=705&cd=0%7C0%7C0%7C0&ch=26&cr=0&cs=0&cv=1&dr=0&ds=3&er=&ft=VgcwUVIIL7ThWHrYvO2GZ&l=021646377076607fdbddc0200ff2f010a2e588c0000003e2ed25c&lr=all&mime_type=video_mp4&net=0&pl=0&qs=0&rc=M2ptMzU6Zjo2NzMzNGkzM0ApNDo2MzlpZmU5N2Y5aGQ1O2djc281cjQwal9gLS1kLS9zczNfY2AvXl5gYy1gMWJjYTM6Yw%3D%3D&vl=&vr=')])
