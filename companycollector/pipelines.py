# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
from scrapy.exceptions import DropItem
from models import CompanySection, CompanySubSection
from companycollector.items import SectionItem, LegalEntityItem
from companycollector.utils import CompaniesBuffer


class SectionsPipeline(object):
    collection_name = 'sections_items'

    def __init__(self):
        pass

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        if isinstance(item, SectionItem):
            if re.match('[A-Z]+', item['code']):
                CompanySection.get_or_create(name=item['name'], url=item['url'], code=item['code'])
            else:
                if item['section_companies_count']:
                    CompanySubSection.get_or_create(name=item['name'], url=item['url'],
                                                    code=item['code'],
                                                    companies_count=item['section_companies_count'],
                                                    section=item['parent_code'])
                else:
                    raise DropItem("Missing section_companies_count in %s" % item)
        return item


class LegalEntitiesPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, LegalEntityItem):
            buffer = CompaniesBuffer()
            buffer.add_item(item)
        return item