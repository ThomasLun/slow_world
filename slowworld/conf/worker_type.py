# -*-*-*-*- coding: utf-8 -*-*-*-*-
# @Time    : 2019/12/26 上午10:06        
# @Author  : LpL                    
# @Email   : peilun2050@gmail.com    
# -*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*

# def fast_task(*args): return {x:args[TAST_MAP.get(args[0]).index(x)] for x in TAST_MAP.get(args[0])}


#  任务名
# 上传文件
ZIP_FILES = "zip_files"
GET_TITLES = "get_titles"


# 上传厂商表

def fast_task(*args):
    assert len(args)
    task_word = TAST_MAP.get(args[0])
    assert len(args) == len(task_word)
    data = {x: args[task_word.index(x)] for x in task_word}
    return data


TAST_MAP = {
    GET_TITLES: ["type", "file", "outpath", "channel_id"],
    ZIP_FILES: ["type", "inpath","file_list","outpath"],
}

if __name__ == '__main__':
    pass
