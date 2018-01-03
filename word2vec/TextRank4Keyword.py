#-*- encoding:utf-8 -*-
from  textrank4zh import TextRank4Keyword,TextRank4Sentence
import codecs

file = "..\docment\content12.txt"
text = codecs.open(file,'r','utf-8').read()
#text ="年龄在60周岁以上的，持有大型客车、牵引车、城市公交车、中型客车、大型货车驾驶证的，可以在本平台办理超龄换证业务，申请换领准驾车型为小型汽车或者小型自动挡汽车的机动车驾驶证；年龄在70周岁以上的，持有普通三轮摩托车、普通二轮摩托车驾驶证的，可以在本平台办理超龄换证业务，申请换领准驾车型为轻便摩托车的机动车驾驶证。 网上办理超龄换证业务，需先到指定医院（体检医院）进行体检并获取《机动车驾驶人身体条件证明》。"
word = TextRank4Keyword()

word.analyze(text,window = 2,lower = True)
w_list = word.get_keywords(num = 20,word_min_len = 1)

print ('关键词:')
for w in w_list:
    print (w.word,w.weight)
phrase = word.get_keyphrases(keywords_num = 5,min_occur_num=2)

print ('关键词组:')
for p in phrase:
    print (p)
sentence = TextRank4Sentence()
sentence.analyze(text,lower = True)
s_list = sentence.get_key_sentences(num = 3,sentence_min_len = 5)

print( '关键句:')
for s in s_list:
    print (s.sentence,s.weight)



