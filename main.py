import sys
import os
import pandas as pd
from pathlib import Path
import xlsxwriter

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

    print("\n--=================== SEO PROJECT ===================--\n")
    print("-- EPITA MTI 2018 -- Subject 1")
    print("Contributors : Jouffret Romain (jouffr_a), Barat Valentin (barat_v)\n")
    print("\n--=================== Checking system :  ===================--\n\n")
    if os.system("which python") != 0:
        print('This program needs python 2.X to run. Please isntall it first.')
        return
    if os.system("which python3") != 0:
        print('This program needs python 3.X to run. Please isntall it first.')
        return
    if os.system("which pip") != 0:
        print('This program needs pip for packages control. Please isntall it first.')
        return
    if os.system("pip install scrapy") != 0:
        print('This program needs scrapy to run. Please isntall it first.')
        return
    if os.system("pip install xlsxwriter") != 0:
        print('This program needs xlsxwriter to run. Please isntall it first.')
        return
    if os.system("pip install pandas") != 0:
        print('This program needs pandas to run. Please isntall it first.')
        return
    print("\n--===================  Using :  ===================--\n\n")
    os.system("python --version")
    os.system("python3 --version")
    os.system("pip --version")
    os.system("pip3 --version")
    os.system("scrapy version")
    print("\nDescription:\n\n  This project scrap and collect information over craig's list for jobs posts.\n  It limits itself to the San Francisco area. Once all the results are collected\n  it will sets of shingles that will be used to calculate the distance of\n  jaccard in between the differents shingles and ultimately the whole\n  item. The results are displayed in the terminal but also available in CSV\n  or XLSX files.")
    print("\n\n --==== INFO ====--\n     If you desire to stop the crawling before it ends press once Ctrl+C to close it clean.")
    print("\n--=================== CRAWLING ======================--\n")
    os.system('scrapy runspider duplicated_content/spiders/jobs.py')

    print("\n--================ END OF CRWALING =================--\n")

    fil = Path('items.txt')
    f = open('items.txt', 'r')
    #print(''.join(f.readline()))
    texts = f.readlines()
    allt = list()
    for t in texts:
        allt.append(set(get_shingles(t, size=SHINGLE_SIZE)))
    print("Number of items scraped used : ", end='')
    print(len(allt))
    x = -1
    csvtab = list()
    for item in allt :
        x += 1
        j = 0
        #print(x, end='')
        #print(' :', end='')
        colmn = list()
        for comp in allt :
            perc = round(jaccard(item, comp) * 100, 2)
            #print(' | ', perc , end='')
            colmn.append(jaccard(item, comp) * 100)
        csvtab.append(colmn)
        #print('|')

    df = pd.DataFrame(csvtab)
    df.to_csv('test.csv', index=False, header=False)
    with pd.ExcelWriter ('test.xlsx') as writer:
                df.to_excel(writer, sheet_name = 'sheet1',engine='xlsxwriter')
    #print(jaccard(shingles1, shingles2))
    print("\n--=================== END ===================--\n")
    # ADD TIMER

# ===== EXECUTE =====
#
if __name__ == '__main__':
    main()
