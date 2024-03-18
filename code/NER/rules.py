# encoding=utf8
import nltk, json

from .tools import ner_stanford, cut_stanford


def get_stanford_ner_nodes(parent):
    # 对得到的树进行遍历
    date = ''
    num = ''
    org = ''
    loc = ''
    for node in parent:
        if type(node) is nltk.Tree:
            if node.label() == 'DATE':
                date = date + " " + ''.join([i[0] for i in node])
            elif node.label() == 'NUMBER':
                num = num + " " + ''.join([i[0] for i in node])

            elif node.label() == 'ORGANIZATIONL':
                org = org + " " + ''.join([i[0] for i in node])
            elif node.label() == 'LOCATION':
                loc = loc + " " + ''.join([i[0] for i in node])
    if len(num) > 0 or len(date) > 0 or len(org) > 0 or len(loc) > 0:
        return {'date': date, 'num': num, 'org': org, 'loc': loc}
    else:
        return {}


def grammer_parse(raw_sentence=None, file_object=None):
    # assert grammer_type in set(['hanlp_keep','stanford_ner_drop','stanford_pos_drop'])
    # 如果文本太短，则直接跳过
    if len(raw_sentence.strip()) < 5:
        return False
    # 定义语法：<DATE>+  只要Date出现，一次或者多次，都是属于一个Date
    grammer_dict = \
        {

            'stanford_ner_drop': r"""
        DATE:{<DATE>+<MISC>?<DATE>*<O>{2}}
        {<DATE>+<MISC>?<DATE>*}
        {<DATE>+}
        {<TIME>+}
        ORGANIZATIONL:{<ORGANIZATION>+}
        LOCATION:{<LOCATION|STATE_OR_PROVINCE|CITY|COUNTRY>+}
        """
        }
    # 通过NLTK来对语法进行解析
    stanford_ner_drop_rp = nltk.RegexpParser(grammer_dict['stanford_ner_drop'])
    try:
        # ner_stanford(raw_sentence)就是将关键字命名体进行了识别，O指的意思是没有我们规定的类型
        # 得到的stanford_ner_drop_result为draw类型，可以通过draw()方法进行绘制
        stanford_ner_drop_result = stanford_ner_drop_rp.parse(ner_stanford(raw_sentence))

    except:
        print("the error sentence is {}".format(raw_sentence))
    else:
        # 将得到的树类型的结果按照规则对结点进行合并
        stanford_keep_drop_dict = get_stanford_ner_nodes(stanford_ner_drop_result)
        if len(stanford_keep_drop_dict) > 0:
            # 将字典写入文件，通过json.dumps将字符串转化为json数据
            file_object.write(json.dumps(stanford_keep_drop_dict, skipkeys=False,
                                         ensure_ascii=False,
                                         check_circular=True,
                                         allow_nan=True,
                                         cls=None,
                                         indent=4,
                                         separators=None,
                                         default=None,
                                         sort_keys=False))
