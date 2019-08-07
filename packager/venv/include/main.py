#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import plistlib

config_path = '/Users/guanzhenfa/Documents/project/RandomSDK/package_config.plist'
configuration = ''
sdk = ''
output = ''

def package(proj_name, proj_path, target_name,output):

    clean(proj_path,target_name)
    if sdk.lower() == 'both':
        build(proj_name,proj_path,target_name,'iphoneos',configuration,output)
        build(proj_name, proj_path, target_name, 'iphonesimulator', configuration, output)
    else:
        build(proj_name,proj_path,target_name,sdk,configuration,output)

def clean(proj_path, target_name):
    project = '-project %s'%proj_path
    targrt = '-target %s'%target_name
    sentence = 'xcodebuild clean %s %s -configuration %s'%(project,targrt,configuration)
    print(sentence)
    os.system(sentence)

def build(proj_name,proj_path, target_name,sdk,configuration,output):

    output_path = prepare_output_path(output,sdk)
    project = '-project %s' % proj_path
    target = '-target %s' % target_name
    log_path = os.path.join(output_path,'log')
    if not os.path.isdir(log_path):
        os.makedirs(log_path)
    log_path = os.path.join(log_path,proj_name + '.txt')
    sentence = 'xcodebuild build %s %s -sdk %s -configuration %s CONFIGURATION_BUILD_DIR=%s > %s'%(project,
                                                                                                   target,
                                                                                                   sdk,
                                                                                                   configuration,
                                                                                                   output_path,
                                                                                                   log_path)
    print(sentence)
    os.system(sentence)

def prepare_output_path(output,sdk):
    output = os.path.join(output, sdk)
    if not os.path.isdir(output):
        os.makedirs(output)
    return output

def combine():
    pass

if __name__ == '__main__':

    with open(config_path,'rb') as f:
        config_dict = plistlib.load(f)
        sdk = config_dict['sdk']
        configuration = config_dict['configuration']
        output = config_dict['output_path']
        module_dict = config_dict['Module']
        layer_dict = config_dict['FunctionLayer']
        core_dict = config_dict['Core']

        #function layer
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
        package(proj_name,proj_path,target_name,output)
        print('core: %s %s %s' % (proj_name, proj_path, target_name))

        os.system('open %s'%output)