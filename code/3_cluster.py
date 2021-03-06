#-*- coding:utf-8 -*-
import os, csv
import numpy as np
import scipy.cluster.hierarchy as sch

from variables import APPS
from variables import DISTANCE_BASE_PATH, DUPLICATES_REPORT_PATH
from variables import CORPUS_PATH
from variables import T_THRESHOLD

from util_corpus import get_all_reports_id

# ---------------------------------------------------------------------------------------
# Description   : Function to aggregate the reports into groups
# ---------------------------------------------------------------------------------------

def cluster(app):
	all_reports_id = get_all_reports_id(app)
	distance_matrix = np.load('/'.join([DISTANCE_BASE_PATH, app, 'distance_txt.npy']))
	distArray = distance_matrix[np.triu_indices(len(distance_matrix), 1)] # 返回上三角，不包括对角线

	Z = sch.linkage(distArray, method = 'single')  # Perform hierarchical/agglomerative clustering. Single distance
	clusters = sch.fcluster(Z, T_THRESHOLD, criterion = 'distance') # # Form flat clusters from the hierarchical clustering defined by the given linkage matrix.
	# The cophenetic distance between two objects is the height of the dendrogram where the two branches that include the two objects merge into a single branch. 
	# Forms flat clusters so that the original observations in each flat cluster have no greater a cophenetic distance than t.
	# print(type(Z)) #<class 'numpy.ndarray'>
	# print(type(clusters))#<class 'numpy.ndarray'>
	# print(Z.shape) # (999, 4)
	# print(clusters.shape) # (1000,) ?
	# print(type(clusters[0])) # <class 'numpy.int32'>
	duplicate_set = {} # 这个名字其实取得不太恰当
	for i, cluster_id in enumerate(clusters): # 这就是clusters的内容
		report_id = all_reports_id[i]
		if cluster_id not in duplicate_set.keys():
			duplicate_set[cluster_id] = [report_id]
		else:
			duplicate_set[cluster_id].append(report_id)
	# print(len(duplicate_set)) # 955 效果不是很好？
	# yuheng add---------------------------------------------------------------------
	for key in duplicate_set:
		if len(duplicate_set[key]) > 1:
			ds = duplicate_set[key]
			for num in ds:
				repo_file = open('/'.join([CORPUS_PATH, app +"original", num]) + ".txt", "r")
				repo_con = repo_file.read()
				print(repo_con)
				repo_file.close()
				print("---")
			print(f"============ end of one review of {app}")

	# yuheng add---------------------------------------------------------------------
	if not os.path.exists('/'.join([DUPLICATES_REPORT_PATH, app])):
		os.makedirs('/'.join([DUPLICATES_REPORT_PATH, app]))

	# save duplicate_set
	out = open('/'.join([DUPLICATES_REPORT_PATH, app, 'duplicate_set.csv']), 'w+')
	writer = csv.writer(out)
	for k in duplicate_set.keys():
		records = duplicate_set[k]
		writer.writerow(records)
	out.close()

for app in APPS:
	cluster(app)
