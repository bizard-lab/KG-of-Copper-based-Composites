#-*- coding=utf8 -*-
from grammer.rules import grammer_parse
fp = open('text.txt', 'r', encoding='utf8')
fout = open('out.txt','w',encoding='utf8')

[grammer_parse(line.strip(), fout) for line in fp if len(line.strip())>0]
fp.close()
fout.close()
