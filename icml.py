# coding:utf-8
import re
import os
import requests
import multiprocessing
import urllib.request as request


def _main(i, all_num, url, path):
    _url_data = requests.get(url).text
    _url_paf = os.path.splitext(url)[0] + "/" + os.path.basename(url).replace("html", "pdf")
    _name = _url_data.split("<h1>")[1].split("</h1>")[0]
    _name = _name.replace(':', '_').replace('\"', '_').replace('?', '_').replace('/', '_')
    _name = os.path.join(path, _name) + ".pdf"
    print("[{}/{}] Downloading {} -> {}".format(i, all_num, _url_paf, _name))
    request.urlretrieve(_url_paf, os.path.join(path, _name))
    pass

if __name__ == '__main__':

    # Config = {
    #     "SummaryURL": "https://icml.cc/Conferences/2017/Schedule/?type=Poster",
    #     "FindPattern": r"(?<=href=\")http://proceedings.mlr.press/v70/.+?\.html(?=\")",
    #     "localDir": "C:\\Users\\ALISURE\\Desktop\\Paper\\{}-{}".format("ICML", 2017)
    # }
    Config = {
        "SummaryURL": "https://icml.cc/Conferences/2018/Schedule/?type=Poster",
        "FindPattern": r"(?<=href=\")http://proceedings.mlr.press/v80/.+?\.html(?=\")",
        "localDir": "C:\\Users\\ALISURE\\Desktop\\Paper\\{}-{}".format("ICML", 2018)
    }

    if not os.path.exists(Config["localDir"]):
        os.makedirs(Config["localDir"])

    # get web context
    data = requests.get(Config["SummaryURL"]).text
    link_list = re.findall(Config["FindPattern"], data)

    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count() - 1)

    for index, _link in enumerate(link_list):
        pool.apply_async(func=_main, args=(index, len(link_list), _link, Config["localDir"]))
        pass

    pool.close()
    pool.join()

    print("all download finished")
