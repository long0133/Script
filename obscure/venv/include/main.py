#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import re
import hashlib
import random

map = {}
obscure_file_keyname = ['MC','Module','Storage','UICompoent','Network','SDKEntrance']
brace_regex = r'\(.*?\)(\w*)|(\{)' #正则匹配方法名中的如 (NSString *)pwd
find_invoke_regex = r'\[.*\];' #查找匹配方法的调用
find_method_name_regex = r'(\+|-)\s(\(.*\))(.*)(\{|\s)' #查找方法名

#遍历.h文件 查找带有mo_ mc_ mp_开头的方法,并且混淆记录到map中
def obscure_prepare(root_path):
    file_list = os.listdir(root_path)
    for fn in file_list:
        file_path = os.path.join(root_path,fn)
        if not os.path.isdir(file_path):
            #非文件夹
            if fn.endswith('.h'):
                with open(file_path,'r+') as f:
                    for line in f:
                        if re.search('mo_',line) or re.search('mc_',line) or re.search('mp_',line):
                            method_name = line.split(';')[0]
                            signature = get_methodsignature(method_name)
                            make_diff_map(signature)

        else:
            obscure_prepare(file_path)

#遍历.m文件 根据map里的key value进行文件里 方法实现的混淆 以及方法调用的混淆
def obscure(root_path):

    file_list = os.listdir(root_path)
    for fn in file_list:
        file_path = os.path.join(root_path, fn)
        if not os.path.isdir(file_path):
            flag = False
            for key in obscure_file_keyname:
                if re.search(key, fn):
                    flag = True
            if not flag: continue
            # 非文件夹
            if fn.endswith('.m'):
                #.m文件
                with open(file_path, 'r+') as f:
                    temp = open(get_temp_file_path(root_path,fn), 'r+')
                    for line in f:
                        if re.search('mo_', line) or re.search('mc_', line) or re.search('mp_', line):
                            if re.search(r'\[',line) or re.search(r']',line):
                                #提取完整的调用式
                                line = line.strip()
                                for k,v in map.items():
                                    if re.search(k,line):
                                        line = line.replace(k,v)
                            else:
                                if re.search('-',line) or re.search('\+',line):
                                    # 实现
                                    signature = get_methodsignature(line).strip()
                                    if len(signature) != 0:
                                        line = line.replace(signature,map[signature])
                                else:
                                    #其他
                                    for k, v in map.items():
                                        if re.search(k, line):
                                            line = line.replace(k, v)

                        temp.write(line)
                    f.seek(0)
                    f.truncate()
                    f.write(temp.read())
                    temp.close()
            elif fn.endswith('.h'):
                #.h文件
                with open(file_path,'r+') as f:
                    temp = open(get_temp_file_path(root_path, fn), 'r+')
                    for line in f:
                        if re.search('-', line) or re.search('\+', line):
                            # 实现
                            signature = get_methodsignature(line).strip().replace(';','')
                            if signature in map.keys():
                                line = line.replace(signature, map[signature])
                            else:
                                print('not included: ', signature)
                        temp.write(line)
                    f.seek(0)
                    f.truncate()
                    f.write(temp.read())
                    temp.close()
        else:
            obscure(file_path)

def get_temp_file_path(root_path,fn):
    # temp_path_dir = os.path.join(root_path, 'temp')
    # if not os.path.isdir(temp_path_dir):
    #     os.makedirs(temp_path_dir)
    temp_path_file = os.path.join(root_path, fn)
    return temp_path_file

def get_temp_file_path_for_class_ob(root_path,fn):
    # temp_path_dir = os.path.join(root_path, 'temp')
    # if not os.path.isdir(temp_path_dir):
    #     os.makedirs(temp_path_dir)
    temp_path_file = os.path.join(root_path, 'temp_'+fn)
    return temp_path_file

#混淆方法的实现
def make_diff_map(signature):
    md5 = hashlib.md5(signature.encode('utf-8')).hexdigest()
    if signature.endswith(':'):
        md5 = md5 + ':'
    map[signature] = 'obscure_' + md5

#获取方法的方法签名
def get_methodsignature(method_name):
    method_name = method_name.split(')',1)[-1]
    signature = re.sub(brace_regex,'',method_name)
    #只取方法签名的第一段做混淆
    sig = signature.split(' ')[0]
    # print(sig + '------' + method_name)
    return sig

###################Class Obscure############################
class_map = {}
interface_regex = r'[\s]*@interface+[\s]*[_a-zA-Z]+([\s]+)'
ignore_list = ['AppDelegate','ViewController']

def class_obscure_prepare(root_path):
    file_list = os.listdir(root_path)
    for fn in file_list:
        file_path = os.path.join(root_path,fn)
        if not os.path.isdir(file_path):
            if fn.endswith('.h'):
                with open(file_path,'r+') as f:
                    for line in f:
                        if re.search(interface_regex,line):
                            class_name = extract_class_name(line)
                            if class_name.startswith('UI') or class_name.startswith('NS') or class_name.startswith('App'):
                                continue
                            if not class_name in ignore_list:
                                class_map[class_name] = obscure_class_name(class_name)
        else:
            class_obscure_prepare(file_path)

def class_obscure(root_path):
    file_list = os.listdir(root_path)
    for fn in file_list:
        file_path = os.path.join(root_path, fn)
        if not os.path.isdir(file_path):
            if fn.endswith('.h') or fn.endswith('.m'):
                pure_file_name = fn.split('.')[0]
                # print(pure_file_name)
                with open(file_path,'r+') as f:
                    temp = open(get_temp_file_path_for_class_ob(root_path,fn),'w+',encoding='utf-8',errors='ignore')
                    for line in f:
                        if re.search('#import',line):
                            #文件import不做修改
                            temp.write(line)
                            continue
                        for k,v in class_map.items():
                            if re.search(k, line):
                                line = re.sub(k,v,line)
                        temp.write(line)
                    temp.close()

                    with open(get_temp_file_path_for_class_ob(root_path,fn),'r+') as temp_file:
                        f.seek(0)
                        f.truncate()
                        for line in temp_file:
                            f.write(line)
                    # f.seek(0)
                    # f.truncate()
                    # f.write(temp.read())

        else:
            class_obscure(file_path)

def extract_class_name(raw):
    raw = raw.split(':')[0]
    raw = raw.strip().replace('@interface', '')
    raw = raw.split('(')[0]
    return raw.strip()

def obscure_class_name(class_name):
    class_name = hashlib.md5(class_name.encode('utf-8')).hexdigest()
    return 'mc' + ranstr(5);

def ranstr(num):
    H = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

    salt = ''
    for i in range(num):
        salt += random.choice(H)

    return salt

if __name__ == '__main__':
    root_path = '/Users/guanzhenfa/Documents/git/RandomSDK'
    # obscure_prepare(root_path)
    # print(map)
    # obscure(root_path)

    class_obscure_prepare(root_path)
    class_obscure(root_path)
    print(class_map)