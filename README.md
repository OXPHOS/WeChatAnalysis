
-[中文](#微信群分城市分性别信息统计，群成员签名词云与情感分析)
-[English](#WeChat Group Info Extraction and Analysis)

## 微信群分城市分性别信息统计，群成员签名词云与情感分析
### 简介
嘛，最开始是在一个相亲群做的分析，所以可以统计群里性别比，和分城市人数、性别差异。

通过分性别签名词云可以看出男女思维差异。

情感分析也可以起到类似的作用。但可能由于分词不完善，以及仅使用了英文情感分析资源，当前没有得到特别有效的信息。

### 配置

使用[itchat](https://itchat.readthedocs.io/zh/latest/)作为个人微信API`itchat==1.3.10`
其它dependencies请见文件[`environment.yml`]()

### 本地运行
#### 创建环境
在conda环境下，创建环境：
```conda env create -f environment.yml```
`environment.yml`文件的第一行为环境名称，激活环境：
```source activate myenv```

#### 运行代码
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

运行举例
1. 仅进行性别信息分析：
`python wechat_group_analysis.py --group_name 群名 --gender_info True`

2. 进行性别分析，词云生成：
`python wechat_group_analysis.py --group_name 群名 --gender_info True --word_cloud True`

3. 进行性别分析，词云生成，并使用`Tab`作为词云文件分隔符：
`python wechat_group_analysis.py --group_name 群名 --gender_info True --word_cloud True --separator \t`

#### 结果展示
- 分城市人数性别统计

- 词云示例

## WeChat Group Info Extraction and Analysis
**Analyze gender distribution (overall / by city) in target WeChat group.**

**Generate word cloud art and perform sentiment analysis on signatures of group members by gender**
