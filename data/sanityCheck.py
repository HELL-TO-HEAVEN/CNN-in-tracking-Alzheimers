'''
check what percentage of voxels fall in the specified range of (0, 200)
'''

import nibabel
import os
import glob
from paths import paths, file_names
import re

def checkIntensityRange(file):
	img = nibabel.load(file)
	img = img.get_data()
	
	total_voxels = img.shape[0] * img.shape[1] * img.shape[2]
	within_range_voxel_count = ((img >= 0) & (img <= 200)).sum()
	outside_range_voxel_count = ((img < 0) | (img > 200)).sum()
	print('percentage within range : ', (within_range_voxel_count * 1.0) / total_voxels)
	
def run_tests():
	path = paths['data']['Input_to_Training_Model']
	all_files = glob.glob(os.path.join(path, paths['data']['Raw_MRI_location']))
	for file in all_files:
		print(re.split(r'[/.]', file)[-2])
		checkIntensityRange(file)
		print('\n')
		
run_tests()