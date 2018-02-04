# -*- coding: utf-8 -*-
#Author: Chunyang Chen
#Goal: check the results of the UI2code 

import os
import subprocess

def checkResults(inputFile):
	accuracy_list = []
	with open(inputFile) as f:
		with open('.tmp.gold.txt', 'w') as fw_gold, open('.tmp.pred.txt', 'w') as fw_pred:
			for line in f:
				items = line.strip().split("\t")
				if len(items) == 5:
					#check the exact match
					if items[1] == items[2]:
						accuracy_list.append(1)
					else:
						accuracy_list.append(0)					
					#check the BLEU score
					fw_gold.write(items[1]+"\n")
					fw_pred.write(items[2]+"\n")
					
	print "Among %s testing cases, %s (%s) are totally correct" % (len(accuracy_list), accuracy_list.count(1), float(accuracy_list.count(1))/len(accuracy_list))
	metric = subprocess.check_output('perl multi-bleu.perl %s < %s'%('.tmp.gold.txt', '.tmp.pred.txt'), shell=True)									
	print metric.split(", ")[0].split("= ")[1]
	

if __name__ == '__main__':
	
	f_rawResult = "results/results.txt"
	
	
	try:
		checkResults(f_rawResult)
		
	except Exception, e:
		print e
		raise	