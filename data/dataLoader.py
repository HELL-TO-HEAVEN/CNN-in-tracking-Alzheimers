'''
pyTorch custom dataloader
'''
import h5py
import numpy as np
import torch
from torch.utils.data import DataLoader
from torch.utils.data.sampler import SubsetRandomSampler
from paths import paths, file_names
import os
import pickle as cPickle
from paths import paths, file_names
from modelConfig import params
from random import shuffle

class HDF5loader():
	def __init__(self, filename):
		f = h5py.File(filename, 'r',  libver='latest', swmr=True)
		self.img_f = f['Image4D']
		self.label = [0 if x == 'NL' else (2 if x == 'AD' else 1) for x in f['DIAGNOSIS_LABEL']]
		
	def __getitem__(self, index):
		img = self.img_f[index]
		label = self.label[index]
		
		#print(index, img.max(), img.min())
		
		#for coronal view
		img = np.moveaxis(img, 1, 3)
		
		#normalizing image - Gaussian normalization per volume
		if np.std(img) != 0:  # to account for black images
			mean = np.mean(img)
			std = np.std(img)
			img = 1.0 * (img - mean) / std
		
		img = img.astype(float)
		img = torch.from_numpy(img).float()
		label = torch.LongTensor([label])
		
		return (img ,label)
		
	def __len__(self):
		return self.img_f.shape[0]
	
def dataLoader(hdf5_file):
	data = HDF5loader(hdf5_file)
	num_workers = 8
	
	train_indices = cPickle.load(open(os.path.join(paths['data']['Input_to_Training_Model'],
												   file_names['data']['Train_set_indices']), 'r'))
	shuffle(train_indices)
	
	valid_indices = cPickle.load(open(os.path.join(paths['data']['Input_to_Training_Model'],
												   file_names['data']['Valid_set_indices']), 'r'))
	
	test_indices = cPickle.load(open(os.path.join(paths['data']['Input_to_Training_Model'],
												   file_names['data']['Test_set_indices']), 'r'))
	
	train_sampler = SubsetRandomSampler(train_indices)
	valid_sampler = SubsetRandomSampler(valid_indices)
	test_sampler = SubsetRandomSampler(test_indices)
	
	train_loader = DataLoader(data, batch_size=params['train']['batch_size'], sampler=train_sampler, num_workers=num_workers)
	valid_loader = DataLoader(data, batch_size=params['train']['batch_size'], sampler=valid_sampler, num_workers=num_workers)
	test_loader = DataLoader(data, batch_size=params['train']['batch_size'], sampler=test_sampler, num_workers=num_workers)
	
	return (train_loader, valid_loader, test_loader)

def run_test_():
	max_epochs = 10
	
	datafile = os.path.join(paths['data']['hdf5_path'], file_names['data']['hdf5_file'])
	train_loader, valid_loader, test_loader = dataLoader(datafile)
	
	from tqdm import tqdm
	
	for ep in range(max_epochs):
		print('Epoch ' + str(ep) + ' out of ' + str(max_epochs))
		
		pbt = tqdm(total=len(train_loader))
		
		for batch_idx, (images, labels) in enumerate(train_loader):
			#print('batch ' + str(batch_idx) + ' out of ' + str(len(train_loader)))
			pbt.update(1)
		pbt.close()
	
	
def run_tests():
	n_gpus = 1
	
	max_epochs = 10
	
	data = HDF5loader(os.path.join(paths['data']['hdf5_path'], file_names['data']['hdf5_file']))

	train_sampler = SubsetRandomSampler([0, 1, 2])
	valid_sampler = SubsetRandomSampler([3, 4, 5])

	train_iter = DataLoader(data, batch_size=1*n_gpus, sampler=train_sampler, num_workers=8)
	valid_iter = DataLoader(data, batch_size=1*n_gpus, sampler=valid_sampler, num_workers=8)

	for ep in range(max_epochs):
		print('Epoch ' + str(ep) + ' out of ' + str(max_epochs))

		print('TRAIN:')
		for batch_idx, data_ in enumerate(train_iter):
			batch_x, batch_y = data_
			print('batch ' + str(batch_idx) + str(batch_y) + ' out of ' + str(len(train_iter)))

		
		
		print('VALID:')
		for batch_idx, data_ in enumerate(valid_iter):
			batch_x, batch_y = data_
			print('batch ' + str(batch_idx) + str(batch_y) + ' out of ' + str(len(valid_iter)))
		
		
#run_tests()

#run_test_()