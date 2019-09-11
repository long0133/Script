#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import re
import hashlib
import random
import base64



################### Method Obscure ############################
map = {}
obscure_file_blacklist = []  # 文件名黑名单 这些.h文件里的方法将不会被混淆
obscure_method_keywords_blacklist = ['DEPRECATED_MSG_ATTRIBUTE','__deprecated_msg'] # 方法名关键字黑名单
obscure_method_prefix = ['mo_','mc_','mp_','i_','p_','c_']  # 如有值则只修改带有这些前缀的方法
brace_regex = r'\s?:\s?\([\w<>^()\*\s,]*\)\s?[\w]*'  # 正则匹配方法名中的如 (NSString *)pwd
find_invoke_regex = r'\[.*\];'  # 查找匹配方法的调用
find_method_name_regex = r'(\+|-)\s(\(.*\))(.*)(\{|\s)'  # 查找方法名
method_verify_regex = r'[a-zA-Z0-9_]*'
temp_file_paths_arr = [] #临时文件的数组

# 遍历.h文件 查找带有mo_ mc_ mp_开头的方法,并且混淆记录到map中
def obscure_prepare(root_path):
    file_list = os.listdir(root_path)
    for fn in file_list:
        file_path = os.path.join(root_path, fn)
        if not os.path.isdir(file_path):
            # 非文件夹
            if fn.endswith('.h') or fn.endswith('.m'):
                if fn in obscure_file_blacklist:
                    continue
                with open(file_path, 'r+') as f:
                    for line in f:
                        if shoudl_obscure_method(line):
                            if re.match(find_method_name_regex, line):
                                method_name = line.split(';')[0]
                                method_name = method_name.split('{')[0]
                                # print(method_name)
                                signature = get_methodsignature(method_name)
                                for sub_sig in signature:
                                    make_diff_map(sub_sig)
                                # print(signature + '-----' + ob)

        else:
            obscure_prepare(file_path)


# 遍历.m文件 根据map里的key value进行文件里 方法实现的混淆 以及方法调用的混淆
def obscure(root_path):
    return
    file_list = os.listdir(root_path)
    for fn in file_list:
        file_path = os.path.join(root_path, fn)
        if not os.path.isdir(file_path):
            # print('处理文件: ' + fn)
            # 非文件夹
            if fn.endswith('.m') or fn.endswith('.h'):
                # .m文件
                with open(file_path, 'r+') as f:
                    temp_file_path = get_temp_file_path(root_path, fn)
                    temp_file_paths_arr.append(temp_file_path) #保存临时文件的地址,以便后续删除
                    temp = open(temp_file_path, 'w+',encoding='utf-8',errors='ignore')
                    for line in f:
                        if shoudl_obscure_method(line):
                            for k,v in map.items():
                                if len(k) != 0 and re.search(k,line):
                                    line = re.sub(k,v,line)
                        temp.write(line)
                    temp.close()

                    with open(get_temp_file_path(root_path,fn), 'r+') as temp_file:
                        f.seek(0)
                        f.truncate()
                        for line in temp_file:
                            f.write(line)
        else:
            obscure(file_path)


def shoudl_obscure_method(line):
    for prefix in obscure_method_prefix:
        if re.search(prefix, line):
            return True
    return False

def get_temp_file_path(root_path, fn):
    temp_path_file = os.path.join(root_path, 'temp_' + fn)
    return temp_path_file


# 混淆方法的实现
def make_diff_map(signature):

    for key in obscure_method_keywords_blacklist:
        if re.search(key,signature):
            return

    ob = ''
    if len(signature) <= 5:
        ob = ob + ranDomName2[random.randint(0,60) % len(ranDomName2)]
        ob = ob.lower()
    elif len(signature) > 5 and len(signature) <= 10:
        ob = ob + ranDomName2[random.randint(50, 100) % len(ranDomName2)]
        ob = ob.lower()
        ob = ob + ranDomName3[random.randint(0, 60) % len(ranDomName3)]
    else:
        ob = ob + ranDomName2[random.randint(50, 100) % len(ranDomName2)]
        ob = ob.lower()
        ob = ob + ranDomName3[random.randint(0, 60) % len(ranDomName3)]
        ob = ob + ranDomName4[random.randint(0, 60) % len(ranDomName4)]
    map[signature] = ob
    return ob


# 获取方法的方法签名
def get_methodsignature(method_name):

    for key in obscure_method_keywords_blacklist:
        if re.search(key,method_name):
            return []

    method_name = method_name.split(')', 1)[-1]
    signature = re.sub(brace_regex, ' ', method_name).strip()
    signature = re.sub(':', '',signature)
    sig = signature.split(' ')
    #目前仅取第一部分的签名
    first_part = sig[0]
    for prefix in obscure_method_prefix:
        if re.match(prefix,first_part):
            return [first_part]
    return []


################### ClassName Obscure ############################
class_map = {}
interface_regex = r'[\s]*@interface+[\s]*[_a-zA-Z]+([\s]+)'
ignore_list = ['AppDelegate', 'ViewController','SDKEntrance'] #不需要混淆的类名
ignore_dir_list = ['module_ui_three_724']
class_prefix = ''
ranDomName1 = ['ZYH', 'ZYH', 'ZYH', 'ZYH', 'ZYH', 'ZYH', 'COA', 'COA', 'COA', 'COA', 'COA', 'COA', 'NES', 'NES',
                'LOM', 'LOM', 'LOM', 'LOM', 'MEE', 'MEE', 'MEE']

ranDomName2 = ['The', 'Fog', 'TR', 'Haode', 'Xitong', 'Lunbotu', 'Shitu', 'Picture', 'Photo', 'Xieyi', 'Text', 'Rich',
               'Line', 'Sys', 'Turn', 'Rever', 'Tiaozhuan', 'Control', 'Noname', 'Name', 'Waker', 'Date', 'Weak', 'XML',
               'Hob', 'File', 'Function', 'Fanfa', 'Hob', 'COO', 'Program', 'Net', 'Device', 'SheBei', 'Didian',
               'People', 'Thing', 'Shijian', 'Shang', 'Shangbao', 'Other', 'Yanse', 'Color', 'Object', 'Animate',
               'Dongzuo', 'Word', 'Act', 'Different', 'Plus', 'Sub', 'Age', 'Newer', 'Login', 'Register', 'Huanxiao',
               'Length', 'Count', 'Jihuoma', 'Fly', 'Loop', 'Star', 'Get', 'Set', 'Get', 'Set', 'Get', 'Set', 'Get',
               'Set', 'Shenhe', 'Read', 'Write', 'Laker', 'Shanghai', 'Some', 'Get', 'Set', 'In', 'This', 'That',
               'String', 'Number', 'AAA', 'Main', 'Work', 'Enable', 'Disable', 'Check', 'Ment']

ranDomName3 = ['Welcome', 'In', 'Order', 'To', 'Get', 'First', 'Request', 'Some', 'Basic',
               'Information', 'One', 'Comes', 'Three' 'Pieces', 'The', 'Suite', 'Head', 'LLV', 'MMO', 'RPG', 'Game',
               'Random', 'Test', 'Length', 'FPS', 'Shumu', 'Tree', 'Heap', 'Value', 'Number', 'Ana', 'Bit', 'Use',
               'For', 'Date', 'Shangbao', 'Other', 'Yanse', 'Color', 'Object', 'Button', 'View', 'Image', 'View',
               'Load', 'Creat']

ranDomName4 = ['Singleton', 'Logger', 'Order', 'Person', 'Comp', 'Resp', '1', '2', '3', '4', '5', '6', 'Object', 'Figure', 'Cele',
               'Solider', 'Response', 'Calcuter', 'Menu', 'Wee', 'Suit', 'Gate', 'World', 'Car', 'Rp', 'Age',
               'Giving', 'Doing', 'Play', 'Add', 'Vce', 'Change', 'JSON', 'Standar', 'Adavance', 'Country', 'Check',
               'SSS', 'Host', 'Vic', 'Ter', 'Style', 'VC', 'Key', 'Style', 'CSS', 'Script', 'Test', 'Text', 'Tion',
               'Animate', 'Button', 'View', 'Image', 'SSL', 'Section', 'View', 'Seg', 'Load', 'Mon']

def class_obscure_prepare(root_path):
    file_list = os.listdir(root_path)
    for fn in file_list:
        if fn in ignore_dir_list:
            continue
        file_path = os.path.join(root_path, fn)
        if not os.path.isdir(file_path):
            if fn.endswith('.h'):
                with open(file_path, 'r+') as f:
                    for line in f:
                        if re.search(interface_regex, line):
                            class_name = extract_class_name(line)
                            if class_name.startswith('UI') or class_name.startswith('NS'):
                                continue
                            if not class_name in ignore_list:
                                if class_name == 'ModuleRegister':
                                    print(class_name)
                                class_map[class_name] = obscure_class_name_(class_name)
        else:
            class_obscure_prepare(file_path)


def class_obscure(root_path):
    file_list = os.listdir(root_path)
    for fn in file_list:
        file_path = os.path.join(root_path, fn)
        if not os.path.isdir(file_path):
            if fn.endswith('.h') or fn.endswith('.m'):
                # print(pure_file_name)
                with open(file_path, 'r+') as f:
                    temp = open(get_temp_file_path(root_path, fn), 'w+', encoding='utf-8', errors='ignore')
                    for line in f:
                        if re.search('#import', line):
                            # 文件import不做修改
                            temp.write(line)
                            continue
                        for k, v in class_map.items():
                            if re.search(k, line):
                                line = re.sub(k, v, line)
                        temp.write(line)
                    temp.close()

                    with open(get_temp_file_path(root_path, fn), 'r+') as temp_file:
                        f.seek(0)
                        f.truncate()
                        for line in temp_file:
                            f.write(line)

        else:
            class_obscure(file_path)

import plistlib
def package_plist_ob(root_path):
    file_list = os.listdir(root_path)
    for fn in file_list:
        file_path = os.path.join(root_path, fn)
        if not os.path.isdir(file_path):
            if fn == 'package_config.plist':
                with open(file_path,'rb') as f:
                    root_object = plistlib.load(f)
                    module_arr = root_object['Module']
                    layer_arr = root_object['FunctionLayer']
                    for index in range(0,len(layer_arr)):
                        func_l = layer_arr[index]
                        class_name = func_l['class_name']
                        if class_name in class_map:
                            ob_name = class_map[class_name]
                            print(class_name + '    ' + ob_name)
                            root_object['FunctionLayer'][index]['class_name'] = ob_name

                    for index in range(0,len(module_arr)):
                        module = module_arr[index]
                        class_name = module['class_name']
                        if class_name in class_map:
                            ob_name = class_map[class_name]
                            print(class_name + '    ' + ob_name)
                            root_object['Module'][index]['class_name'] = ob_name

                plistlib.writePlist(root_object, file_path)


        else:
            package_plist_ob(file_path)

def extract_class_name(raw):
    raw = raw.split(':')[0]
    raw = raw.strip().replace('@interface', '')
    raw = raw.split('(')[0]
    return raw.strip()


def obscure_class_name_(self):
    name1 = ranDomName1[random.randint(0, 50) % len(ranDomName1)]
    name2 = ranDomName2[random.randint(0, 200) % len(ranDomName2)]
    name3 = ranDomName3[random.randint(250, 500) % len(ranDomName3)]
    name4 = ranDomName4[random.randint(450, 800) % len(ranDomName4)]

    ob_class_name = name1+name2+name3+name4
    return ob_class_name

def save_map(root_path):
    dir = os.path.join(root_path,'obscure')
    if not os.path.isdir(dir):
        os.makedirs(dir)
    map_file = os.path.join(dir,'map_file.h')
    with open(map_file,'w+') as f:
        for classname in class_map.keys():
            f.write('#define %s %s \n'%(class_map[classname], classname))

def ranstr(num,uppercase=False):
    H = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
    if uppercase:
        H = 'ABCDEFGHIJKLMNOPQRSTUVWXY'

    salt = ''
    for i in range(num):
        salt += random.choice(H)

    return salt
################### fileName Obscure ############################
ignore_filename_list = ['ModuleRegister.h','ModuleRegister.m',
                        'register_backup.h','register_temp.h',
                        'ViewController.h','ViewController.m',
                        'AppDelegate.h','AppDelegate.m',
                        'main.m'] #.h .m文件名
filename_ob_map = {}
import_regex = r'#import ["<]?[a-zA-Z0-9/.]*[">]?'
real_header_name_regex = r'[A-Z]{1}[a-zA-Z0-9_]*(.h){1}'

def filename_obscure_prepare(root_path):
    filelist = os.listdir(root_path)
    for fn in filelist:
        file_path = os.path.join(root_path, fn)
        if not os.path.isdir(file_path):
            if not fn in ignore_filename_list:
                if fn.endswith('.h') or fn.endswith('.m'):
                    real_header_name = fn.split('.')[0]
                    filename_ob_map[real_header_name] = obscure_class_name_(fn)

        else:
            filename_obscure_prepare(file_path)

def filename_obscure(root_path):
    filelist = os.listdir(root_path)
    for fn in filelist:
        file_path = os.path.join(root_path, fn)
        if not os.path.isdir(file_path):
            if fn.endswith('.h') or fn.endswith('.m'):
                #更换文件内的import的文件名
                with open(file_path, 'r+') as f:
                    temp_path = get_temp_file_path(root_path, fn)
                    temp_file_paths_arr.append(temp_path)
                    temp = open(temp_path, 'w+')
                    for line in f:
                        if re.search(import_regex, line):
                            all = re.search(real_header_name_regex,line)
                            if all:
                                mach = all.group()
                                key = mach.split('.')[0]
                                if key in filename_ob_map.keys():

                                    line = re.sub(mach, filename_ob_map[key] + '.h',line)
                        temp.write(line)
                    temp.close()

                    with open(get_temp_file_path(root_path,fn),'r+') as temp:
                        f.seek(0)
                        f.truncate()
                        for line in temp:
                            f.write(line)

                #跟换此文件的文件名
                subs = fn.split('.')
                key = subs[0]
                type = subs[1]
                if key in filename_ob_map.keys():
                    file_ob_name = filename_ob_map[key] + '.' +type
                    ob_file_path = os.path.join(root_path,file_ob_name)
                    os.renames(file_path,ob_file_path)


        else:
            filename_obscure(file_path)


################### string Obscure #################################

string_regex = r'(@"){1}(.*)("){1}'
allow_string_ob_filename = ['Macro.h']
key_in_file = 'StorageProtocol.h' #ios 工程中定义了magic_number的文件, 在混淆时 需要根据magic_number更改工程中的magic_number值
magic_number = '0xaa'
chinese_regex = r'[\u4E00-\u9FA5]{1,}'

def string_obscure_encrypt(root_path):
    filelist = os.listdir(root_path)
    for fn in filelist:
        file_path = os.path.join(root_path, fn)
        if not os.path.isdir(file_path):
            if fn in allow_string_ob_filename:
                with open(file_path, 'r+') as f:
                    file_content = ''
                    for line in f:
                        #设置混淆开关为打开
                        if re.search('#define isMix',line):
                            line = '#define isMix true'

                        #混淆提取的字符串
                        match = re.search(string_regex,line)
                        if match:
                            if not re.search(chinese_regex,match.group()):
                                ob = xor_encrypt(match.group(),magic_number)
                                line = re.sub(string_regex,'%s'%ob,line)
                        file_content += line
                    f.seek(0)
                    f.truncate()
                    f.write(file_content)
            elif fn == key_in_file:
                with open(file_path, 'r+') as f:
                    file_content = ''
                    for line in f:
                        if re.search('#define magicNumber',line):
                            line = '#define magicNumber @"%s"'%magic_number
                        file_content += line

                    f.seek(0)
                    f.truncate()
                    f.write(file_content)
        else:
            string_obscure_encrypt(file_path)


def string_obscure_decrypt(root_path):
    pass

# def xor_encrypt(tips,key):
#
#     tips = tips.split('"')[1]
#     lkey = len(key)
#     secret = []
#     num = 0
#     for each in tips:
#         if num >= lkey:
#             num = num % lkey
#         char = (str(ord(each) ^ ord(key[num])))
#         secret.append(char)
#         num += 1
#     ob_bytes = "(char []) "
#     ob_bytes += '{' + ','.join(secret) + '}'
#     ob_bytes = '( ' + ob_bytes + ' )'
#     print(ob_bytes)
#     return ob_bytes

def xor_encrypt(tips,key):

    tips = tips.split('"')[1]
    lkey = len(key)
    secret = []
    num = 0
    for each in tips:
        if num >= lkey:
            num = num % lkey
        secret.append(chr(ord(each) ^ ord(key[num])))
        num += 1
    ob_bytes = "".join(secret).encode()
    return base64.b64encode(ob_bytes).decode()

def xor_decrypt(tips,key):
    tips = base64.b64decode(tips).decode()
    lkey=len(key)
    secret=[]
    num=0
    for each in tips:
        if num>=lkey:
            num=num%lkey
        secret.append( chr( ord(each)^ord(key[num]) ) )
        num+=1
    de_str = "".join( secret ).encode()
    return de_str

############################# Res Obscure ############################
import json
res_maping_file_name = 'zrscWork.json'
res_ob_map = {}

def res_ob_pre(res_path):
    ob_prefix = ranstr(3, True)
    if os.path.isdir(res_path):
        file_list = os.listdir(res_path)
        for fn in file_list:
            if fn == res_maping_file_name:
                sys_config_path = os.path.join(res_path, res_maping_file_name)
                with open(sys_config_path,'r+') as f:
                    sys_config_dict = json.load(f)
                    for k, v in sys_config_dict.items():
                        res_ob_map[v] = ob_prefix + ranstr(4) + k + 'Res'
                    print(res_ob_map)

                with open(sys_config_path,'r+') as f:
                    file_content = ''
                    for line in f:
                        for k, v in res_ob_map.items():
                            line = re.sub(k, v, line)
                        file_content += line
                    print(file_content)
                    f.seek(0)
                    f.truncate()
                    f.write(file_content)


def changeFileName(res_path):
    if os.path.isdir(res_path):
        file_list = os.listdir(res_path)
        for fn in file_list:
            fn_without_suffix = fn.split('.')[0]
            suffix = fn.split('.')[-1]
            old_path = os.path.join(res_path, fn)
            if fn_without_suffix in res_ob_map.keys():
                new_path = os.path.join(res_path, res_ob_map[fn_without_suffix] + '.' + suffix)
                os.renames(old_path, new_path)

def addGrabageFile(res_path):
    # 无效资源
    for i in range(0, 15):
        random_file_name = obscure_class_name_('')
        path = os.path.join(res_path, random_file_name + '.png')
        with open(path, 'w+') as f:
            f.write(ranstr(random.randint(300, 1000)))

######################################################################
def res_ob():
    res_path = '/Users/guanzhenfa/Documents/工作/V6SDK美术素材/test'
    res_ob_pre(res_path)
    changeFileName(res_path)
    addGrabageFile(res_path)

def method_ob():
    root_path = '/Users/guanzhenfa/Documents/company_git/iOS_RandomSDK'
    obscure_prepare(root_path)
    obscure(root_path)
    cleaning_up()


def class_name_ob():
    root_path = '/Users/guanzhenfa/Documents/company_git/iOS_RandomSDK'
    print('类名混淆准备...')
    class_obscure_prepare(root_path)
    print('开始混淆类名...')
    class_obscure(root_path)
    save_map(root_path)
    print('结束混淆类名...')
    package_plist_ob(root_path)


def file_name_ob():
    root_path = '/Users/guanzhenfa/Documents/company_git/iOS_RandomSDK'
    filename_obscure_prepare(root_path)
    print(filename_ob_map)
    filename_obscure(root_path)
    cleaning_up()

def string_ob():
    root_path = '/Users/guanzhenfa/Documents/company_git/iOS_RandomSDK'
    print('开始加密字符串...')
    string_obscure_encrypt(root_path)
    print('结束加密字符串...')

def cleaning_up():
    for path in temp_file_paths_arr:
        os.remove(path)

if __name__ == '__main__':
    class_prefix = ranstr(random.randint(2, 4), True)
    # class_name_ob()
    method_ob()
    # string_ob()
    res_ob()