#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import pathlib
import re
import codecs

list = []

def ipa_search(ipa_path,regex):
    fd = os.listdir(ipa_path)
    for file_name in fd:
        file_path = os.path.join(ipa_path,file_name)
        is_dir = os.path.isdir(file_path)
        if is_dir:
            dir_path = file_path
            ipa_search(dir_path,regex)
        else:
            with codecs.open(file_path,'rb',encoding='gbk',errors='ignore') as f:
                for line in f:
                   match = re.search(regex,line)
                   if(match):
                       list.append('文件名: ' + file_name + '\n' + '路径: ' + file_path + '\n' + '内容: ' + line)
                       print(file_path)
                       break


if __name__ == '__main__':
    print('ipa包需要解压缩后,获得payload文件夹才能查找,且关键字中只能包含中文,英文,或者数字')
    print('请输入payload文件的绝对路径:')
    ipa_path = input()
    print('请输入匹配关键字:')
    key = input()
    fp = ipa_search(ipa_path,key)

    out_path = os.path.join(ipa_path, key + '.txt')
    out = open(out_path, 'w')
    for content in list:
        out.write('\n'+content+'\n')
        out.write('--------------------------------------------------------------------------')
    out.close()
    print('****匹配文件所在路径**** '+out_path)
    print('\n\n\n')
    inp = 1
    while inp:
        inp = input()

#塒NG
#/Users/guanzhenfa/Documents/ipa/qn/Payload