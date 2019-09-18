#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import plistlib
import re
import shutil
import datetime

config_path = '/Users/guanzhenfa/Documents/company_git/iOS_RandomSDK/package_config.plist' #配置文件路径
sdk_helper_path = '/Users/guanzhenfa/Documents/company_git/iOS_RandomSDK/SDKHelper(1).m' #sdkhelper 的文件路径

iphoneos = 'iphoneos'
iphonesimulator = 'iphonesimulator'
order_file_path = ''
configuration = '' #从配置文件中读取,表示打包是Debug环境还是Release环境
sdk = '' #从配置文件中读取,表示打包是用iphoneos还是iphonesimulator或者both
output = '' #从配置文件中读取,打好的包将输出在这个文件夹里
targets_info = {} #<target_name:class name>
target_names = {} #用于替换注册文件中的placeholder
register_file_name = 'ModuleRegisterManager.h'
register_backup_path = ''
build_date = ''

def package(proj_name, proj_path, target_name,output):

    clean(proj_path,target_name)
    if sdk.lower() == 'both':
        build(proj_name,proj_path,target_name,iphoneos,configuration,output)
        build(proj_name, proj_path, target_name, iphonesimulator, configuration, output)
    else:
        build(proj_name,proj_path,target_name,sdk,configuration,output)

def package_core(proj_name, proj_path, target_name,output):

    clean(proj_path, target_name)
    if sdk.lower() == 'both':
        build(proj_name, proj_path, target_name, iphoneos, configuration, output,is_sdk_core=True)
        build(proj_name, proj_path, target_name, iphonesimulator, configuration, output,is_sdk_core=True)
    else:
        build(proj_name, proj_path, target_name, sdk, configuration, output,is_sdk_core=True)

def clean(proj_path, target_name):
    project = '-project %s'%proj_path
    targrt = '-target %s'%target_name
    sentence = 'xcodebuild clean %s %s -configuration %s'%(project,targrt,configuration)
    print(sentence)
    os.system(sentence)

def build(proj_name,proj_path, target_name,sdk,configuration,output, is_sdk_core=False):

    output_path = get_output_path(output,sdk)
    project = '-project %s' % proj_path
    target = '-target %s' % target_name
    log_path = os.path.join(output_path,'log')
    if not os.path.isdir(log_path):
        os.makedirs(log_path)
    log_path = os.path.join(log_path,proj_name + '.txt')
    sentence = ''
    if is_sdk_core:
        sentence = 'xcodebuild build %s %s -sdk %s -configuration %s ' \
                   'CONFIGURATION_BUILD_DIR=%s ' \
                   'MACH_O_TYPE=mh_dylib ' \
                   'DEBUG_INFORMATION_FORMAT=dwarf-with-dsym ' \
                   'ORDER_FILE=%s ' \
                   '> %s' % (
            project,
            target,
            sdk,
            configuration,
            output_path,
            order_file_path,
            log_path)
    else:
        sentence = 'xcodebuild build %s %s -sdk %s -configuration %s ' \
                   'CONFIGURATION_BUILD_DIR=%s ' \
                   'MACH_O_TYPE=staticlib ' \
                   '> %s' % (
        project,
        target,
        sdk,
        configuration,
        output_path,
        log_path)

    print(sentence)
    os.system(sentence)

def get_output_path(output,sdk):
    output = os.path.join(output, build_date + '/' + sdk)
    if not os.path.isdir(output):
        os.makedirs(output)
    return output

def re_write_register_file(register_file_path):
    dir_path,fname = os.path.split(register_file_path)
    orig_register_file = os.path.join(dir_path,register_file_name)
    target_ui = 'target_ui'
    target_register = 'target_register'
    target_login = 'target_login'
    target_network = 'target_network'
    target_uicompoent = 'target_uicompoent'
    target_storage = 'target_storage'
    target_iap = 'target_iap'
    temperary_file_path = os.path.join(dir_path,'register_temp.h')
    #备份
    register_backup_path = os.path.join(dir_path,'register_backup.h')
    back_up = open(register_backup_path, 'w+')
    shutil.copyfile(orig_register_file,register_backup_path)
    back_up.close()

    with open(register_file_path,'r+') as template:
        temp = open(temperary_file_path,'w+')
        for line in template:
            #根据配置修改模块名
            if re.search(target_uicompoent,line):
                if re.search('#define',line):
                    line = re.sub(target_uicompoent,targets_info[target_uicompoent],line)
                elif re.search('import',line):
                    line = re.sub(target_uicompoent, target_names[target_uicompoent], line)

            elif re.search(target_ui,line):
                if re.search('#define',line):
                    line = re.sub(target_ui, targets_info[target_ui], line)
                elif re.search('import',line):
                    line = re.sub(target_ui, target_names[target_ui], line)

            elif re.search(target_register,line):
                if re.search('#define',line):
                    line = re.sub(target_register, targets_info[target_register], line)
                elif re.search('import',line):
                    line = re.sub(target_register, target_names[target_register], line)

            elif re.search(target_network,line):
                if re.search('#define',line):
                    line = re.sub(target_network, targets_info[target_network], line)
                elif re.search('import',line):
                    line = re.sub(target_network, target_names[target_network], line)

            elif re.search(target_storage,line):
                if re.search('#define',line):
                    line = re.sub(target_storage, targets_info[target_storage], line)
                elif re.search('import',line):
                    line = re.sub(target_storage, target_names[target_storage], line)

            elif re.search(target_iap,line):
                if re.search('#define',line):
                    line = re.sub(target_iap, targets_info[target_iap], line)
                elif re.search('import',line):
                    line = re.sub(target_iap, target_names[target_iap], line)

            elif re.search(target_login,line):
                if re.search('#define',line):
                    line = re.sub(target_login, targets_info[target_login], line)
                elif re.search('import',line):
                    line = re.sub(target_login, target_names[target_login], line)

            temp.write(line)
        temp.close()
        back_up.close()

    with open(orig_register_file,'w+') as re_file:
        temp = open(temperary_file_path,'r+')
        re_file.seek(0)
        re_file.truncate()
        for line in temp:
            re_file.write(line)
        temp.close()

    return register_backup_path,orig_register_file


def recover_register_file(back_up_file_path,orig_register_file):
    with open(orig_register_file,'w+') as re_file:
        temp = open(back_up_file_path,'r+')
        re_file.seek(0)
        re_file.truncate()
        for line in temp:
            re_file.write(line)
        temp.close()

def combine():
    if sdk.lower() == 'both':
        sdkcore = 'SDKCore.framework/SDKCore'
        sdkcore_framwork_path = os.path.join(get_output_path(output,iphoneos),'SDKCore.framework')
        sdkcore_iphoneos_path = os.path.join(get_output_path(output,iphoneos),sdkcore)
        sdkcore_iphonesim_path = os.path.join(get_output_path(output,iphonesimulator),sdkcore)

        temp_path = get_output_path(output,'both')
        os.system('cp -r %s %s'%(sdkcore_framwork_path,temp_path))
        os.system('lipo -create %s %s -o %s'%(sdkcore_iphoneos_path,
                                              sdkcore_iphonesim_path,
                                              os.path.join(temp_path,sdkcore)))

if __name__ == '__main__':

    build_date = datetime.datetime.now().strftime('%Y-%m-%d_%H_%M_%S')

    with open(config_path,'rb') as f:
        config_dict = plistlib.load(f)
        sdk = config_dict['sdk']
        configuration = config_dict['configuration']
        output = config_dict['output_path']
        register_temp_file_path = config_dict['register_templet_file']
        order_file_path = config_dict['order_file_path']
        module_dict = config_dict['Module']
        layer_dict = config_dict['FunctionLayer']
        core_dict = config_dict['Core']

        #矫正
        if configuration.lower() == 'debug':
            configuration = 'Debug'
        elif configuration.lower() == 'release':
            configuration = 'Release'


        for func_l in layer_dict:
            class_name = func_l['class_name']
            target_name = func_l['target_name']
            key = func_l['placeholder']
            targets_info[key] = class_name
            target_names[key] = target_name

        for module in module_dict:
            class_name = module['class_name']
            target_name = module['target_name']
            key = module['placeholder']
            targets_info[key] = class_name
            target_names[key] = target_name

        register_backup_path, orig_register_file = re_write_register_file(register_temp_file_path)

        # function layer
        for func_l in layer_dict:
            proj_name = func_l['project_name']
            proj_path = func_l['project_path']
            target_name = func_l['target_name']
            package(proj_name, proj_path, target_name,output)
            print('func_l: %s %s %s'%(proj_name, proj_path, target_name))

        #module layer
        for module in module_dict:
            proj_name = module['project_name']
            proj_path = module['project_path']
            target_name = module['target_name']
            package(proj_name, proj_path, target_name,output)
            print('module: %s %s %s' % (proj_name, proj_path, target_name))


        #core
        proj_name = core_dict['project_name']
        proj_path = core_dict['project_path']
        target_name = core_dict['target_name']
        package_core(proj_name,proj_path,target_name,output)
        print('core: %s %s %s' % (proj_name, proj_path, target_name))

        combine()
        recover_register_file(register_backup_path,orig_register_file)
        shutil.copy(sdk_helper_path,output)

        os.system('open %s'%output)