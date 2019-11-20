"""
Analyze gender distribution (overall / by city) in target WeChat group.
Generate word cloud art and perform sentiment analysis on signatures of group members by gender.
微信群分城市分性别信息统计，群成员签名词云与情感分析

@ Date: 2019-11-17
@ Author: OXPHOS
"""

import itchat
import pandas as pd
import matplotlib.pyplot as plt

import time
import json
import argparse

import jieba
import re
from googletrans import Translator
from textblob import TextBlob


def get_gender_info(name):
    """
    Extract gender count and ratio from given WeChat group
    从目标群中获取性别分布数量与比例
    
    :param name: the name of the target group / 群名
    :return: statistics of gender distribution in the target group / 性别统计信息
    """
    # Extract group meta data
    # 获取群信息
    roomlist =  itchat.search_chatrooms(name=name)
    chatroom = itchat.update_chatroom(roomlist[0]['UserName'], detailedMember=True)
    
    # Get gender information from target group
    # 获取性别统计信息
    members = chatroom['MemberList']
    stat = pd.Series(0, index=['M', 'F', 'O'])
    for i in range(len(members)):
        tsex = members[i]['Sex'];
        if tsex == 2:
            stat['F'] += 1
        elif tsex == 1:
            stat['M'] += 1
        else:
            stat['O'] += 1
    stat['M/F ratio'] = str(round(float(stat.M) / stat.F, 4))
    return stat


def get_gender_info_by_city(name):
    """
    Extract city-wise gender count and ratio from given WeChat group
    从目标群中获取分城市性别分布数量与比例

    :param name: the name of the target group / 群名
    :return: statistics of city-wise gender distribution in the target group / 性别统计信息
    """
    # Extract group meta data
    # 获取群信息
    roomlist = itchat.search_chatrooms(name=name)
    chatroom = itchat.update_chatroom(roomlist[0]['UserName'], detailedMember=True)

    # Get gender information from target group
    # 获取性别统计信息
    members = chatroom['MemberList']
    stat = pd.DataFrame(0, index=['PEK', 'SHA', 'SZX'], columns = ['O', 'M', 'F'])
    for i in range(len(members)):
        tsex = members[i]['Sex']
        info = members[i]['DisplayName']
        if '北京' in info or ('京' in info and
                            '南京' not in info and
                            '东京' not in info):
            stat.loc['PEK'].iloc[tsex] += 1
        elif '上海' in info or '沪' in info:
            stat.loc['SHA'].iloc[tsex] += 1
        elif '深' in info:
            stat.loc['SZX'].iloc[tsex] += 1
    stat['M/F ratio'] = stat.M/stat.F

    # Plot gender ratio and total number of members at given cities
    # 作图显示目标城市在群中的人数，以及男女比
    ax1 = plt.subplot()
    ax1.plot(stat['M/F ratio'], '.-', color='darkblue')
    ax1.set_ylabel('Male/Female Ratio')
    ax2 = ax1.twinx()
    ax2.bar(stat.index, stat.M + stat.F + stat.O, color='orange', alpha=0.5, width=0.5)
    ax2.set_ylabel('Total number')
    ax2.set_ylim([0, (max(stat.M + stat.F + stat.O)/10+1)*10])
    ax2.legend(['Total number'])
    plt.savefig('%s_Group_gender_ratio_by_city.png' %name)

    return stat


def get_signature_by_gender(name):
    """
    Extract signatures from all group members by gender
    获取群内男、女成员签名

    :param name: the name of the target group / 群名
    :return: Signatures of male and female members / 男、女成员签名
    """
    roomlist =  itchat.search_chatrooms(name=name)
    chatroom = itchat.update_chatroom(roomlist[0]['UserName'], detailedMember=True)
    members = chatroom['MemberList']
    res_m, res_f = {}, {}

    for i in range(len(members)):
        tmp = members[i]['Signature']
        if tmp:
            if members[i]['Sex'] == 1:
                res_m[members[i]['DisplayName']] = tmp
            if members[i]['Sex'] == 2:
                res_f[members[i]['DisplayName']] = tmp

    return {'Male': res_m, 'Female': res_f}


def parse_signatures(bag_of_signatures, separator):
    """
    Parse Chinese sentences into words
    分词
    
    :param bag_of_signatures:  A dictionary composed of {group name: signature list} 
    :param separator: The separator used for word cloud input / 词云输入文件单词分隔符
    :return: A dictionary composed of {group name: word list} 
    """
    def words_in_text(text):
        # Remove emojis
        result = re.sub(r"<span.*\/span>", "", text, flags=re.I)

        # Extract all unicode symbols
        result = ' '.join(re.findall("(\w+\'*\w+)", result))
        seg_list = jieba.cut(result)
        result = ",".join(seg_list)
        result = result.replace(', ,', separator)
        result = result.replace(',', separator)

        return result

    bag_of_words = {}
    for grp, person_signatures in bag_of_signatures.items():
        bag_of_words[grp] = words_in_text('###'.join(person_signatures.values()))
    return bag_of_words


def sentiment_analysis(bag_of_words, translator):
    """
    Perform polarity and subjectivity analysis with extracted words in groups
    借助谷歌翻译与TextBlob 对抽取出来的（分组）单词进行极性与主观性分析
    
    :param bag_of_words: A dictionary composed of {group name: word list} 
    :param translator: instance of a translator / 翻译机实例
    """
    print('---Translating---')

    def translate(text):
        """
        Translate Chinese words into English 
        中文单词->英文
        :param text: list of words to be translated / 待翻译单词列表 
        :return: translation in String，separated with comma / 翻译后文本（字符串形式，以逗号连接）
        
        # TODO: Translation can be slow. Consider multi-processing，or sentiment analysis package for Chinese.
        # TODO: 翻译速度可能会慢。考虑调整为多线程，或尝试其它中文情感分析资源。
        """
        trans = []
        error_words = []
        # Translate word by word
        # 按照单词进行翻译
        for w in text.split(','):
            try:
                translation = translator.translate(w, dest='en')
                trans.append(translation.text)
                time.sleep(5)
            except:
                error_words.append(w)

        return ','.join(trans)

    # param sanity check
    # 输入类型检查
    if not isinstance(bag_of_words, dict):
        print('TypeError: subgroups of the signatures and subgroup names are required (in Dict format).')
        return

    # Sentiment analysis by groups
    # 分组情感分析
    for grp, words in bag_of_words.items():
        print('%s:' %grp, TextBlob(translate(words)).sentiment)

    return


if __name__ == '__main__':
    # QR code for WeChat login
    # 微信登录二维码
    itchat.auto_login(hotReload=1)

    parser = argparse.ArgumentParser()
    parser.add_argument('group_name', type=str, help='Name of the WeChat group to be analyzed.') # 群名
    parser.add_argument('--run_all', type=bool, default=False, help='Run all functions below.')  # 运行全部功能
    parser.add_argument('--gender_info', type=bool, default=False, help='Extract gender information.') # 抽取性别信息
    parser.add_argument('--gender_info_by_city', type=bool, default=False,
                        help='Extract gender information by city if available.')  # 抽取分城市性别信息（如果群名片有信息）
    parser.add_argument('--signatures', type=bool, default=False,
                        help='Extract signatures of group members (by gender) and save as json.')
                        # 抽取群成员签名信息（分性别）并保存（Json）
    parser.add_argument('--word_cloud', type=bool, default=False,
                        help='Extract signatures of group members (by gender) and parse by words for downstream '
                             'word cloud display.')
                        # 抽取群成员签名信息（分性别），分词，并保存为词云输入文件（指定分隔符），方便后续词云处理
    parser.add_argument('--separator', type=str, default=';', \
                        help='Separator for word cloud art input.') # 词云文件分隔符
    parser.add_argument('--sentiment_analysis', type=bool, default=False,
                        help='Extract signatures of group members (by gender), parse by words, and perform '
                             'sentiment analysis.') # 抽取群成员签名信息（分性别），分词，翻译，进行情感分析
    args, unparsed = parser.parse_known_args()

    if not itchat.search_chatrooms(args.group_name):
        print('ERROR: Chat group [%s] not activated, please check group name, or post a msg in the group. / '
                               '群聊【%s】未激活，请检查群名，或在群中发布一条消息。' %(args.group_name, args.group_name))
    else:
        print('Analyzing / 正在分析群聊 【%s】...' %args.group_name)

        # Extract gender information
        # 抽取性别信息
        if args.run_all or args.gender_info:
            print(get_gender_info(args.group_name))

        # Extract gender information by city if available
        # 抽取分城市性别信息（如果群名片有信息）
        if args.run_all or args.gender_info_by_city:
            print(get_gender_info_by_city(args.group_name))

        # Extract signatures of group members (by gender) and save as json
        # 抽取群成员签名信息（分性别）并保存（Json）
        if args.run_all or args.signatures:
            signature_by_gender = get_signature_by_gender(args.group_name)
            with open('%s_signatures_by_gender.json' %args.group_name, 'w') as outfile:
                json.dump(signature_by_gender, outfile)

        # Extract signatures of group members (by gender) and parse by words for downstream word cloud display
        # Free online word cloud resource: https://wordart.com/create.
        # Use font Noto Sans S Chinese or upload customized font for Chinese display
        # 抽取群成员签名信息（分性别），分词，并保存为词云输入文件（指定分隔符），方便后续词云处理
        # 免费词云生成网站：https://wordart.com/create. 需选择Noto Sans S Chinese字体或自行上传字体来支持中文显示。
        if args.run_all or args.word_cloud:
            signature_by_gender = get_signature_by_gender(args.group_name)
            signature_by_gender_parse = parse_signatures(signature_by_gender, args.separator)
            for grp, sig_words in signature_by_gender_parse.items():
                with open('%s_%s_parsed_signatures.txt' %(args.group_name, grp), 'w') as outfile:
                    outfile.write(sig_words)

        # Extract signatures of group members (by gender), parse by words, and perform sentiment analysis
        # 抽取群成员签名信息（分性别），分词，翻译，进行情感分析
        if args.run_all:
            translator = Translator(service_urls=['translate.google.com'])
            sentiment_analysis(signature_by_gender_parse, translator)
        elif args.sentiment_analysis:
            translator = Translator(service_urls=['translate.google.com'])
            signature_by_gender = get_signature_by_gender(args.group_name)
            signature_by_gender_parse = parse_signatures(signature_by_gender, args.separator)
            sentiment_analysis(signature_by_gender_parse, translator)


