from crawler import crawl_medium
from composer import compose
from wechat_client import upload_image, upload_article
import styler
import footer_decorator
import zh_converter

# url = 'https://bit.ly/eating-social-tactics'
url = 'https://bit.ly/eating-amaz'
article_data = crawl_medium(url)
article = compose(article_data, upload_image, styler, footer_decorator, [zh_converter])
# article = compose(article_data, lambda i: '', styler, footer_decorator, [zh_converter])
upload_article(article)
