import shutil
import os

output_filename = 'archive'
dir_name = 'dir'


for i in range(534):
	print(i)
	shutil.make_archive(output_filename, 'zip', dir_name)

	shutil.rmtree(dir_name)

	os.makedirs(dir_name)
	shutil.move(output_filename + ".zip", dir_name)
