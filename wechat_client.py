import json
import requests
from settings import SETTINGS


def get_access_token():
    response = requests.get(
        'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (
            SETTINGS['account_id'], SETTINGS['secret_key']))
    if response.status_code != 200:
        raise Exception('Failed to get access token')
    return json.loads(response.text)['access_token']


def upload_image(img_filename):
    files = {'media': open(img_filename, 'rb')}
    response = requests.post(
        'https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=' + get_access_token(),
        files=files)
    if response.status_code != 200:
        raise Exception('Failed to upload image ' + img_filename)
    return json.loads(response.text)['url']


def upload_article(article):
    title = article['title']
    content = article['content']
    author = '人生经理Charlene'
    thumb_media_id = 'Tbt5DXSqC3bfid5UxqErjLRd9i4NQfbQSaTu73gTVYs'  # lifecoachbanner
    post_url = 'https://api.weixin.qq.com/cgi-bin/material/add_news?access_token=' + get_access_token()
    post_body = {
        "articles": [{
            "title": title,
            "thumb_media_id": thumb_media_id,
            "author": author,
            "show_cover_pic": 0,
            "content": content,
            "content_source_url": '',
        },
        ],
    }
    headers = {"Content-type": "application/json", "charset": "UTF-8"}
    response = requests.post(post_url, data=bytes(json.dumps(post_body, ensure_ascii=False), encoding='utf-8'),
                             headers=headers)
    print('Article upload: ' + response.text)
