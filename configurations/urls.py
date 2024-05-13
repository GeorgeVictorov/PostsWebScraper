import random

page = random.choice(range(1, 25))
TRV_URL: str = 'https://www.trv-science.ru/category/edu/page/{}'.format(page)
