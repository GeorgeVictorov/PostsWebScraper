import random

page = random.choice(range(1, 25))

TRV_URL: str = 'https://www.trv-science.ru/category/edu/page/{}'.format(page)

VLG_URL: str = 'https://www.the-village.ru/posts/weekend'

DLT_URL: str = 'https://diletant.media/rss/articles/'

API_URL = 'https://nitrojamrec.ru/api/v1/posts'
