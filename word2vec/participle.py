 # -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 14:00:11 2017

@author: first
"""
#encoding=utf-8
import time
import jieba
import sys
import re
import files_to_file
from html.parser import HTMLParser

docment_path = "../docment/"
output_path  = "../output/"
config_path = "../config/"

def list_to_string(source_list,sp,stop_list):#合并字符串
    outputstr = ""
    for element in source_list:
        line = element.replace(" ","").strip()#删除空格 删除换行符
        if len(line) != 0: #空字符直接跳过           
            outputstr += line + sp;#添加间隔
    return outputstr;#返回utf8数据格式

def viewBar(i):#显示状态栏
    #print ('\rcomplete percent:%.0f%%' % i)
    sys.stdout.write('\rcomplete percent:%.0f%%' % i)
    sys.stdout.flush()
    
def readfile_total_line(inputfile):#获取文件总行书
    count = 0
    for fileline in inputfile:
        count += 1
    inputfile.seek(0,0);
    return count

def docment_to_word(files,output):#把文档分词后保存
    files_to_file.save_files_to_file(files,postfix=".txt",objectfile=output_path+"docment.txt")#把一个目录的数据保存到txt文档中
    html_parser = HTMLParser()#转义处理html符号
    #jieba.enable_parallel()#开启并行分词
    jieba.initialize()#手动初始化（可选） 手动进行加载 速度较快
    jieba.set_dictionary(config_path+'dict.txt.big')#设置主词库
    jieba.load_userdict(config_path+"dict.txt") #设置从词库
    inputfile = open(output_path+"docment.txt","r+",encoding= 'utf8')#获取文件句柄 二进制方式读取
    outputfile = open(output,"w",encoding= 'utf8')#创建输出文件 二进制方式写入
    filterfile = open(config_path+"filter.txt","r+",encoding= 'utf8')#过滤符号文件
    starttime = time.time()#获取开始时间
    
    print ("start process...")
    input_total_line = readfile_total_line(inputfile)#获取总行数
    filterstr = ""
    filterstr += filterfile.readline().replace("\n","").strip()#读取转义符过滤文件 删除换行符与空格
    filterstr += filterfile.readline().replace("\n","").strip()#读取英文符号符过滤文件 删除换行符与空格
    filterstr += filterfile.readline().replace("\n","").strip()#读取中文符号过滤文件 删除换行符与空格
    
    #print(filterstr.replace("\n",""))
    filterfile.close()#关闭过滤文件
    nlinechar   = 0#换行计数
    ndisplay    = 0#显示计数
    process_line= 0#是否显示

    for fileline in inputfile:
        process_line += 1
        fileline = html_parser.unescape(fileline)#删除转义符
        fileline = fileline.upper();#全部转化为大写
        fileline = re.sub(filterstr,"",fileline) #过滤标点符号 
        convline = list_to_string(jieba.cut(fileline,cut_all=False,HMM=True)," ",[])#进行分类转化 关闭HMM分词功能
        if len(convline) != 0:
            outputfile.write(convline)#保存转化后的文件
        #以下是添加换行符
        nlinechar  += len(convline)#记录文件大小
        if nlinechar >= 1000:
            outputfile.write("\n")#以上是添加换行符
            nlinechar = 0
        ndisplay += 1;
        if ndisplay >= 1000:#大于两千进行写入操作
            ndisplay=0
            viewBar((process_line/input_total_line)*100)#输出进度
            outputfile.flush()#写入磁盘  

    endtime = time.time()
    inputfile.close()
    outputfile.close()
    print ("\ntotal time:%3d"%(endtime - starttime)+"s")
