"""
@author: lowinli
指代消解评测代码
"""
import itertools
import numpy as np
from scipy.optimize import linear_sum_assignment


def get_f1(precision, recall):
    """
    Parameters
    ------
        precision       float       准确率
        recall          float       召回率
    Return
    ------
        float       调和平均数
    """
    if precision == 0 and recall == 0:
        return 0
    return precision * recall * 2 / (precision + recall)


def muc(predicted_clusters, gold_clusters):
    """
    the link based MUC

    Parameters
    ------
        predicted_clusters      list(list)       预测实体簇
        gold_clusters           list(list)       标注实体簇
    Return
    ------
        tuple(float)    准确率、召回率、调和平均数
    """
    pred_edges = set()
    for cluster in predicted_clusters:
        pred_edges |= set(itertools.combinations(cluster, 2))
    gold_edges = set()
    for cluster in gold_clusters:
        gold_edges |= set(itertools.combinations(cluster, 2))
    correct_edges = gold_edges & pred_edges
    precision = len(correct_edges) / len(pred_edges)
    recall = len(correct_edges) / len(gold_edges)
    f1 = get_f1(precision, recall)
    return precision, recall, f1


def b_cubed(predicted_clusters, gold_clusters):
    """
    B cubed metric

    Parameters
    ------
        predicted_clusters      list(list)       预测实体簇
        gold_clusters           list(list)       标注实体簇
    Return
    ------
        tuple(float)    准确率、召回率、调和平均数
    """
    mentions = set(sum(predicted_clusters, [])) & set(sum(gold_clusters, []))
    precisions = []
    recalls = []
    for mention in mentions:
        mention2predicted_cluster = [x for x in predicted_clusters if mention in x][0]
        mention2gold_cluster = [x for x in gold_clusters if mention in x][0]
        corrects = set(mention2predicted_cluster) & set(mention2gold_cluster)
        precisions.append(len(corrects) / len(mention2predicted_cluster))
        recalls.append(len(corrects) / len(mention2gold_cluster))
    precision = sum(precisions) / len(precisions)
    recall = sum(recalls) / len(recalls)
    f1 = get_f1(precision, recall)
    return precision, recall, f1


def ceaf(predicted_clusters, gold_clusters):
    """
    the entity based CEAF metric

    Parameters
    ------
        predicted_clusters      list(list)       预测实体簇
        gold_clusters           list(list)       标注实体簇
    Return
    ------
        tuple(float)    准确率、召回率、调和平均数
    """
    scores = np.zeros((len(predicted_clusters), len(gold_clusters)))
    for j in range(len(gold_clusters)):
        for i in range(len(predicted_clusters)):
            scores[i, j] = len(set(predicted_clusters[i]) & set(gold_clusters[j]))
    indexs = linear_sum_assignment(scores, maximize=True)
    max_correct_mentions = sum(
        [scores[indexs[0][i], indexs[1][i]] for i in range(indexs[0].shape[0])]
    )
    precision = max_correct_mentions / len(sum(predicted_clusters, []))
    recall = max_correct_mentions / len(sum(gold_clusters, []))
    f1 = get_f1(precision, recall)
    return precision, recall, f1


def conll_coref_f1(predicted_clusters, gold_clusters):
    """
    
    Parameters
    ------
        predicted_clusters      list(list)       预测实体簇
        gold_clusters           list(list)       标注实体簇
    Return
    ------
        f1    调和平均数
    """
    _, _, f1_m = muc(predicted_clusters, gold_clusters)
    _, _, f1_b = b_cubed(predicted_clusters, gold_clusters)
    _, _, f1_c = ceaf(predicted_clusters, gold_clusters)
    return (f1_m + f1_b + f1_c) / 3
