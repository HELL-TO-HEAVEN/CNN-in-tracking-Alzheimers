'''
pyTorch custom dataloader
'''
import h5py
import numpy as np
import torch
from torch.utils.data import DataLoader
from torch.utils.data.sampler import SubsetRandomSampler

class HDF5loader():
	def __init__(self, filename):
		self.img_f = filename['Image4D']
		#self.label = filename['DIAGNOSIS_LABEL']
		
	def __getitem__(self, index):
		img = self.img_f[index]
		
		#for coronal view
		img = np.moveaxis(img, 1, 3)
		
		#normalizing image - Gaussian normalization per volume
		if np.std(img) != 0:  # to account for black images
			mean = np.mean(img)
			std = np.std(img)
			image = 1.0 * (img - mean) / std
		
		#label = self.label[index]
		
		img = img.astype(float)
		img = torch.from_numpy(img).float()
		#label = torch.LongTensor(label)
		
		return img #, label)
		
	def __len__(self):
		return self.img_f.shape[0]
	
	
def run_tests():
	n_gpus = 1
	
	max_epochs = 10
	
	hdf5_file = h5py.File('/home/NOBACKUP/sbasu11/3DMRItoNextLabel.hdf5', 'r',  libver='latest', swmr=True)
	data = HDF5loader(hdf5_file)

	train_sampler = SubsetRandomSampler([0, 1, 2])
	#valid_sampler = SubsetRandomSampler([3, 4, 5])

	train_iter = DataLoader(data, batch_size=1*n_gpus, sampler=train_sampler, num_workers=8)
	#valid_iter = DataLoader(data, batch_size=1*n_gpus, sampler=valid_sampler, num_workers=8)

	for ep in range(max_epochs):
		print('Epoch ' + str(ep) + ' out of ' + str(max_epochs))

		print('TRAIN:')
		for batch_idx, data_ in enumerate(train_iter):
			batch_x = data_
			print('batch ' + str(batch_idx) + ' out of ' + str(len(train_iter)))

		
		'''
        print('VALID:')
        for batch_idx, data_ in enumerate(valid_iter):
            batch_x = data_
            print('batch ' + str(batch_idx) + ' out of ' + str(len(valid_iter)))
		'''
		
run_tests()