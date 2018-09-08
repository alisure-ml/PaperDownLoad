# coding:utf-8
import re
import os
import requests
import multiprocessing
import urllib.request as request


def _main(i, all_num, url, filename):
    print("[{}/{}] Downloading {} -> {}".format(i, all_num, url, filename))
    request.urlretrieve(url, filename)
    pass

if __name__ == '__main__':

    # ICCV 2017, CVPR 2018, CVPR 2017, CVPR 2016
    year = 2017  # 2018, 2017, 2016
    conference = "ICCV"  # ICCV, CVPR
    address = "http://openaccess.thecvf.com/"
    data_url = "{}{}{}.py".format(address, conference, year)
    localDir = 'C:\\Users\\ALISURE\\Desktop\\{}-{}\\'.format(conference, year)
    if not os.path.exists(localDir):
        os.makedirs(localDir)

    # get web context
    data = requests.get(data_url).text
    link_list = re.findall(r"(?<=href=\").+?pdf(?=\">pdf)|(?<=href=\').+?pdf(?=\">pdf)", data)
    name_list = re.findall(r"(?<=href=\").+?{}_paper.html\">.+?</a>".format(year), data)

    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count() - 1)

    for index, _name in enumerate(name_list):
        _name = _name.split('<')[0].split('>')[1].replace(':', '_').replace('\"', '_').replace('?', '_').replace('/', '_')
        pool.apply_async(func=_main, args=(index, len(name_list), address + link_list[index], localDir + _name + '.pdf'))
        pass

    pool.close()
    pool.join()

    print("all download finished")
