# -*-*-*-*- coding: utf-8 -*-*-*-*-
# @Time    : 2020/1/2 上午10:44        
# @Author  : LpL                    
# @Email   : peilun2050@gmail.com    
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*
import site

site.addsitedir("../")
import os

root_path = "/Users/mac/PycharmProjects/new_fuckcode/OrderCenter/data"
file_list = os.listdir(root_path)


def clear_file():

    def del_file(path):
        ls = os.listdir(path)
        for i in ls:
            c_path = os.path.join(path, i)
            if os.path.isdir(c_path):
                del_file(c_path)
            else:
                os.remove(c_path)
    for path in file_list:
        if path != ".DS_Store":
            path = os.path.join(root_path, path)
            del_file(path)




if __name__ == '__main__':
    clear_file()
