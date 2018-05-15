# -*- coding: utf-8 -*-
from settings import database
from models import CompanySection, CompanySubSection, LegalEntity, WordTable, CollocationTable, ParsedPages


database.connect()
database.create_tables([CompanySection, CompanySubSection, LegalEntity, WordTable, CollocationTable, ParsedPages])

