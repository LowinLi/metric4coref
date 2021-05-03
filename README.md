# metric4coref
![](https://github.com/LowinLi/metric4coref/actions/workflows/python-package.yml/badge.svg)
[![codecov](https://codecov.io/gh/LowinLi/metric4coref/branch/main/graph/badge.svg?token=LPM96OTSLY)](https://codecov.io/gh/LowinLi/metric4coref)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/metric4coref.svg)](https://pypi.org/project/metric4coref/)
[![PyPI](https://img.shields.io/pypi/v/metric4coref.svg)](https://pypi.org/project/metric4coref/)
![](https://img.shields.io/badge/language-python-green)
![](https://img.shields.io/badge/style-black-black)
![](https://img.shields.io/badge/license-MIT-orange)
[![Downloads](https://pepy.tech/badge/metric4coref)](https://pepy.tech/project/metric4coref)

共指消解任务CoNLL的[官方评测库](https://github.com/conll/reference-coreference-scorers)是**Perl**语言完成的，但是近些年基于**Python**语言为主的深度学习在共指消解任务上的应用越来越普遍，所以同时也非常需要一个基于**Python**的便捷评测库。

### 使用方法
+ 安装
```bash
pip install metric4coref
```
+ 使用
```python
from metric4coref import muc, ceaf, b_cubed, conll_coref_f1
# "a", "b" 等代表mention id
# predict_clusters、gold_clusters分别代表模型生成mention簇和标注mention簇
predict_clusters = [["a", "b", "c"], ["d", "e", "f", "g"], ["h", "i", "j"], ["k"]]
gold_clusters = [["a", "b", "d"], ["c", "e", "f", "g"], ["h", "i", "j", "k"]]

print(muc(predict_clusters, gold_clusters))
# -> 准确率、召回率、f1：(0.5833333333333334, 0.4666666666666667, 0.5185185185185186)
print(b_cubed(predict_clusters, gold_clusters))
# -> 准确率、召回率、f1：(0.7424242424242423, 0.606060606060606, 0.6673476336397685)
print(ceaf(predict_clusters, gold_clusters))
# -> 准确率、召回率、f1：(0.7272727272727273, 0.7272727272727273, 0.7272727272727273)
print(conll_coref_f1(predict_clusters, gold_clusters))
# -> 以上三个f1平均值： 0.6377129598103382
```

### 共指消解的评测方法

- [x] the link based MUC
    - [论文](https://www.aclweb.org/anthology/M95-1005.pdf)
    - 1995
- [x] B cubed metric
    - [论文](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.47.5848&rep=rep1&type=pdf)
    - 1998
- [x] the entity based CEAF metric
    - [论文](https://www.aclweb.org/anthology/H05-1004.pdf)
    - 2005
- [ ] BLANC
- [ ] Link-Based Entity-Aware metric (LEA).

### 共指消解任务
+ 任务主页
[CoNLL 2012 Co-reference task](https://cemantix.org/conll/2012/introduction.html)
+ [官方metric](https://github.com/conll/reference-coreference-scorers)
    + Average F1 of MUC, B-cubed, and CEAF

### 算法解读

- the link based MUC
    - 解释：基于簇中两两mention连接的边作为评测依据
        - precision：
            分子：所有系统预测边与所有标注边的交集的个数
            分母：所有预测边的个数
        - recall：
            分子：所有系统预测边与所有标注边的交集的个数
            分母：所有标注边的个数
        - f1:
            precision * recall * 2 / (precision + recall)
    - 例子：
        - 预测边：
        ab、bc、ac、de、df、dg、ef、eg、fg、hi、ij、hj共12个
        - 标注边：
        ab、ad、bd、ce、cf、cg、ef、eg、fg、hi、hj、hk、ij、ik、jk共15个
        - 预测边和标注边的交集：
        ab、ef、eg、fg、hi、hj、ij共7个
        - precision: 7/12=0.5833333
        - recall: 7/15=0.4666667
        - f1: 0.5833333 * 0.4666667 * 2 / (0.5833333 + 0.4666667)=0.5185185
    - 特点：
        - 不考虑单个mention的簇，因为没有边
        - 倾向于生成很多mention的簇，容易得高分
- B cubed metric
    - 解释：以mention为单位，每个mention计算一个precision和recall，在加权平均所有mention的precision和recall
        - 每个mention的计算方法：
            - precision：
                分子：系统预测的包含mention的簇与人工标注的包含mention的簇的mention交集个数
                分母：系统生成的包含mention的簇的个数
            - recall：
                分子：系统预测的包含mention的簇与人工标注的包含mention的簇的mention交集个数
                分母：人工标注的包含mention的簇的个数
            - f1:
                precision * recall * 2 / (precision + recall)
    - 例子：
        - mention a:
            所在预测簇: ["a", "b", "c"]
            所在标注簇: ["a", "b", "d"]
            precision:
                分子: a、b共2个
                分母: a、b、c共3个
                =2/3=0.666
            recall:
                分子: a、b共2个
                分母: a、b、d共3个
                =2/3=0.666
        - mention b:
            所在预测簇: ["a", "b", "c"]
            所在标注簇: ["a", "b", "d"]
            precision:
                分子: a、b共2个
                分母: a、b、c共3个
                =2/3=0.666
            recall:
                分子: a、b共2个
                分母: a、b、d共3个
                =2/3=0.666
        - mention c
            所在预测簇: ["a", "b", "c"]
            所在标注簇: ["c", "e", "f", "g"]
            precision:
                分子: c共1个
                分母: a、b、c共3个
                =1/3=0.333
            recall:
                分子: c共1个
                分母: c、e、f、g共4个
                =1/4=0.25
        ...
        - 对所有mention的precision、recall求平均值
    - 特点：
        - 对每个mention等权重看待
- the entity based CEAF metric
    - 解释：
        1. 标注的实体簇为R、系统生成的实体簇为S,R中每个mention为r、S中每个mention为s
        2. R的个数与S的个数的少者为m
        3. 建立从R到S的一一映射map，每个映射对应从R中的r到S中的s，映射的个数为m
        4. 计算每个映射中，r和s中相同mention个数
        5. 计算整个map映射中，所有相同mention的个数
        6. 遍历所有可能的map，取所有相同mention的个数的最大的映射map，相同mention个数为n
        7. precision = n/S的mention个数
        8. recall = n/R的mention个数
    - 例子：
        - 预测的实体簇个数为4
        - 标注的实体簇个数为3
            那么m=3
        - 遍历可知，映射关系为
            标注实体簇1 --> 预测实体簇1
            标注实体簇2 --> 预测实体簇2
            标注实体簇3 --> 预测实体簇3
        - 计数：
            正确的mention有：
                a、b、e、f、g、h、i、j共8个
            预测的mention个数共11个
            标注的mention个数共11个
        - 指标：
            precision=8/11=0.7272727
            recall=8/11=0.7272727
