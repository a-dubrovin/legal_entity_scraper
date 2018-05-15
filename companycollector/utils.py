# -*- coding: utf-8 -*-
import scrapy
from models import LegalEntity, ParsedPages

class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        pass


class CompaniesBuffer(Singleton):

    buffer = {}

    def __init__(self):
        pass

    def add_item(self, item):
        if isinstance(item, scrapy.Item):
            if not item['section'] in self.buffer:
                self.buffer[item['section']] = {}

            if not item['page'] in self.buffer[item['section']]:
                self.buffer[item['section']][item['page']] = {'items': [], 'quantity': item['page_quantity']}

            self.buffer[item['section']][item['page']]['items'].append(item)

            if len(self.buffer[item['section']][item['page']]['items']) == self.buffer[item['section']][item['page']]['page_quantity']:
                if self.save_page(item['section'], item['page'], item['page_quantity']):
                    self.buffer[item['section']].pop(item['page'], None)
        else:
            raise TypeError('item must be instance of scrapy.Item')

    def save_page(self, section, page, quantity):
        data_list = []
        for item in self.buffer[section][page]['items']:
            data_list.append((
                item['pk'],
                item['short_name'],
                item['full_name'],
                item['company_type'],
                item['registration_date'],
                item['section_code'],

                item['director'],
                item['authorized_capital'],
                item['personnel_count'],
                item['founders_count'],
                item['status'],

                item['zipcode'],
                item['address'],
                item['legal_address'],
                item['email'],
                item['site'],
                item['phone'],
                item['fax'],
                item['gps_coordinates'],

                item['inn'],
                item['kpp'],
                item['okpo'],
                item['ogrn'],
                item['okfc'],
                item['okogu'],
                item['okato'],
                item['fsfr'],
                item['main_activity'],
                item['description'],
            ))
        fields = [
            LegalEntity.pk,
            LegalEntity.short_name,
            LegalEntity.full_name,
            LegalEntity.company_type,
            LegalEntity.registration_date,
            LegalEntity.sub_section,
            LegalEntity.director,
            LegalEntity.authorized_capital,
            LegalEntity.personnel_count,
            LegalEntity.founders_count,
            LegalEntity.status,
            LegalEntity.zipcode,
            LegalEntity.address,
            LegalEntity.legal_address,
            LegalEntity.email,
            LegalEntity.site,
            LegalEntity.phone,
            LegalEntity.fax,
            LegalEntity.gps_coordinates,
            LegalEntity.inn,
            LegalEntity.kpp,
            LegalEntity.okpo,
            LegalEntity.ogrn,
            LegalEntity.okfc,
            LegalEntity.okogu,
            LegalEntity.okato,
            LegalEntity.fsfr,
            LegalEntity.main_activity,
            LegalEntity.description
        ]
        if LegalEntity.insert_many(data_list, fields=fields).execute():
            ParsedPages.create(section=section, page_number=page, compaines_quantity=quantity)
            return True
        else:
            return False