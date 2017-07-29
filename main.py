import sys
import os
import argparse
from datetime import datetime

import pandas as pd
from pathlib import Path

import plotly.plotly as py
import plotly
import plotly.graph_objs as go

import xlsxwriter
import numpy as np
from IPython.display import display, HTML
from xhtml2pdf import pisa

plotly.tools.set_credentials_file(username='Nahast', api_key='lBowybnVZZf4S6W5I2KN')

# ===== SHINGLES ======
#
SHINGLE_SIZE_DEFAULT = 5

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

# ===== REPORT BUILDING ======
#
def report_block_template(report_type, graph_url, caption=''):
    if report_type == 'interactive':
        graph_block = '<iframe style="border: none;" src="{graph_url}.embed" width="100%" height="600px"></iframe>'
    elif report_type == 'static':
        graph_block = (''
            '<a href="{graph_url}" target="_blank">' # Open the interactive graph when you click on the image
                '<img style="height: 400px;" src="{graph_url}.png">'
            '</a>')

    report_block = ('' +
        graph_block +
        '{caption}' + # Optional caption to include below the graph
        '<br>'      + # Line break
        '<a href="{graph_url}" style="color: rgb(190,190,190); text-decoration: none; font-weight: 200;" target="_blank">'+
            'Click to comment and see the interactive graph' + # Direct readers to Plotly for commenting, interactive graph
        '</a>' +
        '<br>' +
        '<hr>') # horizontal line

    return report_block.format(graph_url=graph_url, caption=caption)

# ===== CONVERT HTML TO PDF ======
#
def convert_html_to_pdf(source_html, output_filename):
    # open output file for writing (truncated binary)
    result_file = open(output_filename, "w+b")

    # convert HTML to PDF
    pisa_status = pisa.CreatePDF(
            source_html,                # the HTML to convert
            dest=result_file)           # file handle to recieve result

    # close output file
    result_file.close()                 # close output file

    # return True on success and False on errors
    return pisa_status.err

# ===== MAIN ======
#
def main():
    startTime = datetime.now()
    parser = argparse.ArgumentParser()
    parser.add_argument("root", help="Website you want to scrap")
    parser.add_argument("shingles", help="Integer that will determine shingles size")
    args = parser.parse_args()
    print("\n--=================== SEO PROJECT ===================--\n")
    print("-- EPITA MTI 2018 -- Subject 1")
    print("Contributors : Jouffret Romain (jouffr_a), Barat Valentin (barat_v)\n")
    print("\n--=================== Setup :  ===================--\n\n")
    fil = Path('items.txt')
    if fil.is_file():
        os.system('rm items.txt')
    fil = Path('text.txt')
    if fil.is_file():
        os.system('rm items.txt')
    fil = Path('items.txt')
    if fil.is_file():
        os.system('rm items.txt')
    fil = Path('items.txt')
    if fil.is_file():
        os.system('rm items.txt')
    if os.system("which python") != 0:
        print('This program needs python 2.X to run. Please isntall it first.')
        return
    if os.system("which python3") != 0:
        print('This program needs python 3.X to run. Please isntall it first.')
        return
    if os.system("which pip3") != 0:
        print('This program needs pip3 for packages control. Please isntall it first.')
        return
    if os.system("pip3 install scrapy") != 0:
        print('This program needs scrapy to run. Please isntall it first.')
        return
    if os.system("pip3 install xlsxwriter") != 0:
        print('This program needs xlsxwriter to run. Please isntall it first.')
        return
    if os.system("pip3 install pandas") != 0:
        print('This program needs pandas to run. Please isntall it first.')
        return
    if os.system("pip3 install plotly --upgrade") != 0:
        print('This program needs pandas to run. Please isntall it first.')
        return
    if os.system("pip3 install --pre xhtml2pdf") != 0:
        print('This program needs pandas to run. Please isntall it (with --pre for python3 compat.) first.')
        return
    if os.system("pip3 install ipython") != 0:
        print('This program needs pandas to run. Please isntall it first.')
        return
    print("\n--===================  Using :  ===================--\n\n")
    os.system("python --version")
    os.system("python3 --version")
    os.system("pip --version")
    os.system("pip3 --version")
    os.system("scrapy version")
    print("plotly 2.0.12")
    os.system("echo ipython & ipython --version")
    print("\nDescription:\n\n  This project scrap and collect information over craig's list for jobs posts.\n  It limits itself to the San Francisco area. Once all the results are collected\n  it will sets of shingles that will be used to calculate the distance of\n  jaccard in between the differents shingles and ultimately the whole\n  item. The results are displayed in the terminal but also available in CSV\n  or XLSX files.")
    print("\n--=================== INFO ======================--\n")
    print("If you desire to stop the crawling before it ends press once Ctrl+C to close it clean.\n")
    print("\n--=================== CRAWLING ======================--\n")
    print('Site to explore: ', args.root)
    os.system('scrapy runspider duplicated_content/spiders/jobs.py -a site=' + args.root)

    print("\n--================ END OF CRWALING =================--\n")

    fil = Path('items.txt')
    f = open('items.txt', 'r')
    texts = f.readlines()
    allt = list()
    for t in texts:
        allt.append(set(get_shingles(t, size=int(args.shingles))))
    print("Number of items scraped used : ", end='')
    print('Size of the shingles created: '.join(args.shingles))
    print(len(allt))
    x = -1
    y = -1
    csvtab = list()
    y_ax = list()
    x_ax = list()
    print('* Processing of the results')
    for item in allt :
        x += 1
        colmn = list()
        for comp in allt :
            perc = jaccard(item, comp) * 100
            colmn.append(perc)
            if perc != 100 :
                if  y < 1000 :
                    y_ax.append(perc)
                    y += 1
                if x < 200 :
                    x_ax.append(perc)
        csvtab.append(colmn)
    print('* Finished calculating')

    # WRINTING REPORT CSV
    df = pd.DataFrame(csvtab)
    df.to_csv('seo_result.csv', index=False, header=False)
    with pd.ExcelWriter ('seo_result.xlsx') as writer:
                df.to_excel(writer, sheet_name = 'sheet1',engine='xlsxwriter')

    print('* Finished creating csv file')

    # STARTING REPORT
    trace1 = go.Scatter(
        y = np.asarray(y_ax),
        mode = 'markers'
    )

    trace2 = go.Scattergl(
        y = np.asarray(x_ax),
        mode = 'markers',
        marker=dict(
            size='16',
            color = np.asarray(x_ax), #set color equal to a variable
            colorscale='Viridis',
            showscale=True
        )
    )

    data = [trace1]
    data2 = [trace2]

    plot1 = py.plot(data2, filename='scatter-plot-data-seo-gl', auto_open=False)
    plot2 = py.plot(data, filename='scatter-plot-data-seo', auto_open=False)

    graphs = [ plot1, plot2 ]

    interactive_report = ''
    static_report = ''

    for graph_url in graphs:
        _static_block = report_block_template('static', graph_url, caption='')
        _interactive_block = report_block_template('interactive', graph_url, caption='')
        static_report += _static_block
        interactive_report += _interactive_block

    #display(HTML(interactive_report))
    #display(HTML(static_report))

    print('* Finished creating report\n\n')

    convert_html_to_pdf(static_report, 'seo_report.pdf')

    os.system('open seo_report.pdf')
    os.system('open seo_result.csv')

    print('Time of execution: ', (datetime.now() - startTime))

    print("\n--=================== END ===================--\n")

# ===== EXECUTE =====
#
if __name__ == '__main__':
    main()
