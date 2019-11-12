
from pydub import AudioSegment
import os 
from glob import glob
import time
def convert_to_16k(path1, path2):
	'''
	Params:
	-------
		path1: original father path
		path2: out wav father path
	'''
	pathNames = glob(os.path.join(path1,'*'))
	if not os.path.exists(path2):
		os.mkdir((path2))

	for pathname in pathNames:
		bname = os.path.basename(pathname)
		preName = '.'.join(bname.split('.')[:-1])
		sufName = bname.split('.')[-1]

		x = AudioSegment.from_file(os.path.join(path1, bname), format=sufName)
		x = x.set_channels(1)
		x = x.set_frame_rate(16000)
		x = x.set_sample_width(2)
		x.export(os.path.join(path2,preName +'.wav'), format='wav')
	return 0
	
import librosa 
def is_all_16k(path):
	'''
		test files in path is/not all sampling rate 16k.
	'''
	all_flag = True
	pathNames = glob(os.path.join(path,'*'))
	for pathname in pathNames:
		x, sr = librosa.load(pathname, sr=None)
		
		if sr != 16000:
			print(f'{pathname} SAMPLE RATE IS NOT 16K')
			all_flag = False
	if all_flag:
		print(f'ALL files in {path} are 16k.')

# multiprocess
from multiprocessing import cpu_count
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm

def multipro_resample(f, *args, num_workers=None):
	'''
	path1_list = args[0]
	path2_list = args[1]
	'''
	path1_list = args[0]
	path2_list = args[1]

	if num_workers == None:
		num_workers = cpu_count()
		print(f'num_workers = {num_workers}')
	
	executor = ProcessPoolExecutor(max_workers = num_workers)
	futures = []
	for path1, path2 in zip(path1_list, path2_list):
		print(path1, path2)
		futures.append(executor.submit(f, path1, path2))
		result_list = [future.result() for future in tqdm(futures)]
	print(result_list)


def test():
	# convert_to_16k('input_path', 'output_path')
	# is_all_16k('input_path')
	# is_all_16k('output_path')
	
	Pin = [os.path.join('test_multi',str(i)) for i in range(1, 8)]
	Pout = [os.path.join('test_multi','out_'+str(i)) for i in range(1, 8)]
	
	t2 = time.time()
	for i,j in zip(Pin, Pout):
		convert_to_16k(i, j)
	t3 = time.time()
	print(t3-t2)

	t0 = time.time()
	multipro_resample(convert_to_16k, Pin, Pout, num_workers=5)
	t1 = time.time()
	print(t1-t0)

def main(config):
	multipro_resample(convert_to_16k, [config.input_folder], [config.output_folder], config.num_workers)
import argparse	
if __name__ == "__main__":
	# test()
	parser = argparse.ArgumentParser(description="convert folder1's sr to folder2 with sr=16k ")

	parser.add_argument('-i','--input_folder', type=str, default='', help='input the folder what you want convert to 16k')
	parser.add_argument('-o','--output_folder', type=str, default='', help='output floder')	
	parser.add_argument('-n','--num_workers', type=int, default=None, help='多进程数目')
	config = parser.parse_args()

	# main(config)
	is_all_16k(config.output_folder)


