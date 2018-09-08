# http://papers.nips.cc/book/advances-in-neural-information-processing-systems-30-2017

# coding:utf-8
import re
import os
import requests
import multiprocessing
import urllib.request as request


def _main(i, all_num, url, path):
    print("[{}/{}] Downloading {} -> {}".format(i, all_num, url, path))
    request.urlretrieve(url, path)
    pass

if __name__ == '__main__':

    Config = {
        "WebURL": "http://papers.nips.cc",
        "SummaryURL": "http://papers.nips.cc/book/advances-in-neural-information-processing-systems-30-2017",
        "FindPattern": r"(?<=\<li\>).+?paper.+?(?=\</li\>)",
        "localDir": "C:\\Users\\ALISURE\\Desktop\\Paper\\{}-{}".format("NIPS", 2017)
    }

    if not os.path.exists(Config["localDir"]):
        os.makedirs(Config["localDir"])

    # get web context
    data = requests.get(Config["SummaryURL"]).text
    link_list = re.findall(Config["FindPattern"], data)

    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count() - 1)

    for index, _link in enumerate(link_list):
        _datas = _link.split("href=\"")[1].split("</a>")[0].split("\">")
        _url_pdf = Config["WebURL"] + _datas[0] + ".pdf" if Config["WebURL"] not in _datas[0] else _datas[0] + ".pdf"
        _name = _datas[1].replace(':', '_').replace('\"', '_').replace('?', '_').replace('/', '_')
        _name = os.path.join(Config["localDir"], _name) + ".pdf"
        pool.apply_async(func=_main, args=(index, len(link_list), _url_pdf, _name))
        pass

    pool.close()
    pool.join()

    print("all download finished")
