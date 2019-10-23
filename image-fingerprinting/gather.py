# USAGE
# python gather.py --input 101_ObjectCategories --output images --csv output.csv

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
import time
from index import remove_sameclass
import imagehash
import distance
from PIL import ImageFile # Python：IOError: image file is truncated 的解决办法
ImageFile.LOAD_TRUNCATED_IMAGES = True



# construct the argument parse and parse the arguments
time0 = time.time()
print(os.getcwd())
if os.path.exists(os.getcwd()+'\\'+'db'):
	shutil.rmtree(os.getcwd()+'\\'+'db')
os.mkdir(os.getcwd()+'\\'+'db')
trainset = os.getcwd()[:os.getcwd().rfind('\\')]+r'\web-bird\train'

def copy_data(src,dest):
	# -------copy train data------
	time1=time.time()
	print('copying train data...')
	if os.path.exists(dest):
		shutil.rmtree(dest)
	shutil.copytree(src, dest)
	print('copy to '+dest+' over, time: %.1f min'%((time.time()-time1)/60))
	print('------------------------------------------------------------------------------------')
# copy data
# dataset = trainset[:trainset.rfind('\\')+1]+'train_delete'
# copy_data(trainset,dataset)
# or not copy
dataset =trainset

if os.path.exists(dataset + '\\' + 'repeat'):
	shutil.rmtree(dataset + '\\' + 'repeat')
time2= time.time()
classname = os.listdir(dataset)
print(classname)
for class_id in classname:
	remove_sameclass(dataset,class_id)
	sys.stdout.write('\r delete subclass {}'.format(class_id[:3]))
	sys.stdout.flush()
print('\r-----------------------------process intra subclass over-------------------------------time:%.1f min'%((time.time()-time2)/60))
# loop over the input images
if os.path.exists(os.getcwd()+'\\'+'all_db.db'):
	os.remove(os.getcwd()+'\\'+'all_db.db')

all_db_path = os.getcwd()+'\\'+'all_db.db'
if os.path.exists(all_db_path + '.bak'):
	os.remove(all_db_path + '.bak')
	print('delete all_db.db.bak   ', end=' ')
if os.path.exists(all_db_path + '.dat'):
	os.remove(all_db_path + '.dat')
	print('delete all_db.db.dat   ', end=' ')
if os.path.exists(all_db_path + '.dir'):
	os.remove(all_db_path + '.dir')
	print('delete all_db.db.dir   ')
all_db = shelve.open(os.getcwd()+'\\'+'all_db.db', writeback=True)

def hamming(db):
	tem = []
	count = 0
	for k in db.keys():
		count+=1
		for j in tem:
			if distance.hamming(k.encode("utf-8"), j.encode("utf-8")) <= 2:
				value1 = db[k]
				value2 = db[j]
				value = list(set(value1 + value2))
				db[k] = value
				db[j] = value
		tem.append(k)
		sys.stdout.write('\rhamming id [{}/{}  --  {}]'.format('%5d'%count,len(db.keys()),k))
		sys.stdout.flush()

time3= time.time()
for imagePath in glob2.iglob(dataset + "/*/*.jpg"):
	image = Image.open(imagePath)
	h = str(imagehash.dhash(image))
	filename = imagePath[imagePath.rfind('\\') + 1:]
	all_db[h] = all_db.get(h, []) + [filename]
	image.close()
	sys.stdout.write('\rload db subclass {}'.format(imagePath.split('\\')[-2]))
	sys.stdout.flush()

hamming(all_db)
print('\r-----------------------------process inter subclass over-------------------------------time:%d s'%(time.time()-time3))
time4 = time.time()
copy = set()
for key, value in all_db.items():
	if len(value) > 1:
		copy = copy | (set(value))
root = dataset[:dataset.rfind('\\')]
if not os.path.exists(root + '\\' + 'repeat'):
	os.mkdir(root + '\\' + 'repeat')
for path in copy:
	shutil.copy(dataset + '\\' + path[:-10]+'\\'+path, root + '\\' + 'repeat\\' + path)
	sys.stdout.write('\r copy image {} /{}'.format(path,len(copy)))
	sys.stdout.flush()
for path in copy:
	if os.path.exists(dataset + '\\' + path[:-10] + '\\' + path):
		os.remove(dataset + '\\' + path[:-10] + '\\' + path)
	sys.stdout.write('\r delete image {} /{}'.format(path,len(copy)))
	sys.stdout.flush()

print('\r---------------------------------delete repeat over------------------------------------time:%d s'%(time.time()-time4))
print('total time:%.1f min'%((time.time()-time0)/60))


def sort_allrepeat(dir):
	sort_dir = os.path.join(dir,'sort')
	if os.path.exists(sort_dir):
		shutil.rmtree(sort_dir)
	os.mkdir(sort_dir)
	for path in glob2.iglob(dir+'/*.jpg'):
		image = Image.open(path)