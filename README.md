# polyhymnia

Polyhymnia (/pɒliˈhɪmniə/; Greek: Πολυύμνια, lit. 'the one of many hymns'), alternatively Polymnia (Πολύμνια) was in Greek mythology the Muse of sacred poetry, sacred hymn, dance, and eloquence as well as agriculture and pantomime.

Polyhymnia name comes from the Greek words "poly" meaning "many" and "hymnos", which means "praise".

将praise理解为增强，那么该项目就是对“诗歌”的增强，即对自然语言数据的增广（我说是就是不接受反驳）。那么，该项目旨在给各位NLP工程师提供一些开箱即用的数据增广办法。

## Survey

- [哈工大｜NLP数据增强方法？我有15种](https://mp.weixin.qq.com/s/YQ9jKtGVN9a7Uzi5zFE0pg)



## Installation

推荐使用本地安装模式。

- 本地安装：

```bash
git clone https://github.com/luoy2/polyhymnia.git
cd polyhymnia
pip install .
```
测试安装：
```bash
~/polyhymnia$ python38 -m unittest tests/test_methods.py -v
[Polyhnmnia] 2021-10-21 11:11:38,266 - DEBUG - execute tasks: 
[Polyhnmnia] 2021-10-21 11:11:38,266 - DEBUG - random_insertion: 3 times
[Polyhnmnia] 2021-10-21 11:11:38,266 - DEBUG - synonym_replacement: 2 times
[Polyhnmnia] 2021-10-21 11:11:38,266 - DEBUG - random_deletion: 2 times
[Polyhnmnia] 2021-10-21 11:11:38,266 - DEBUG - random_swap: 2 times
[Polyhnmnia] 2021-10-21 11:11:38,302 - DEBUG - random_insertion --- 谷物小麦种植
[Polyhnmnia] 2021-10-21 11:11:38,341 - DEBUG - synonym_replacement --- 玉米栽植
[Polyhnmnia] 2021-10-21 11:11:38,341 - DEBUG - random_deletion --- 小麦种植
[Polyhnmnia] 2021-10-21 11:11:38,341 - DEBUG - random_swap --- 种植小麦
[Polyhnmnia] 2021-10-21 11:11:38,341 - DEBUG - random_swap --- 种植小麦
[Polyhnmnia] 2021-10-21 11:11:38,341 - DEBUG - random_deletion --- 小麦种植
[Polyhnmnia] 2021-10-21 11:11:38,342 - DEBUG - synonym_replacement --- 小麦甘蔗
[Polyhnmnia] 2021-10-21 11:11:38,342 - DEBUG - random_insertion --- 棉花小麦种植
[Polyhnmnia] 2021-10-21 11:11:38,342 - DEBUG - random_insertion --- 农作物小麦种植
['种植小麦', '小麦种植', '谷物小麦种植', '小麦种植', '种植小麦', '农作物小麦种植', '小麦甘蔗', '棉花小
ok
test_reverse_translate (tests.test_methods.TestMethods) ... 请使用 ReverseTranslate.set_creds(appid, 
ok
test_simbert (tests.test_methods.TestMethods) ... 2021-10-21 11:11:38.407926: I tensorflow/stream_exebcudart.so.11.0
['身份证丢了，怎么办',
 '身份证丢了怎么办?',
 '身份证丢了怎么办啊',
 '身份证丢了怎么办？',
 '身份证丢了怎么办！',
 '身份证丢失怎么办？',
 '身份证丢了该怎么办',
 '身份证丢失，怎么办？']
ok

----------------------------------------------------------------------
Ran 4 tests in 11.913s
```


## Usage

- **simbert 数据生成** 

  使用simbert_v2 ([SimBERTv2来了！融合检索和生成的RoFormer-Sim模型](https://spaces.ac.cn/archives/8454)) 进行相似句生成。

  ```python
  from polyhymnia import Simbert
  Simbert.gen("身份证丢了怎么办", 8)
  
  Out[38]: 
  ['身份证丢了怎么办?',
   '身份证丢了怎么办？',
   '身份证丢了怎么办。',
   '身份证丢失了怎么办',
   '身份证丢失了怎么办？',
   '身份证丢了咋办？',
   '身份证丢失怎么办？',
   '身份证丢失怎么办！']
  
  ```

  默认会使用GPU进行生成，如果想使用CPU，请自行在**引用包之前**设置CUDA_VISIBLE_DEVICES 环境变量:

  ```python
  import os
  os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
  from polyhymnia import Simbert
  ```

  

- **reverse_translate 多链翻译**

  使用之前请先于https://api.fanyi.baidu.com/product/11 申请翻译`api appid`和`appsecret`

  ```python
  from polyhymnia import ReverseTranslate
  
  In [3]: ReverseTranslate.set_creds(appid, appSecret)
  In [4]: ReverseTranslate.gen("小麦种植", 4)   
  [Polyhnmnia] 2021-10-20 18:05:04,331 - DEBUG - start translate for: 小麦种植
  [Polyhnmnia] 2021-10-20 18:05:05,744 - DEBUG - zh -> hu -> spa -> zh: 小麦栽培
  [Polyhnmnia] 2021-10-20 18:05:07,481 - DEBUG - zh -> dan -> rom -> zh: 小麦种植；
  [Polyhnmnia] 2021-10-20 18:05:08,424 - DEBUG - zh -> bul -> zh: 小麦作物
  [Polyhnmnia] 2021-10-20 18:05:09,301 - DEBUG - zh -> en -> zh: 小麦种植
  Out[4]: ['小麦种植', '小麦作物', '小麦种植；', '小麦栽培']
  
  ```
  
- [EDA: Easy Data Augmentation Techniques for Boosting Performance on Text Classification Tasks](https://arxiv.org/abs/1901.11196)

  在此进行了一些改进，使用sobol随机序列生成随机任务顺序，保证任务随机性

  ```python
  In [1]: from polyhymnia import EDA    
  
  In [2]: EDA.gen("小麦种植", 8)                
  
  [Polyhnmnia] 2021-10-20 18:10:24,632 - DEBUG - execute tasks: 
  [Polyhnmnia] 2021-10-20 18:10:24,632 - DEBUG - random_insertion: 3 times
  [Polyhnmnia] 2021-10-20 18:10:24,632 - DEBUG - synonym_replacement: 2 times
  [Polyhnmnia] 2021-10-20 18:10:24,632 - DEBUG - random_deletion: 2 times
  [Polyhnmnia] 2021-10-20 18:10:24,632 - DEBUG - random_swap: 2 times
  [Polyhnmnia] 2021-10-20 18:10:24,673 - DEBUG - random_insertion --- 玉米小麦种植
  [Polyhnmnia] 2021-10-20 18:10:24,717 - DEBUG - synonym_replacement --- 甜菜作物
  [Polyhnmnia] 2021-10-20 18:10:24,718 - DEBUG - random_deletion --- 小麦种植
  [Polyhnmnia] 2021-10-20 18:10:24,718 - DEBUG - random_swap --- 种植小麦
  [Polyhnmnia] 2021-10-20 18:10:24,718 - DEBUG - random_swap --- 种植小麦
  [Polyhnmnia] 2021-10-20 18:10:24,718 - DEBUG - random_deletion --- 小麦种植
  [Polyhnmnia] 2021-10-20 18:10:24,718 - DEBUG - synonym_replacement --- 大豆栽植
  [Polyhnmnia] 2021-10-20 18:10:24,718 - DEBUG - random_insertion --- 马铃薯小麦种植
  [Polyhnmnia] 2021-10-20 18:10:24,718 - DEBUG - random_insertion --- 种植小麦种植
          
  Out[2]: ['种植小麦', '小麦种植', '种植小麦种植', '玉米小麦种植', '小麦种植', '种植小麦', '甜
  菜作物', '大豆栽植', '马铃薯小麦种植']
  
  ```

  高级api `polyhymnia.methods.noising.stacking.eda.gen`

  - `alpha_sr` 同义词替换概率, 默认为0.1

  - `alpha_ri` 随机插入概率, 默认为0.1

  - `alpha_rs` 随机替换词顺序概率，默认为0.1

  - `p_rd` 随机删除概率，默认为0.1

  使用者可以使用高级api进行任务组合，如：

  ```python
  from polyhymnia.methods.noising.stacking.eda import gen
  contents = '小麦种植'
  print(gen(contents, num_aug=8, p_rd=0, alpha_ri=0))
  ```

  ```
  [Polyhnmnia] 2021-10-20 18:15:03,438 - DEBUG - execute tasks: 
  [Polyhnmnia] 2021-10-20 18:15:03,438 - DEBUG - synonym_replacement: 4 times
  [Polyhnmnia] 2021-10-20 18:15:03,438 - DEBUG - random_swap: 4 times
  [Polyhnmnia] 2021-10-20 18:15:03,438 - DEBUG - synonym_replacement --- 小麦耕种
  [Polyhnmnia] 2021-10-20 18:15:03,438 - DEBUG - synonym_replacement --- 小麦栽植
  [Polyhnmnia] 2021-10-20 18:15:03,438 - DEBUG - random_swap --- 种植小麦
  [Polyhnmnia] 2021-10-20 18:15:03,439 - DEBUG - random_swap --- 种植小麦
  [Polyhnmnia] 2021-10-20 18:15:03,439 - DEBUG - synonym_replacement --- 小麦种植
  [Polyhnmnia] 2021-10-20 18:15:03,439 - DEBUG - synonym_replacement --- 谷物种植
  [Polyhnmnia] 2021-10-20 18:15:03,439 - DEBUG - random_swap --- 种植小麦
  [Polyhnmnia] 2021-10-20 18:15:03,439 - DEBUG - random_swap --- 种植小麦
  
  Out[6]: ['种植小麦', '小麦耕种', '种植小麦', '小麦栽植', '谷物种植', '小麦种植', '种植小麦', '种植小
  麦']
  ```

  可以发现的是，当设置某些概率为0时，基于**sobol序列**的特性，EDA会均匀分配概率非0的任务进行数据增强组合。

  Ref:
  - [Sobol序列](https://en.wikipedia.org/wiki/Sobol_sequence)
  - [低差异序列](https://zhuanlan.zhihu.com/p/20197323)
  

- [AEDA: An Easier Data Augmentation Technique for Text Classification](https://arxiv.org/abs/2108.13230)

  ```python
  In [6]: from polyhymnia import AEDA   
  In [7]: AEDA.gen("身份证丢了怎么办", 4)       
  Out[7]: ['身份证丢了怎么,办', '身份证丢了怎么办。', '身 份证丢了怎么办', '身份证丢了怎么办']
  ```

    高级api `polyhymnia.methods.noising.insertion.aeda_text`

    - `fraction` 插入标点符号数量比例，默认为1/3
    
    - `puncs` 插入标点符号列表，默认为`[",", "。", "，", "\t", " "]`
  
    
  



## Logging

- 使用`polyhymnia._logger.LoggingFactory`进行模块日志配置, 使用`polyhymnia.set_verbose`来进行快速切换日志等级。

  ```python
  In [1]: import polyhymnia                               
  In [2]: polyhymnia.ReverseTranslate.set_creds(appid, appsecret)              
  In [3]: polyhymnia.ReverseTranslate.gen("你是狗吗", 3)                                             
  Out[3]: ['你是狗吗？', '你是一只狗。']
  # 此时没有日志信息
      
  In [4]: import polyhymnia                                 
  In [5]: polyhymnia.set_verbose(True)                                               
  In [6]: ReverseTranslate.gen("你是狗吗", 3)                                                  
  [Polyhnmnia] 2021-10-21 08:21:05,464 - DEBUG - start translate for: 你是狗吗
  [Polyhnmnia] 2021-10-21 08:21:06,668 - DEBUG - zh -> el -> en -> zh: 你是一只狗。
  [Polyhnmnia] 2021-10-21 08:21:08,065 - DEBUG - zh -> cs -> ara -> zh: 你是狗吗？
  [Polyhnmnia] 2021-10-21 08:21:09,438 - DEBUG - zh -> est -> pt -> zh: 你是狗吗？
  [Polyhnmnia] 2021-10-21 08:21:10,775 - DEBUG - zh -> bul -> ru -> zh: 你是狗吗？
  [Polyhnmnia] 2021-10-21 08:21:11,693 - DEBUG - zh -> en -> zh: 你是狗吗
  Out[6]: ['你是狗吗', '你是狗吗？', '你是一只狗。']
  ```
  





## 鸣谢

- [bert4keras](https://github.com/bojone/bert4keras)
- [RoFormer-Sim: Integrating Retrieval and Generation into RoFormer](https://github.com/ZhuiyiTechnology/roformer-sim)
- [chatopera/Synonyms: 中文近义词：聊天机器人，智能问答工具包](https://github.com/chatopera/Synonyms)

- [fxsjy/jieba: 结巴中文分词](https://github.com/fxsjy/jieba)
- [tsroten/zhon: Constants used in Chinese text processing](https://github.com/tsroten/zhon)
- [easy to use retry decorator in python - GitHub](https://github.com/invl/retry)
- [SciPy library main repository - GitHub](https://github.com/scipy/scipy)
- [tensorflow/tensorflow: An Open Source Machine ... - GitHub](https://github.com/tensorflow/tensorflow)
- [psf/requests: A simple, yet elegant, HTTP library. - GitHub](https://github.com/psf/requests)
- [GitHub - zhanlaoban/EDA_NLP_for_Chinese](https://github.com/zhanlaoban/EDA_NLP_for_Chinese)
- [通用翻译API - 百度翻译开放平台](https://api.fanyi.baidu.com/product/11)
