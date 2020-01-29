# -*-*-*-*- coding: utf-8 -*-*-*-*-
# @Time    : 2018/11/29 下午10:25        
# @Author  : LpL                    
# @Email   : peilun2050@gmail.com    
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
import hashlib
import site
import zipfile

import os
site.addsitedir("../")  # For absolute import


def get_md5(file=None, data=None):
    """返回文件MD5
    data:{'body':'xasdad'}
    """
    md5_list = []
    if file:
        with open(file, "rb") as f:
            body = f.read()
            data = [{'body': body}]

    assert data and data != None and data != []

    for i in data:
        md5_list.append(hashlib.md5(i['body']).hexdigest())
    return md5_list


def zipfiles(dirpath, name_list, outFullName):
    """
    压缩指定文件夹
    """
    zip = zipfile.ZipFile(outFullName,"w",zipfile.ZIP_DEFLATED)
    for path,dirnames,filenames in os.walk(dirpath):
        fpath = path.replace(dirpath,'')
        for filename in filenames:
            if filename in name_list:
                zip.write(os.path.join(path,filename),os.path.join(fpath,filename))
    zip.close()


if __name__ == '__main__':
    # md5 = get_md5('/Users/mac/Downloads/0001876-w-b-1.png')
    # print(md5)
    print(1)
    zipfiles("../data/channel_output", ["小哈皮原单.xlsx", "有赞原单.xlsx"],"../data/vendor_zip/dog.zip")
