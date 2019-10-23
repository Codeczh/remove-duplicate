# USAGE
# python search.py --dataset images --shelve db.shelve --query images/84eba74d-38ae-4bf6-b8bd-79ffa1dad23a.jpg

# import the necessary packages
from PIL import Image
import argparse
import random
import shutil
import shelve
import glob2
import uuid
import os
import sys
from index import remove_sameclass
import imagehash
import distance

dataset = os.getcwd()[:os.getcwd().rfind('\\')]+r'\web-bird\train_delete'
root = dataset[:dataset.rfind('\\')]

def fmv_repeat(src,dest): #dataset,root
	if os.path.exists(dest + '\\' + 'repeat\\'):
		shutil.rmtree(dest + '\\' + 'repeat')

	if os.path.exists(src + '\\' + 'repeat'):
		shutil.copytree(src + '\\' + 'repeat', dest + '\\' + 'repeat\\')
		shutil.rmtree(src + '\\' + 'repeat')
	print('copy interclass repeat over')
def fmv_subrepeat(src,dest):
	if os.path.exists(dest + '\\' + 'repeat_sub\\'):
		shutil.rmtree(dest + '\\' + 'repeat_sub\\')
	os.mkdir(dest + '\\' + 'repeat_sub\\')
	for path in glob2.iglob(src+'/*/repeat'):
		if os.path.exists(dest + '\\' + 'repeat_sub\\'+path.split('\\')[-2]):
			shutil.rmtree(dest + '\\' + 'repeat_sub\\'+path.split('\\')[-2])
		shutil.copytree(path, dest + '\\' + 'repeat_sub\\'+path.split('\\')[-2])
		shutil.rmtree(path, dest + '\\' + 'repeat_sub\\' + path.split('\\')[-2])
		sys.stdout.write('\rcopy subclass {}'.format(path.split('\\')[-2]))
		sys.stdout.flush()
	print('\r  copy subclass repeat over')
fmv_subrepeat(dataset,root)
