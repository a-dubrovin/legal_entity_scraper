# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SectionItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    code = scrapy.Field()
    parent_code = scrapy.Field()
    section_companies_count = scrapy.Field()


class LegalEntityItem(scrapy.Item):
    pk = scrapy.Field()
    short_name = scrapy.Field()
    full_name = scrapy.Field()
    company_type = scrapy.Field()
    registration_date = scrapy.Field()
    section_code = scrapy.Field()

    director = scrapy.Field()
    authorized_capital = scrapy.Field()
    personnel_count = scrapy.Field()
    founders_count = scrapy.Field()
    status = scrapy.Field()

    zipcode = scrapy.Field()
    address = scrapy.Field()
    legal_address = scrapy.Field()
    email = scrapy.Field()
    site = scrapy.Field()
    phone = scrapy.Field()
    fax = scrapy.Field()
    gps_coordinates = scrapy.Field()

    inn = scrapy.Field()
    kpp = scrapy.Field()
    okpo = scrapy.Field()
    ogrn = scrapy.Field()
    okfc = scrapy.Field()
    okogu = scrapy.Field()
    okopf = scrapy.Field()
    okato = scrapy.Field()
    fsfr = scrapy.Field()
    main_activity = scrapy.Field()
    description = scrapy.Field()