# 微信群分城市分性别信息统计，群成员签名词云与情感分析/WeChat Group Info Extraction and Analysis

**NOTE: This pkg might violate PC**

## Table of Contents

* [简介\/Intro](#简介-\/-Intro)
* [配置\/Dependencies](#配置-/-Dependencies)
* [本地运行\/Run instructions](#本地运行-/-Run-instructions)
  * [创建环境\/Environment](#创建环境\/Environment)
  * [运行代码\/Run](#运行代码-/-Run)
  * [运行举例\/Examples](#运行举例-/-Examples)
* [结果展示\/Results showcase](#结果展示-/-Results-showcase)


## 简介 / Intro
嘛，最开始是在一个相亲群做的分析，所以可以统计群里性别比，和分城市人数、性别差异。

通过分性别签名词云可以看出男女思维差异。

情感分析也可以起到类似的作用。但可能由于分词不完善，以及仅使用了英文情感分析资源，当前没有得到特别有效的信息。

Analyze gender distribution (overall / by city) in target WeChat group.

Generate word cloud art and perform sentiment analysis on signatures of group members by gender

Both word cloud and sentiment analysis could be adopted to analyze the difference between males and females.
However, the coarse parsing might have compromised the power of sentiment analysis here.

## 配置 / Dependencies

使用[itchat](https://itchat.readthedocs.io/zh/latest/)作为个人微信API

`itchat==1.3.10`

其它dependencies请见文件[`environment.yml`](https://github.com/OXPHOS/WeChatAnalysis/blob/master/environment.yml)

See other dependencies in [`environment.yml`](https://github.com/OXPHOS/WeChatAnalysis/blob/master/environment.yml)


## 本地运行 / Run instructions
### 创建环境 / Environment
在conda环境下，创建环境：

```conda env create -f environment.yml```

`environment.yml`文件的第一行为环境名称，激活环境：

Find the env name at the first row of file `environment.yml`, and activate the env:

```source activate myenv```

### 运行代码 / Run
不同功能列表如下：

| 参数 | 含义 | 是否必须     | 缺省值  | 备注    | 
|-------|----------|-------------|------------|---------|
| group_name | 群名 | 是 |   |     | 
| run_all  | 运行以下全部功能 | 否 | False |   | 
| gender_info | 抽取性别信息 | 否 | False|    | 
| gender_info_by_city   |抽取分城市性别信息 |否  | False | 必须保证群名片中包含地点信息，且大多数人有标准群名片  | 
| signatures  | 抽取群成员签名信息（分性别）并保存（Json）  | 否  | False  |  | 
| word_cloud   | 抽取群成员签名信息（分性别），分词，并保存为词云输入文件（指定分隔符），方便后续词云处理 | 否  | False | | 
| separator   | 词云文件分隔符 | 否 | ; |  | 
| sentiment_analysis  | 抽取群成员签名信息（分性别），分词，翻译，进行情感分析 | 否  | False | 使用谷歌翻译，可能需要翻墙 | 

See detailed instructions on params in [this](https://github.com/OXPHOS/WeChatAnalysis/blob/master/wechat_group_analysis.py#L204) file.

### 运行举例 / Examples
1. 仅进行性别信息分析 / Gender statistics only：

`python wechat_group_analysis.py group_name 群名 --gender_info True`

2. 进行性别分析，词云生成 / Gender statistics + word cloud：

`python wechat_group_analysis.py group_name 群名 --gender_info True --word_cloud True`

3. 进行性别分析，词云生成，并使用`Tab`作为词云文件分隔符  / 
Gender statistics + word cloud, use `\Tab` as separator for word cloud art input file：

`python wechat_group_analysis.py group_name 群名 --gender_info True --word_cloud True --separator \t`

## 结果展示 / Results showcase
- 分城市人数性别统计 / Gender statistics by city

![gender_by_city](https://github.com/OXPHOS/WeChatAnalysis/blob/master/example_output/Group_gender_ratio_by_city.png)

- 词云示例 / Word cloud example

([免费词云生成网站](https://wordart.com/create)。 需选择Noto Sans S Chinese字体或自行上传字体来支持中文显示。)

([Note](https://wordart.com/create): 
Use font Noto Sans S Chinese or upload customized font for Chinese display)

![Word Cloud Male](https://github.com/OXPHOS/WeChatAnalysis/blob/master/example_output/word_cloud_m.png)
![Word Cloud Female](https://github.com/OXPHOS/WeChatAnalysis/blob/master/example_output/word_cloud_f.png)


