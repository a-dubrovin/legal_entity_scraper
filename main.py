# -*- coding: utf-8 -*-
import argparse
#from parse import DataCollector
#from calculate import Calculator
import scrapy
from scrapy.cmdline import execute

if __name__ == "__main__":
    #execute(['scrapy', 'runspider', 'companycollector/spiders/sections_spider.py'])
    execute(['scrapy', 'runspider', 'companycollector/spiders/legal_entities_spider.py'])
    """
    parser = argparse.ArgumentParser(description='Params list')
    parser.add_argument('--del_companies', action='store_true', help='Clear CompanyTable')
    parser.add_argument('--collect_companies', action='store_true', help='Collect companies')
    parser.add_argument('--calculate_words', action='store_true', help='Calculate top words')
    parser.add_argument('--calculate_collocations', action='store_true', help='Calculate top collocations')
    parser.add_argument('--top_words', action='store_true', help='Show top words')
    parser.add_argument('--top_collocations', action='store_true', help='Show top collocations')
    parser.add_argument('--save_top_words', action='store_true', help='Save top words to file "top_words.csv"')
    parser.add_argument('--save_top_collocations', action='store_true', help='Save top collocations to file '
                                                                             '"top_collocations.csv"')

    args = parser.parse_args()

    if args.collect_company:
        print('Collecting companies.')
        if args.del_company:
            print('Clearing company table.')
        DataCollector.collect(clear_companies=args.del_company)
    if args.calculate_words or args.calculate_collocations:
        if args.calculate_words:
            print('Calculating words.')
        if args.calculate_collocations:
            print('Calculating collocations.')
        Calculator.calculate(words=args.calculate_words, collocations=args.calculate_collocations)

    if args.top_words:
        Calculator.show_top_words()
    if args.top_collocations:
        Calculator.show_top_collocations()
    if args.save_top_words:
        Calculator.top_words_to_csv()
    if args.save_top_collocations:
        Calculator.top_collocations_to_csv()
    """