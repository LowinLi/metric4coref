"""
@author: lowinli
单元测试

以下a、b、c等表示mention
["a", "b", "c"]等表示这些mention归为一个实体的簇
predict_clusters 表示系统预测簇
gold_clusters 表示标注簇
"""
import unittest
from src import get_f1, muc, ceaf, b_cubed

predict_clusters = [["a", "b", "c"], ["d", "e", "f", "g"], ["h", "i", "j"], ["k"]]
gold_clusters = [["a", "b", "d"], ["c", "e", "f", "g"], ["h", "i", "j", "k"]]


class Tests(unittest.TestCase):
    def test_f1(self):
        self.assertAlmostEqual(get_f1(0.8, 0.9), 0.8470588)

    def test_muc(self):
        '''
            论文：https://www.aclweb.org/anthology/M95-1005.pdf
            发布：1995
            解释：基于簇中两两mention连接的边作为评测依据
                precision：
                    分子：所有系统预测边与所有标注边的交集的个数
                    分母：所有预测边的个数
                recall：
                    分子：所有系统预测边与所有标注边的交集的个数
                    分母：所有标注边的个数
                f1:
                    precision * recall * 2 / (precision + recall)
            例子：
                预测边：ab、bc、ac、de、df、dg、ef、eg、fg、hi、ij、hj共12个
                标注边：ab、ad、bd、ce、cf、cg、ef、eg、fg、hi、hj、hk、ij、ik、jk共15个
                预测边和标注边的交集：ab、ef、eg、fg、hi、hj、ij共7个
                precision: 7/12=0.5833333
                recall: 7/15=0.4666667
                f1: 0.5833333 * 0.4666667 * 2 / (0.5833333 + 0.4666667)=0.5185185
            特点：
                不考虑单个mention的簇，因为没有边
                倾向于生成很多mention的簇，容易得高分
        '''
        p, r, f1 = muc(predict_clusters, gold_clusters)
        self.assertAlmostEqual(p, 0.5833333)
        self.assertAlmostEqual(r, 0.4666667)
        self.assertAlmostEqual(f1, 0.5185185)

    def test_b_cubed(self):
        '''
            论文：https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.47.5848&rep=rep1&type=pdf
            发布：1998
            解释：以mention为单位，每个mention计算一个precision和recall，在加权平均所有mention的precision和recall
                每个mention的计算方法：
                    precision：
                        分子：系统预测的包含mention的簇与人工标注的包含mention的簇的mention交集个数
                        分母：系统生成的包含mention的簇的个数
                    recall：
                        分子：系统预测的包含mention的簇与人工标注的包含mention的簇的mention交集个数
                        分母：人工标注的包含mention的簇的个数
                    f1:
                        precision * recall * 2 / (precision + recall)
            例子：
                mention a:
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
                mention b:
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
                mention c
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
                    
                对所有mention的precision、recall求平均值
            特点：
                对每个mention等权重看待
        '''
        p, r, f1 = b_cubed(predict_clusters, gold_clusters)
        self.assertAlmostEqual(p, 0.7424242)
        self.assertAlmostEqual(r, 0.6060606)
        self.assertAlmostEqual(f1, 0.6673476)

    def test_ceaf(self):
        '''
            论文：https://www.aclweb.org/anthology/H05-1004.pdf
            发布：2005
            解释：
                1. 标注的实体簇为R、系统生成的实体簇为S,R中每个mention为r、S中每个mention为s
                2. R的个数与S的个数的少者为m
                3. 建立从R到S的一一映射map，每个映射对应从R中的r到S中的s，映射的个数为m
                4. 计算每个映射中，r和s中相同mention个数
                5. 计算整个map映射中，所有相同mention的个数
                6. 遍历所有可能的map，取所有相同mention的个数的最大的映射map，相同mention个数为n
                7. precision = n/S的mention个数
                8. recall = n/R的mention个数
            例子：
                预测的实体簇个数为4
                标注的实体簇个数为3
                那么m=3
                遍历可知，映射关系为
                    标注实体簇1 --> 预测实体簇1
                    标注实体簇2 --> 预测实体簇2
                    标注实体簇3 --> 预测实体簇3
                计数：
                    正确的mention有：
                        a、b、e、f、g、h、i、j共8个
                    预测的mention个数共11个
                    标注的mention个数共11个
                指标：
                    precision=8/11=0.7272727
                    recall=8/11=0.7272727
        '''
        p, r, f1 = ceaf(predict_clusters, gold_clusters)
        self.assertAlmostEqual(p, 0.7272727)
        self.assertAlmostEqual(r, 0.7272727)
        self.assertAlmostEqual(f1, 0.7272727)
