#！/opt/anaconda3/bin/python
# -*- coding = utf-8 -*-
from bs4 import BeautifulSoup
import re
import urllib.request, urllib.error
import os
import threading
import queue

class myThread(threading.Thread):
    def __init__(self, ThreadID, name, baseurl, chapterindex_list, chaptername_list, chapterurl_list, page_num):
        threading.Thread.__init__(self)
        self.ThreadID = ThreadID
        self.name = name
        self.baseurl = baseurl
        self.chapterindex_list = chapterindex_list
        self.chaptername_list = chaptername_list
        self.chapterurl_list = chapterurl_list
        self.page_num = page_num
        self.article_list = []
    def run(self):
        self.article_list = getTxt_thread(self.baseurl, self.chapterindex_list, self.chaptername_list, self.chapterurl_list, self.page_num)
    def get_article_list(self):
        threading.Thread.join(self)
        try:
            return self.article_list
        except Exception:
            return None

def is_numeric(character):
    pattern = r'^[0-9]\d*$'
    match = re.match(pattern, character)
    return match is not None

#中文数字转阿拉伯数字
def number_c2e(chinese_number):
    map = {'〇':0, '零':0, '一':1, '二':2, '三':3, '四':4, '五':5, '六':6,'七':7, '八':8, '九':9, '十':10}
    bit_map = {'十':10, '百':100, '千':1000, '万':1000}
    size = len(chinese_number)
    if size == 0: return 0
    if size < 2:
        return map[chinese_number]
    
    ans = 0
    continue_flag = False
    for i in range(size):
        if continue_flag:
            continue_flag = False
            continue

        if i + 1 < size:
            if chinese_number[i+1] in bit_map.keys():
                ans += map[chinese_number[i]] * bit_map[chinese_number[i+1]]
                continue_flag = True
                continue
        
        ans += map[chinese_number[i]]
    return ans

#获取指定URL的网页内容,输入URL,输出网页内容
def askURL(url):
    head = {"User-Agent": "Chrome / 128.0.6613.85"} #浏览器头部信息
    request = urllib.request.Request(url, headers=head)
    html = ""

    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    
    return html

def getData(baseurl, savepath):
    page_num = 1
    page = ""
    print('Downloading ' + savepath) 
    
    while page_num <= 8:#总共12页
        article = []
        page = getPage(baseurl, page_num)
        page_html = askURL(page)
        soup = BeautifulSoup(page_html, "html.parser")
        chapterindex_list, chaptername_list, chapterurl_list = getChapter(soup.find_all('li', class_='col-md-3'))
        print('Downloading page ' + str(page_num) + '.')
        #article = getTxt(baseurl, chapterindex_list, chaptername_list, chapterurl_list, page_num)
        #使用5个线程，来加速这100个任务，任务平均分配
        job_index = [20, 40, 60, 80]
        thread1 = myThread(1, "Thread-1", baseurl, chapterindex_list[:job_index[0]], chaptername_list[:job_index[0]], chapterurl_list[:job_index[0]], page_num)
        thread2 = myThread(2, "Thread-2", baseurl, chapterindex_list[job_index[0]:job_index[1]], chaptername_list[job_index[0]:job_index[1]], chapterurl_list[job_index[0]:job_index[1]], page_num)
        thread3 = myThread(3, "Thread-3", baseurl, chapterindex_list[job_index[1]:job_index[2]], chaptername_list[job_index[1]:job_index[2]], chapterurl_list[job_index[1]:job_index[2]], page_num)
        thread4 = myThread(4, "Thread-4", baseurl, chapterindex_list[job_index[2]:job_index[3]], chaptername_list[job_index[2]:job_index[3]], chapterurl_list[job_index[2]:job_index[3]], page_num)
        thread5 = myThread(5, "Thread-5", baseurl, chapterindex_list[job_index[3]:], chaptername_list[job_index[3]:], chapterurl_list[job_index[3]:], page_num)
        #多线程，后汇总好像不需要重新排序？
        thread1.start()
        thread2.start()
        thread3.start()
        thread4.start()
        thread5.start()
        thread1.join()
        thread2.join()
        thread3.join()
        thread4.join()
        thread5.join()

        article = thread1.get_article_list() + thread2.get_article_list() + thread3.get_article_list() + thread4.get_article_list() + thread5.get_article_list()

        SaveData(article, savepath, page_num)
        
        page_num = page_num + 1

    return 0

def getPage(url, index):
    page_url = url + 'index_' + str(index) + '.html'
    return page_url
    #page = ""
    #html = askURL(url)
    #soup = BeautifulSoup(html, "html.parser")
    #links = soup.find('li', class_ = 'page-item active')
    #page = links.find('a')
    #return page

def getChapter(list_all):#分析拿到具体章节的url,并读取网页内容；如有分页,多次调用本程序
    chapter_url = []
    chapter_name = []
    chapter_index = []
    for chapter_item in list_all:
        tmp = chapter_item.find('a')
        tmp_1 = tmp['href'].split('/')
        chapter_url.append(tmp_1[-1])
        chapter_name.append(chapter_item.get_text())
        tmp = chapter_item.get_text()
        tmp_1 = tmp.split('章')
        tmp_2 = tmp_1[0].lstrip('第')
        if is_numeric(tmp_2):
            chapter_index.append(int(tmp_2))
        else:
            chapter_index.append(number_c2e(tmp_2))

    return chapter_index, chapter_name, chapter_url

def getTxt(baseurl, chapterindex_list, chaptername_list, chapterurl_list, page_num):#分析该章节,并提取文章
    page_chapter_index = page_num * 100
    article_list = []
    move = dict.fromkeys((ord(c) for c in u"\xa0\n\t\r"))
    #for i in range(17):
    for i in range(len(chapterindex_list)):
        article = ''
        if chapterindex_list[i] <= page_chapter_index:
            tmp_url = baseurl + chapterurl_list[i]
            html = BeautifulSoup(askURL(tmp_url), "html.parser")
            article_1 = html.find('article').getText().translate(move)
            article = article + article_1.lstrip('第(1/3)页').rstrip('第(1/3)页')

            tmp_url = tmp_url.rstrip('.html') + '_2.html'
            html = BeautifulSoup(askURL(tmp_url), "html.parser")
            article_2 = html.find('article').getText().translate(move)
            article = article + article_2.lstrip('第(2/3)页').rstrip('第(2/3)页')

            tmp_url = tmp_url.split('_')[0] + '_3.html'
            html = BeautifulSoup(askURL(tmp_url), "html.parser")
            article_3 = html.find('article').getText().translate(move)
            article = article + article_3.lstrip('第(3/3)页').rstrip('第(3/3)页')

            #print(chaptername_list[i])
            article = chaptername_list[i] + '\n' + re.sub(r'([a-zA-Z0-9]+\.)+[a-z]+', "", article)
            article_list.append(article)
    return article_list

def getTxt_thread(baseurl, chapterindex_list, chaptername_list, chapterurl_list, page_num):#分析该章节,并提取文章
    page_chapter_index = page_num * 100
    article_list = []
    move = dict.fromkeys((ord(c) for c in u"\xa0\n\t\r"))
    #for i in range(17):
    for i in range(len(chapterindex_list)):
        article = ''
        if chapterindex_list[i] <= page_chapter_index:
            tmp_url = baseurl + chapterurl_list[i]
            html = BeautifulSoup(askURL(tmp_url), "html.parser")
            article_1 = html.find('article').getText().translate(move)
            article = article + article_1.lstrip('第(1/3)页').rstrip('第(1/3)页')

            tmp_url = tmp_url.rstrip('.html') + '_2.html'
            html = BeautifulSoup(askURL(tmp_url), "html.parser")
            article_2 = html.find('article').getText().translate(move)
            article = article + article_2.lstrip('第(2/3)页').rstrip('第(2/3)页')

            tmp_url = tmp_url.split('_')[0] + '_3.html'
            html = BeautifulSoup(askURL(tmp_url), "html.parser")
            article_3 = html.find('article').getText().translate(move)
            article = article + article_3.lstrip('第(3/3)页').rstrip('第(3/3)页')

            #print(chaptername_list[i])
            article = chaptername_list[i] + '\n' + re.sub(r'([a-zA-Z0-9]+\.)+[a-z]+', "", article)
            article_list.append(article)
    return article_list

def SaveData(DataList, savepath, page_num):
    print('saving page ' + str(page_num))
    if page_num == 1:
        if os.path.isfile(savepath):
            os.remove(savepath) #删除上次保存的文件
        fo = open(savepath, 'w')
        for item in DataList:
            fo.write(item)
            fo.write('\n\n')
        fo.close()
    else:
        fo = open(savepath, '+a')
        for item in DataList:
            fo.write(item)
            fo.write('\n\n')
        fo.close()
    
    return 0

def main():

    baseurl = "https://www.txtd.net/108/108136/"

    savepath = "逍遥四公子宁宸.txt"
    
    getData(baseurl, savepath)

    #print(len(DataList))




if __name__ == "__main__":
    main()
    print("完成！")