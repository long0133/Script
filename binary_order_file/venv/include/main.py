#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import re
from random import shuffle

__TEXT_info_regex = '__TEXT\s__(.*)'

##########################
oc_sym_regex = r'(\+|-)\[.*\]'
block_sym_regex = r'___(.*)'
literal_str_regex = r'literal string:'
head = r'0x(.*)/]?'

def parse_symbol(root_path, link_file_name):
    file_path = os.path.join(root_path,link_file_name)
    oc_symbol_file_path = os.path.join(root_path,'oc_symbol.txt')
    block_symbol_file_path = os.path.join(root_path,'block_symbol.txt')
    cstring_file_path = os.path.join(root_path,'cstring.txt')
    with open(file_path, 'r+', encoding='utf-8', errors='ignore') as f:
        oc_sym_file = open(oc_symbol_file_path,'w+')
        block_sym_file = open(block_symbol_file_path,'w+')
        cstring_file = open(cstring_file_path,'w+')
        for line in f:
            if not re.search('<<dead>>',line):
                if re.search(oc_sym_regex,line):
                    l = re.search(oc_sym_regex,line)
                    oc_sym_file.write(l.group(0) + '\n')
                elif re.search(block_sym_regex,line):
                    l = re.search(block_sym_regex,line)
                    block_sym_file.write(l.group(0) + '\n')
                elif re.search(literal_str_regex,line):
                    subs = line.split(' ')
                    l = subs[-1]
                    cstring_file.write(l)
        oc_sym_file.close()
        block_sym_file.close()
        cstring_file.close()
    shuffle_symbol(root_path,oc_symbol_file_path,block_symbol_file_path,cstring_file_path)

def shuffle_symbol(root_path,oc_path,block_path,str_path):
    oc_symbol_file_path = oc_path
    block_symbol_file_path = block_path
    cstring_file_path = str_path
    order_file_path = os.path.join(root_path, order_filename)
    with open(order_file_path,'w+') as f:
        oc_sym_file = open(oc_symbol_file_path, 'r+')
        block_sym_file = open(block_symbol_file_path, 'r+')
        cstring_file = open(cstring_file_path, 'r+')

        #oc符号随机重排
        f.write('# oc_symbol')
        f.write('\n')
        oc_sym_list = oc_sym_file.readlines()
        shuffle(oc_sym_list)
        for line in oc_sym_list:
            f.write(line)

        f.write('# block_symbol')
        f.write('\n')
        block_sym_list = block_sym_file.readlines()
        shuffle(block_sym_list)
        for line in block_sym_list:
            f.write(line)

        f.write('# c_string')
        f.write('\n')
        cstring_list = cstring_file.readlines()
        shuffle(cstring_list)
        for line in cstring_list:
            f.write(line)


#查找_Text段的信息
str_addr_key = 'start_addr'
end_addr_key = 'end_addr'
seg_name_key = 'seg_name_key'
sect_name_key = 'sect_name_key'

def get_TEXT_info(file_path):
    info_arr = []
    with open(file_path,'r+',encoding='utf-8',errors='ignore') as f:
        for line in f:
            line = re.sub(r'\s',' ',line)
            if re.search(__TEXT_info_regex,line):
                parts = line.split(r' ')
                start_addr = parts[0]
                segment_name = parts[2]
                section_name = parts[3]
                sect_info_dict = {
                    str_addr_key:start_addr,
                    end_addr_key:0,
                    seg_name_key:segment_name,
                    sect_name_key:section_name
                }

                if not len(info_arr) == 0:
                    last_dict = info_arr[-1]
                    last_dict[end_addr_key] = start_addr
                info_arr.append( sect_info_dict)

    print(info_arr)
    return info_arr

def str2hex(s):
    odata = 0;
    su = s.upper()
    for c in su:
        tmp = ord(c)
        if tmp <= ord('9'):
            odata = odata << 4
            odata += tmp - ord('0')
        elif ord('A') <= tmp <= ord('F'):
            odata = odata << 4
            odata += tmp - ord('A') + 10
    return odata

if __name__ == '__main__':
    root_path = '/Users/guanzhenfa/Documents/project/sdk_diff_compare'
    link_info_filename = 'link_file.txt'
    order_filename = 'order_file.txt'

    parse_symbol(root_path,link_info_filename)
