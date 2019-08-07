#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import pathlib
import re
import codecs
import _thread
import queue
import time

key_list = []
dict = {}
output_file_name = 'outputs'
is_need_encode = False

def ipa_search(ipa_path,key_list):
    fd = os.listdir(ipa_path)
    for file_name in fd:
        if file_name == output_file_name:
            continue
        file_path = os.path.join(ipa_path,file_name)
        is_dir = os.path.isdir(file_path)
        if is_dir:
            dir_path = file_path
            ipa_search(dir_path,key_list)
        else:
            with codecs.open(file_path,'rb',encoding='gbk',errors='ignore') as f:
                search_file(f,key_list,file_name,file_path)
            # f = codecs.open(file_path,'rb',encoding='gbk',errors='ignore')
            # mutil_thread_search(f,key_list,file_name,file_path)

def search_file(f,key_list,file_name,file_path):
    for line in f:
        for regex in key_list:
            match = re.search(regex, line)
            if (match):
                queue = dict[regex]
                queue.put('文件名: ' + file_name + '\n' + '路径: ' + file_path + '\n' + '内容: ' + line)
                print(file_path)

def mutil_thread_search(f,key_list,file_name,file_path):
    for regex in key_list:
        _thread.start_new_thread(func_thread_search,(f,regex,file_name,file_path))

def func_thread_search(f,regex,file_name,file_path):
    for line in f:
        match = re.search(regex,line)
        if(match):
            queue = dict[regex]
            queue.put('文件名: ' + file_name + '\n' + '路径: ' + file_path + '\n' + '内容: ' + line)
            print(file_path)
    # f.close()

def prepare(key_list):
    for key in key_list:
        dict[key] = queue.LifoQueue()

def archeive():
    for key in dict.keys():
        q = dict[key]
        out_path = os.path.join(ipa_path, 'outputs')

        if not os.path.isdir(out_path):
            os.makedirs(out_path)

        out_path = os.path.join(out_path, key + '.txt')
        out = open(out_path, 'w')
        while not q.empty():
            content = q.get()
            if(is_need_encode):
                content = content.encode('gbk', 'ignore').decode('utf-8', 'ignore')
            out.write('\n' + content + '\n')
            out.write('--------------------------------------------------------------------------')
        out.close()
        print('****匹配文件所在路径**** ' + out_path)
        print('\n\n\n')

if __name__ == '__main__':
    start_time = time.time()
    print('ipa包需要解压缩后,获得payload文件夹才能查找,且关键字中只能包含中文,英文,或者数字')
    ipa_path = ''
    key = ''
    is_encode = ''

    while len(ipa_path) == 0:
        print('请输入payload文件的绝对路径:')
        ipa_path = input()

    while len(key) == 0:
        print('请输入匹配关键字(多个关键字可用逗号分割):')
        key = input()

    while len(is_encode) == 0:
        print('是否要输出为utf-8编码格式(默认GBK): y/n?:')
        is_encode = input()

    if(is_encode.upper() == 'Y'):
        is_need_encode = True
    key_list = key.split(',')

    prepare(key_list)
    fp = ipa_search(ipa_path,key_list)
    archeive()
    end_time = time.time()
    print('time cost: ',end_time - start_time,'s')

    inp = 1
    while inp:
        inp = input()

#塒,渖,屣,駴,坟,硽
#/Users/guanzhenfa/Documents/ipa/qn/Payload