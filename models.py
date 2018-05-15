# -*- coding: utf-8 -*-
import math
from peewee import *
from settings import database


class CompanySection(Model):
    name = CharField()
    code = CharField()
    url = CharField()

    class Meta:
        database = database


class CompanySubSection(Model):
    section = ForeignKeyField(model=CompanySection, field=CompanySection.code)

    name = CharField()
    code = CharField()
    url = CharField()
    companies_count = IntegerField()

    @classmethod
    def get_unparsed_sections(cls):
        """
        select
            css.code,
            css.name,
            css.url,
            CASE WHEN max(pp.page_number) is null THEN 0 else max(pp.page_number) END as max_parsed_page
        from companysubsection as css
        left outer join parsedpages as pp on css.code = pp.section_id
        group by css.code
        having max(pp.page_number) < css.companies_count or max(pp.page_number) is NULL
        """
        max_parsed_page = Case(None, ((fn.MAX(ParsedPages.page_number) >> None, 0),), fn.MAX(ParsedPages.page_number))
        query = cls\
            .select(cls.code, cls.name, cls.url, cls.companies_count, max_parsed_page.alias('max_parsed_page'))\
            .join(ParsedPages, JOIN.LEFT_OUTER)\
            .group_by(cls.code, cls.name)\
            .having((fn.MAX(ParsedPages.page_number) < cls.companies_count) | (fn.MAX(ParsedPages.page_number) >> None))
        return query

    def get_max_page(self):
        max = math.ceil(self.companies_count / 30)
        return math.ceil(self.companies_count / 30)

    class Meta:
        database = database


class ParsedPages(Model):
    section = ForeignKeyField(model=CompanySubSection, field=CompanySubSection.code)
    page_number = IntegerField()
    compaines_quantity = IntegerField()

    class Meta:
        database = database


class LegalEntity(Model):
    pk = BigIntegerField(primary_key=True)
    sub_section = ForeignKeyField(model=CompanySubSection, field=CompanySubSection.code)

    short_name = CharField()
    full_name = CharField()
    company_type = CharField(null=True)
    registration_date = DateField()

    director = FloatField(null=True)
    authorized_capital = FloatField(null=True)
    personnel_count = IntegerField(null=True)
    founders_count = IntegerField(null=True)
    status = CharField(default='Действующее')
    gps_coordinates = CharField(null=True)

    zipcode = CharField(null=True)
    address = CharField(null=True)
    legal_address = CharField(null=True)
    email = CharField(null=True)
    site = CharField(null=True)
    phone = CharField(null=True)
    fax = CharField(null=True)

    inn = CharField(null=True)
    kpp = CharField(null=True)
    okpo = CharField(null=True)
    ogrn = CharField(null=True)
    okfc = CharField(null=True)
    okogu = CharField(null=True)
    okopf = CharField(null=True)
    okato = CharField(null=True)
    fsfr = CharField(null=True)
    main_activity = CharField(null=True)
    description = CharField()

    class Meta:
        database = database


class WordTable(Model):
    word = CharField()
    count = IntegerField()

    class Meta:
        database = database


class CollocationTable(Model):
    collocation = CharField()
    count = IntegerField()

    class Meta:
        database = database
