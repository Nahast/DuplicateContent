# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pathlib import Path

class DuplicatedContentPipeline(object):
    def process_item(self, item, spider):
        fil = Path('items.txt')
        if fil.is_file():
            f = open('items.txt', 'a+')
        else:
            f = open('items.txt', 'w+')
        f.write(''.join(str(it) for it in item.items()) + '\n')
        f.close()
        return item
