# USAGE
# python index.py --dataset images --shelve db.shelve

# import the necessary packages
from PIL import Image
import imagehash
import distance
import argparse
import shelve
import shutil
import glob
import os
from PIL import ImageFile # Python：IOError: image file is truncated 的解决办法
ImageFile.LOAD_TRUNCATED_IMAGES = True

def remove_sameclass(subdataset,subclass):
	# construct the argument parse and parse the arguments

	sub_path =subdataset +'\\'+ subclass
	saved_db = os.getcwd()+'\\'+'db'+'\\'+subclass[:3]+'.db'
	if os.path.exists(saved_db + '.bak'):
		os.remove(saved_db + '.bak')
		print('delete '+subclass[:3]+'.bak   ', end=' ')
	if os.path.exists(saved_db + '.dat'):
		os.remove(saved_db + '.dat')
		print('delete '+subclass[:3]+'.dat   ', end=' ')
	if os.path.exists(saved_db + '.dir'):
		os.remove(saved_db + '.dir')
		print('delete '+subclass[:3]+'.dir   ')

	# open the shelve database
	db = shelve.open(saved_db, writeback=True)

	def hamming(db):
		tem = []
		for k in db.keys():
			for j in tem:
				if distance.hamming(k.encode("utf-8"), j.encode("utf-8")) <= 2:
					value1 = db[k]
					value2 = db[j]
					value = list(set(value1 + value2))
					db[k] = value
					db[j] = value
			tem.append(k)

	# loop over the image dataset
	for imagePath in glob.glob(sub_path + "/*.jpg"):
		# load the image and compute the difference hash
		image = Image.open(imagePath)
		h = str(imagehash.dhash(image))

		# extract the filename from the path and update the database
		# using the hash as the key and the filename append to the
		# list of values
		# print(imagePath.rfind('\\'))
		filename = imagePath[imagePath.rfind('\\') + 1:]
		# print(filename,h)
		db[h] = db.get(h, []) + [filename]
		#print(db[h])
		image.close()
	hamming(db)
	copy = set()
	for key, value in db.items():
		if len(value) > 1:
			copy = copy | (set(value))
	if not os.path.exists(sub_path + '\\' + 'repeat'):
		os.mkdir(sub_path + '\\' + 'repeat')
	for path in copy:
		shutil.copy(sub_path + '\\' + path, sub_path + '\\' + 'repeat\\' + path)
	for key, value in db.items():
		if len(value) > 1:
			for i in range(len(value) - 1):
				if os.path.isfile(sub_path + '\\' + value[i]):
					os.remove(sub_path + '\\' + value[i])
	# close the shelf database
	db.close()