# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 14:33:54 2017

@author: first
"""
'''
class gensim.models.word2vec.Word2Vec(
sentences=None,size=100,alpha=0.025,window=5, 
min_count=5, max_vocab_size=None, sample=0.001,seed=1, 
workers=3,min_alpha=0.0001, sg=0, hs=0, negative=5, 
cbow_mean=1, hashfxn=<built-in function hash>,iter=5,
null_word=0, trim_rule=None, sorted_vocab=1, batch_words=10000)
参数：
·  sentences：可以是一个·ist，对于大语料集，建议使用BrownCorpus,Text8Corpus或·ineSentence构建。
·  sg： 用于设置训练算法，默认为0，对应CBOW算法；sg=1则采用skip-gram算法。
·  size：是指特征向量的维度，默认为100。大的size需要更多的训练数据,但是效果会更好. 推荐值为几十到几百。
·  window：表示当前词与预测词在一个句子中的最大距离是多少
·  alpha: 是学习速率
·  seed：用于随机数发生器。与初始化词向量有关。
·  min_count: 可以对字典做截断. 词频少于min_count次数的单词会被丢弃掉, 默认值为5
·  max_vocab_size: 设置词向量构建期间的RAM限制。如果所有独立单词个数超过这个，则就消除掉其中最不频繁的一个。每一千万个单词需要大约1GB的RAM。设置成None则没有限制。
·  sample: 高频词汇的随机降采样的配置阈值，默认为1e-3，范围是(0,1e-5)
·  workers：参数控制训练的并行数。
·  hs: 如果为1则会采用hierarchica·softmax技巧。如果设置为0（defau·t），则negative sampling会被使用。
·  negative: 如果>0,则会采用negativesamp·ing，用于设置多少个noise words
·  cbow_mean: 如果为0，则采用上下文词向量的和，如果为1（defau·t）则采用均值。只有使用CBOW的时候才起作用。
·  hashfxn： hash函数来初始化权重。默认使用python的hash函数
·  iter： 迭代次数，默认为5
·  trim_rule： 用于设置词汇表的整理规则，指定那些单词要留下，哪些要被删除。可以设置为None（min_count会被使用）或者一个接受()并返回RU·E_DISCARD,uti·s.RU·E_KEEP或者uti·s.RU·E_DEFAU·T的函数。
·  sorted_vocab： 如果为1（defau·t），则在分配word index 的时候会先对单词基于频率降序排序。
·  batch_words：每一批的传递给线程的单词的数量，默认为10000
'''
#encoding=utf-8
import os
import time
import numpy
import jieba
import participle
import re
from gensim.models import word2vec
from html.parser import HTMLParser
#from gensim.models.keyedvectors import KeyedVectors

docment_path = "../docment/"
output_path  = "../output/"
config_path = "../config/"

def sigmoid(x,a,c):
    return 1.0 / (1.0 + numpy.exp(-a*(x-c)))

def cosine(a,b):
    dist = numpy.dot(a,b)/(numpy.linalg.norm(a)*numpy.linalg.norm(b))
    return dist

def word2vec_process(model_name):
    model_name = output_path+model_name;
    if (os.path.isfile(model_name)):
        print ("find model")
        word2vec_model=word2vec.KeyedVectors.load_word2vec_format(model_name,binary=False)
        print ("model load success")
    else:#没有包含模型进行训练
        starttime = time.time()
        print ("process docment ...")
        participle.docment_to_word(docment_path,output_path+"docment_words.txt")#处理数据
        print ("goto training ...")
        #sentences=word2vec.Text8Corpus('text8.txt')
        sentences=word2vec.LineSentence(output_path+'docment_words.txt')
        word2vec_model=word2vec.Word2Vec(sentences,window=10,min_count=20,sg=1,iter=5,size=50,workers=4,alpha=0.010)
        word2vec_model.wv.save_word2vec_format(model_name,binary=False)
        word2vec_model.wv.save_word2vec_format(model_name+".bin",binary=True)
        print ("end training")
        endtime = time.time()
        print ("\ntotal time:%3d"%(endtime - starttime)+"s")
    #model.train(sentences)
    
    function  = input("\n\nPlease select function:\n1:word to word \n2:doc to doc\n\n");
    if function == '1':
        inputfile = open(model_name,"r+", encoding='UTF-8')#获取文件句柄 二进制方式读取
        while(True):
            input_word = input("\n\nPlease input words:\n\n")
            if input_word.upper() == "Q" :
                break
            inputfile.seek(0)
            for fileline in inputfile:
                list_str = fileline.split(' ')
                if input_word == list_str[0]:
                    for dest in word2vec_model.most_similar(input_word):
                        #if dest[1] >= 0.5:
                            print(dest[0],dest[1])
                    break
                #else:q
                #    print("Not find word in words\n")
        inputfile.close()
        print("exit success")
    elif function == '2':
        html_parser = HTMLParser()#转义处理html符号
        jieba.initialize()#手动初始化（可选） 手动进行加载 速度较快
        jieba.set_dictionary(config_path+'dict.txt.big')#设置主词库
        jieba.load_userdict(config_path+"dict.txt") #设置从词库
        filterfile = open(config_path+"filter.txt","r+",encoding= 'utf8')#过滤符号文件
        filterstr = ""
        filterstr += filterfile.readline().replace("\n","").strip()#读取转义符过滤文件 删除换行符与空格
        filterstr += filterfile.readline().replace("\n","").strip()#读取英文符号符过滤文件 删除换行符与空格
        filterstr += filterfile.readline().replace("\n","").strip()#读取中文符号过滤文件 删除换行符与空格
        
        sigmoid_a = -3
        sigmoid_c =1.5
        sigmoid_max = sigmoid(0,sigmoid_a,sigmoid_c)
        while(True):
            input_docment1 = input("Please input docment1:\n")
            if input_docment1.upper() == "Q" :break
            input_docment2 = input("Please input docment2:\n")
            if input_docment2.upper() == "Q" :break
        
            input_docment1 = html_parser.unescape(input_docment1)#删除转义符
            input_docment1 = input_docment1.upper();#全部转化为大写
            input_docment1 = re.sub(filterstr,"",input_docment1) #过滤标点符号 
            input_docment1 = participle.list_to_string(jieba.cut(input_docment1,cut_all=False,HMM=True)," ",[])

            input_docment2 = html_parser.unescape(input_docment2)#删除转义符
            input_docment2 = input_docment2.upper();#全部转化为大写
            input_docment2 = re.sub(filterstr,"",input_docment2) #过滤标点符号 
            input_docment2 = participle.list_to_string(jieba.cut(input_docment2,cut_all=False,HMM=True)," ",[])

            distance = word2vec_model.wmdistance(input_docment1.split(" "), input_docment2.split(" "))
            #distance = 1/(1+distance)
            print("\n"+input_docment1+" 与 "+input_docment2+"\n")
            print("distance is :%0.4f %0.2f%%"%(distance,100*sigmoid(distance,sigmoid_a,sigmoid_c)/sigmoid_max))
        print("exit success")
    else:
        print("exit success")

word2vec_process('word2vec_model.txt')#参数模型名称 是否属于二进制
#print(sigmoid(3.74,-3,2))  #1.0/(1.0+Math.pow(Math.e,-3*(x-2)) )
#print(sigmoid(3.74,-3,1.5))  #1.0/(1.0+Math.pow(Math.e,-3*(x-1.5)) )
    
    
    
    
    