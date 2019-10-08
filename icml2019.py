# coding:utf-8
import re
import os
import requests
import multiprocessing
import urllib.request as request


def _main(i, all_num, link_info, path):
    if len(link_info) == 1:
        print("[{}/{}] Error {}".format(i, all_num, link_info[0]))
        return

    _name = os.path.join(path, "{}-{}.pdf".format(i, link_info[0]).replace(":", " -"))
    if not os.path.exists(_name):
        try:
            print("[{}/{}] Downloading {}".format(i, all_num,  link_info[1]))
            request.urlretrieve(link_info[1], _name)
            print("[{}/{}] OK {} -> {}".format(i, all_num,  link_info[1], _name))
        except Exception:
            print("-----------------------------------------------------------------")
            print("[{}/{}] Error {} -> {}".format(i, all_num,  link_info[1], _name))
            print("-----------------------------------------------------------------")
            os.remove(_name)
            pass
        pass
    else:
        print("[{}/{}] OK Exist {} -> {}".format(i, all_num,  link_info[1], _name))
        pass

    if len(link_info) == 3:
        _name = os.path.join(path, "{}-{}-supp.pdf".format(i, link_info[0]).replace(":", " -"))
        if not os.path.exists(_name):
            try:
                print("[{}/{}] Downloading {}".format(i, all_num,  link_info[2]))
                request.urlretrieve(link_info[2], _name)
                print("[{}/{}] OK {} -> {}".format(i, all_num,  link_info[2], _name))
            except Exception:
                print("-----------------------------------------------------------------")
                print("[{}/{}] Error {} -> {}".format(i, all_num,  link_info[2], _name))
                print("-----------------------------------------------------------------")
                os.remove(_name)
                pass
            pass
        else:
            print("[{}/{}] OK Exist {} -> {}".format(i, all_num,  link_info[1], _name))
            pass
        pass

    pass

if __name__ == '__main__':

    Config = {
        "SummaryURL": "http://proceedings.mlr.press/v97/",
        "FindPattern": r"(?<=href=\")http://proceedings.mlr.press/v97/.+?\.pdf(?=\")|(?<=\"title\">).+?(?=</p>)",
        "localDir": "D:\\paper\\{}-{}".format("ICML", 2019)
    }
    if not os.path.exists(Config["localDir"]):
        os.makedirs(Config["localDir"])

    # get web context
    print("begin to request get data")
    data = requests.get(Config["SummaryURL"]).text
    print("begin to find {}".format(Config["FindPattern"]))
    _link_list = re.findall(Config["FindPattern"], data)

    print("begin to deal link list")
    link_list = []
    for link_one in _link_list:
        if not link_one.startswith("http"):
            link_list.append([link_one])
        else:
            link_list[-1].append(link_one)
            pass
        pass

    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count() - 1)

    print("begin to download")
    for index, _link_info in enumerate(link_list):
        pool.apply_async(func=_main, args=(index, len(link_list), _link_info, Config["localDir"]))
        pass

    pool.close()
    pool.join()

    print("all download finished")
    pass
