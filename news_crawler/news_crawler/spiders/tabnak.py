import scrapy
import json
import hashlib

class TabnakSpider(scrapy.Spider):
    name = "tabnak"
    directory = 'news/'
    start_urls = json.load(open('tabnak_urls.json'))

    def parse(self, response):
        title = response.css('div.title').css('h1').css('a::text').get().strip()
        news = {'url': response.request.url,'title': title}
        try:
            subtitle = response.css('div.subtitle::text')[1].get()
            news['subtitle'] = subtitle
        except Exception as e:
            print('subtitle:\n',e)
        try:
            body = response.css('div.body').css('p::text')
            if len(body) == 0:
                body = response.css('div.body').css('div::text')
            body = [p.get() for p in body]
            news['body'] = body
        except Exception as e:
            print('body:\n',e)
        filename = hashlib.md5(title.encode()).hexdigest()
        json.dump(news, open(self.directory+filename+'.json','w'))