import sys
import pandas as pd
from pathlib import Path
import xlsxwriter
import scrapy
from duplicated_content.duplicated_content.spiders import jobs 

# ===== SHINGLING ======
#
SHINGLE_SIZE = 5

def get_shingles(f, size):
    shingles = set()
    buf = f # read entire file
    for i in range(0, len(buf)-size+1):
        yield buf[i:i+size]

# ===== JACCARD ======
#
def jaccard(set1, set2):
    x = len(set1.intersection(set2))
    y = len(set1.union(set2))
    return x / float(y)

# ===== MAIN ======
#
def main():
    process = CrawlerProcess()
    process.crawl(jobs.JobsSpider())
    process.start()

    fil = Path('items.txt')
    f = open('items.txt', 'r')
    #print(''.join(f.readline()))
    texts = f.readlines()
    allt = list()
    for t in texts:
        allt.append(set(get_shingles(t, size=SHINGLE_SIZE)))
    print(len(texts))
    print(len(allt))
    x = -1
    csvtab = list()
    for item in allt :
        x += 1
        j = 0
        print(x, end='')
        print('  : \t', end='')
        colmn = list()
        for comp in allt :
            perc = round(jaccard(item, comp) * 100, 2)
            print('  | ', perc , end='')
            colmn.append(jaccard(item, comp) * 100)
        csvtab.append(colmn)
        print('\t|')

    df = pd.DataFrame(csvtab)
    df.to_csv('test.csv', index=False, header=False)
    with pd.ExcelWriter ('test.xlsx') as writer:
                df.to_excel(writer, sheet_name = 'sheet1',engine='xlsxwriter')
    #print(jaccard(shingles1, shingles2))
    print("\n*+*+*+*+*+* END *+*+*+*+*+*\n")
    # ADD TIMER

# ===== EXECUTE =====
#
if __name__ == '__main__':
    main()
