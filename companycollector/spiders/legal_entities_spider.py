# -*- coding: utf-8 -*-
import re

import urllib.parse
import scrapy
from scrapy.http.request import Request
from companycollector.items import LegalEntityItem
import settings
from models import CompanySubSection


class LegalEntitiesSpider(scrapy.Spider):
    name = 'legal_entities_spider'
    rotate_user_agent = True
    start_urls = []

    def start_requests(self):
        for section in CompanySubSection.get_unparsed_sections():
            for page_num in range(section.max_parsed_page+1, section.get_max_page()+1):
                yield Request(urllib.parse.urljoin(settings.SITE_URL, '%s&page=%s' % (section.url, page_num)), self.parse)

    def parse(self, response):
        print(response.url)
        for url in response.xpath('//div[@class="org_list"]//a/@href').extract():
            request = Request(urllib.parse.urljoin(settings.SITE_URL, url), self.parse_company)
            request.meta['section'] = response.url.split('=')[-1]
            yield request

    def parse_company(self, response):
        print(response.url)
        item = LegalEntityItem()

        item['pk'] = response.url.split('/')[-1]
        item['short_name'] = response.xpath('//h1/text()').extract()
        item['full_name'] = response.xpath('//p/*[contains(text(), "Полное юридическое наименование:")]/../a/text()').extract()
        item['company_type'] = 'Unknown'
        item['registration_date'] = response.xpath('//td/*[contains(text(), "Дата внесения в реестр")]/../following-sibling::td/text()').extract()
        item['section_code'] = response.meta['section']

        item['director'] = response.xpath('//td/*[contains(text(), "Руководитель")]/../following-sibling::td/*/text()').extract()
        item['authorized_capital'] = response.xpath('//td/*[contains(text(), "Уставной капитал")]/../following-sibling::td/text()').extract()
        item['personnel_count'] = response.xpath('').extract()
        item['founders_count'] = response.xpath('//td/*[contains(text(), "Количество учредителей")]/../following-sibling::td/text()').extract()
        item['status'] = response.xpath('//td/*[contains(text(), "Статус")]/../following-sibling::td/text()').extract()

        item['zipcode'] = response.xpath('//*[contains(text(), "Индекс")]/../text()').extract()
        item['address'] = response.xpath('//*[contains(text(), "Адрес")]/following-sibling::*/text()').extract()
        item['legal_address'] = response.xpath('//*[contains(text(), "Юридический адрес")]/following-sibling::*/text()').extract()
        item['email'] = ', '.join(response.xpath('//i[contains(text(), "Эл.почта (e-mail):")]/ancestor::p/a/text()').extract_all())
        item['site'] =  ', '.join(response.xpath('//i[contains(text(), "Сайт (www)")]/ancestor::p/a[contains(@href, "go.php?site=")]/text()').extract_all())
        item['phone'] = ', '.join(response.xpath('//i[contains(text(), "Телефон:")]/ancestor::p/a[contains(@href, "search.php?type=phone")]/text()').extract_all())
        item['fax'] = ', '.join(response.xpath('//i[contains(text(), "Факс:")]/ancestor::p/a[contains(@href, "go.php?site=")]/text()').extract_all())

        item['gps_coordinates'] = response.xpath('//a[contains(@href, "companies_on_map")]/text()').extract()

        item['inn'] = response.xpath('//p/*[contains(text(), "ИНН")]/../text()').extract()
        item['kpp'] = response.xpath('//p/*[contains(text(), "КПП")]/../text()').extract()
        item['okpo'] = response.xpath('//*[contains(text(), "ОКПО")]/ancestor::p/span/text()').extract()
        item['ogrn'] = response.xpath('//*[contains(text(), "ОГРН")]/ancestor::p/text()').extract()
        item['okfc'] = response.xpath('//*[contains(text(), "ОКФС")]/ancestor::p/text()').extract()
        item['okogu'] = response.xpath('//*[contains(text(), "ОКОГУ")]/ancestor::p/text()').extract()
        item['okopf'] = response.xpath('//*[contains(text(), "ОКОПФ")]/ancestor::p/text()').extract()
        item['oktmo'] = response.xpath('//*[contains(text(), "ОКТМО")]/ancestor::p/text()').extract()
        item['okato'] = response.xpath('//*[contains(text(), "ОКАТО")]/ancestor::p/a/text()').extract()
        item['fsfr'] = response.xpath('//*[contains(text(), "ФСФР")]/ancestor::p/a/text()').extract()
        item['main_activity'] = response.xpath('//*[contains(text(), "Основной")]/ancestor::p/a/text()').extract()
        item['description'] = response.xpath('//div[@class="content"]/p[contains(text(), "Организация ")]/text()').extract()
