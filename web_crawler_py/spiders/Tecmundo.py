# -*- coding: utf-8 -*-
import uuid
import scrapy
from scrapy.utils.markup import remove_tags
from web_crawler_py.items import NoticiasItem


class TecmundoSpider(scrapy.Spider):
    name = 'Tecmundo'
    allowed_domains = ['tecmundo.com.br']
    start_urls = ['http://tecmundo.com.br/']

    def parse(self, response):
        for article in response.css("div.tec--container article"):
            link = article.css("div.tec--card__info div.tec--card__title a::attr(href)").extract_first()
            # title = article.css("div.tec--card__info div.tec--card__title a::text").extract_first()
            # image = article.css("figure img::attr(data-src)").extract_first()

            if link:
                yield response.follow(link, self.parse_article)

    @staticmethod
    def parse_article(response):
        link = response.url
        title = response.css("title ::text").extract_first()
        author = response.css("div.tec--container div.tec--article__body-grid div.tec--author__info p a::text").extract_first()
        image = response.css("div.tec--container div.tec--article__header-grid header figure img::attr(data-src)").extract_first()
        # text = response.css("div.tec--container div.tec--article__body p::text").getall()
        text = response.css("div.tec--container div.tec--article__body").getall()

        if text:
            text = text[0][:text[0].find("<p><span>Cupons")]
            text = remove_tags(text)
            text = text.replace('</div', '')

        notice = NoticiasItem(title=title, author=author, text=text, link=link, image=image, source="Tecmundo",
                              uuid=str(uuid.uuid4()))
        yield notice
