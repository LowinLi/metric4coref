import itertools
import numpy as np
from scipy.optimize import linear_sum_assignment


def get_f1(precision, recall):
    return precision * recall * 2 / (precision + recall)


def muc(predicted_clusters, gold_clusters):
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
    predicted_clusters = predicted_clusters
    gold_clusters = gold_clusters
    scores = np.zeros((len(predicted_clusters), len(gold_clusters)))
    for i in range(len(gold_clusters)):
        for j in range(len(predicted_clusters)):
            scores[i, j] = len(set(predicted_clusters[i]) & set(gold_clusters[j]))
    indexs = linear_sum_assignment(scores, maximize=True)
    max_correct_mentions = sum(
        [scores[indexs[0][i], indexs[1][i]] for i in range(indexs[0].shape[0])]
    )
    precision = max_correct_mentions / len(sum(predicted_clusters, []))
    recall = max_correct_mentions / len(sum(gold_clusters, []))
    f1 = get_f1(precision, recall)
    return precision, recall, f1