import json
import requests
import re
from bs4 import BeautifulSoup
import urllib.parse
import urllib.request
import os.path


IMG_BASE_URL = 'https://miro.medium.com/max/1200/'


def ensure_file_extension(filename):
    if not (filename.endswith(".jpg") or filename.endswith(".jpg") or filename.endswith(".jpg")):
        print("Turning " + filename + " into " + filename + ".jpg")
        return filename + ".jpg"
    return filename


def parse(data):
    """
        Parses the raw JSON data from Medium post pages to our own format.

        Parameters:
        data (dict): JSON data for a Medium post

        Returns:
        dict: {
            'title': 'title',
            'subtitle': 'subtitle',
            'paragraphs': [
                {
                    'type': 'P',  # 'H3', 'H4', 'IMG', 'ULI', 'OLI', 'BQ'
                    'text': 'text',  # Only used for text paragraphs
                    'markups': [
                        {
                            'type': 'STRONG',  # 'EM', 'A'
                            'start': 0,
                            'end': 0
                        }
                    ],  # Only used for text paragraphs
                    'img_filename': 'img_filename'  # Only used for the IMG paragraphs
                }
            ]
        }
    """
    paragraph_list = []
    markup_dict = {}
    for k, p in data.items():
        if p.get('__typename', '') == 'Paragraph':
            paragraph_list.append(p)
        if p.get('__typename', '') == 'Markup':
            markup_dict[k] = p

    paragraphs = []
    for p in paragraph_list:
        paragraph_type = p['type']
        if paragraph_type == 'IMG':
            img_filename = p['metadata']['id'].split('ImageMetadata:')[1]
            if os.path.isfile(img_filename):
                print("Image already existed: " + img_filename)
            else:
                print("Downloading... " + IMG_BASE_URL + img_filename)
                # Medium returns 403 for the default user-agent
                opener = urllib.request.build_opener()
                opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4)\
                        AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36')]
                urllib.request.install_opener(opener)
                local_filename = ensure_file_extension(img_filename)
                urllib.request.urlretrieve(IMG_BASE_URL + img_filename, local_filename)
            paragraphs.append({'type': paragraph_type, 'img_filename': local_filename})
        else:
            text = p['text']
            markups = []
            for markup_reference in p['markups']:
                markup = markup_dict[markup_reference['id']]
                start = markup['start']
                end = markup['end']
                markup_type = markup['type']
                markups.append({'type': markup_type, 'start': start, 'end': end})
            paragraphs.append({'type': paragraph_type, 'text': text, 'markups': markups})

    # Medium treats the first block of type 'H3' as Title.
    # If Title is followed by a block of type 'H4', the 'H4' is considered subtitle.
    title = None
    subtitle = None
    for idx in range(len(paragraphs)):
        p = paragraphs[idx]
        if p['type'] == 'H3':
            title = p['text']
            paragraphs.pop(idx)
            if idx < len(paragraphs) and paragraphs[idx]['type'] == 'H4':
                subtitle = paragraphs[idx]['text']
                paragraphs.pop(idx)
            break

    return {
        'title': title,
        'subtitle': subtitle,
        'paragraphs': paragraphs
    }


def crawl_medium(url):
    page = requests.get(url)
    if page.status_code != 200:
        raise Exception('Failed to open the URL')

    soup = BeautifulSoup(page.text, 'html.parser')

    # HTML format required:
    # <script>window.__APOLLO_STATE__ = {...json data...}</script>
    script_tags = soup.find_all('script', string=re.compile('__APOLLO_STATE__'))
    if len(script_tags) != 1:
        raise Exception('Can not find the content. The output HTML structure might have changed')

    json_data = script_tags[0].string.split('__APOLLO_STATE__ = ')[1].split('</script>')[0]
    return parse(json.loads(json_data, encoding='utf-8'))
