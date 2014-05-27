# -*- coding: utf-8 -*-
'''
fetch 163 blogs
'''
from bs4 import BeautifulSoup, element
import datetime, urllib, re, os

def get_blog(url):
    filename = 'data/' + url[url.find('static/') + 7 : -1] + '.html'
    if os.path.exists(filename):
        return
    print url
    # get the html page
    soup = BeautifulSoup(urllib.urlopen(url).read())
    # the main content
    block = soup.find('div', class_='nbw-bitm bdwb bds2 bdc0 ')
    if block is None:
        return
    fw = open(filename, 'w')
    fw.write(block.prettify().encode('utf-8'))
    fw.close()
    # the meta info, stored in a javascript section
    block = soup.find('textarea', attrs={'name':'js'})
    if block is None:
        return
    fw = open(filename, 'a')
    fw.write(block.prettify().encode('utf-8'))
    fw.close()


def get_everyblog():
    f = open('articles.txt')
    for line in f:
        if len(line.strip()) == 0 or line[0] == '#':
            continue
        get_blog(line.strip())
    f.close()

def extract_metas():
    fw = open('meta.txt', 'w')
    base = './data/'
    for filename in os.listdir(base):
        f = open(base + filename)
        soup = BeautifulSoup(f)
        title = soup.find('h3', class_='title pre fs1').get_text().strip()
        metas = soup.find('p', class_='tdep clearfix nbw-act fc06').get_text()
        metas = re.sub('\s+', ' ', metas)
        posttime = re.search('[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}', metas).group(0).strip()
        category = re.search(u'\|\s+分类：([^\|]+)', metas, re.U).group(1).strip()
        tags = re.search(u'blogTag:\'([^\']+)\'', str(soup), re.U)
        if tags is None:
            tags = ''
        else:
            tags = tags.group(1).strip().decode('utf-8')
        metainfo = '\t'.join([re.search('[0-9]+', filename).group(0), title, posttime, category, tags])
        fw.write(metainfo.encode('utf-8') + '\n')
        f.close()
    fw.close()

def extract_contents():
    base = './data/'
    for filename in os.listdir(base):
        f = open(base + filename)
        soup = BeautifulSoup(f)
        maincontent = soup.find('div', class_='bct fc05 fc11 nbw-blog ztag')
        fw = open('./txt/' + re.search('[0-9]+', filename).group(0) + '.txt', 'w')
        for item in maincontent.find_all(['font', 'img', 'p'], recursive=False):
            if item.name != 'img':
                output = item.get_text().strip()
                if item.find('img') is not None:
                    output += '\n' + item.find('img').get('src')
            else:
                output = item.get('src')
            if len(output) > 0:
                fw.write(output.encode('utf-8') + '\n')
        fw.close()
        f.close()

def download_images():
    base = './txt/'
    for filename in os.listdir(base):
        filenum = re.search('[0-9]+', filename).group(0)
        imgbase = './img/' + filenum + '/'
        if not os.path.exists(imgbase):
            os.makedirs(imgbase)
        f = open(base + filename)
        for line in f:
            if line.find('http://') < 0:
                continue
            imgmatch = re.search('[0-9]+.(jpg|gif)$', line.strip())
            if imgmatch is None:
                print line.strip()
                continue
            imgname = imgmatch.group(0)
            if os.path.exists(imgbase + imgname):
                continue
            fw = open(imgbase + imgname, 'wb')
            fw.write(urllib.urlopen(line.strip()).read())
            fw.close()
        f.close()

get_everyblog()
extract_metas()
extract_contents()
download_images()

