# -*- coding: utf-8 -*-
import re
import urllib.parse
import scrapy
from companycollector.items import SectionItem
import settings


class SectionsSpider(scrapy.Spider):
    name = 'sections_spider'
    rotate_user_agent = True
    start_urls = [
        urllib.parse.urljoin(settings.SITE_URL, 'okved.php'),
    ]

    def parse(self, response):
        section_urls = []
        for section in response.xpath('//div[@class="content"]//a[contains(@href,"okved")]/..'):
            section_url = section.xpath('a/@href').extract_first()
            if section_url:
                item = SectionItem()
                item['name'] = section.xpath('a/text()').extract_first()
                item['url'] = section_url
                item['code'] = section_url.split('=')[-1]
                section_companies_count = section.xpath('text()[2]').extract_first()
                item['section_companies_count'] = section_companies_count.strip(')( ') if section_companies_count else None
                print(item)
                if re.match('[A-Z]+', item['code']):
                    section_urls.append(urllib.parse.urljoin(settings.SITE_URL, section_url))
                if re.match('[0-9.]+', item['code']):
                    item['parent_code'] = response.url.split('=')[-1]

                yield item

        for section_url in section_urls:
            yield scrapy.Request(section_url, callback=self.parse)