import socket
import sys
import datetime
import time
import os
import csv
import subprocess
import zipfile
from threading import Thread
import shutil
import multiprocessing

def main():
	connect_master()

def connect_master():
	global soc
	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	host = "172.28.235.18"
	port = 2000
	try:
		soc.connect((host, port))
		print ("Worker workerpc1 is connected to the UPC Master.")
	except:
		print("Connection error")
		sys.exit()
	soc.sendall("PC6".encode("utf8"))
	master_response = soc.recv(5120).decode("utf8")
	if master_response=="wait":
		print ("There is no job at master.")
		time.sleep(5)
		main()
	else:
		print ("Please execute this job.", master_response)
		receive_job(master_response, soc)

def receive_job(master_response, soc):
	global csv_file
	if (master_response=="one"):
		csv_file = '/home/workerpc5/Desktop/3threads_pc6/Sam_pc6/one/thread_one.csv'
		one(soc)
	elif (master_response=="two"):
		csv_file = '/home/workerpc5/Desktop/3threads_pc6/Sam_pc6/one/thread_one.csv'
		#csv_file = '/home/workerpc5/Desktop/Sam_pc6/two/constant_time_thread.csv'
		two(soc)
	elif (master_response=="three"):
		csv_file = '/home/workerpc5/Desktop/3threads_pc6/Sam_pc6/one/thread_one.csv'
		#csv_file = '/home/workerpc5/Desktop/Sam_pc6/three/constant_time_thread.csv'
		three(soc)
	elif (master_response=="four"):
		csv_file = '/home/workerpc5/Desktop/3threads_pc6/Sam_pc6/one/thread_one.csv'
		#csv_file = '/home/workerpc5/Desktop/Sam_pc6/four/constant_time_thread.csv'
		four(soc)
	elif (master_response=="five"):
		csv_file = '/home/workerpc5/Desktop/3threads_pc6/Sam_pc6/one/thread_one.csv'
		#csv_file = '/home/workerpc5/Desktop/Sam_pc6/five/constant_time_thread.csv'
		five(soc)
	elif (master_response=="six"):
		csv_file = '/home/workerpc5/Desktop/3threads_pc6/Sam_pc6/one/thread_one.csv'
		#csv_file = '/home/workerpc5/Desktop/Sam_pc6/six/constant_time_thread.csv'
		six(soc)
	elif (master_response=="seven"):
		csv_file = '/home/workerpc5/Desktop/3threads_pc6/Sam_pc6/one/thread_one.csv'
		#csv_file = '/home/workerpc5/Desktop/Sam_pc6/seven/constant_time_thread.csv'
		seven(soc)
	elif (master_response=="eight"):
		csv_file = '/home/workerpc5/Desktop/3threads_pc6/Sam_pc6/one/thread_one.csv'
		#csv_file = '/home/workerpc5/Desktop/Sam_pc6/eight/constant_time_thread.csv'
		eight(soc)
	elif (master_response=="nine"):
		csv_file = '/home/workerpc5/Desktop/3threads_pc6/Sam_pc6/one/thread_one.csv'
		#csv_file = '/home/workerpc5/Desktop/Sam_pc6/nine/constant_time_thread.csv'
		nine(soc)
	elif (master_response=="ten"):
		csv_file = '/home/workerpc5/Desktop/3threads_pc6/Sam_pc6/one/thread_one.csv'
		#csv_file = '/home/workerpc5/Desktop/Sam_pc6/ten/constant_time_thread.csv'
		ten(soc)
	else:
		print ("Something wrong.")

def one(soc):
	global chk_thread_count
	chk_thread_count = 0
	thread1_proce = multiprocessing.Process(target = thread1, args=(soc, 'thread_count'))
	thread1_proce.start()
	returna = thread1_proce.join()
	if returna==None:
		main()
	else:
		print ("No need to wait other threads finishing.")

def two(soc):
	global chk_thread_count
	chk_thread_count = 0
	thread1_proce = multiprocessing.Process(target = thread1, args=(soc, 'thread_count'))
	thread2_proce = multiprocessing.Process(target = thread2, args=(soc, 'thread_count'))
	thread1_proce.start()
	thread2_proce.start()
	returna = thread1_proce.join()
	returnb = thread2_proce.join()
	if returna==None and returnb==None:
		main()
	else:
		print ("Wait other threads finishing.")

def three(soc):
	thread1_proce = multiprocessing.Process(target = thread1, args=(soc, 'thread_count'))
	thread2_proce = multiprocessing.Process(target = thread2, args=(soc, 'thread_count'))
	thread3_proce = multiprocessing.Process(target = thread3, args=(soc, 'thread_count'))
	thread1_proce.start()
	thread2_proce.start()
	thread3_proce.start()
	returna = thread1_proce.join()
	returnb = thread2_proce.join()
	returnc = thread3_proce.join()
	if returna==None and returnb==None and returnc==None:
		main()
	else:
		print ("Wait other threads finishing.")

def four(soc):
	thread1_proce = multiprocessing.Process(target = thread1, args=(soc, 'thread_count'))
	thread2_proce = multiprocessing.Process(target = thread2, args=(soc, 'thread_count'))
	thread3_proce = multiprocessing.Process(target = thread3, args=(soc, 'thread_count'))
	thread4_proce = multiprocessing.Process(target = thread4, args=(soc, 'thread_count'))
	thread1_proce.start()
	thread2_proce.start()
	thread3_proce.start()
	thread4_proce.start()
	returna = thread1_proce.join()
	returnb = thread2_proce.join()
	returnc = thread3_proce.join()
	returnd = thread4_proce.join()
	if returna==None and returnb==None and returnc==None and returnd==None:
		main()
	else:
		print ("Wait other threads finishing.")

def five(soc):
	thread1_proce = multiprocessing.Process(target = thread1, args=(soc, 'thread_count'))
	thread2_proce = multiprocessing.Process(target = thread2, args=(soc, 'thread_count'))
	thread3_proce = multiprocessing.Process(target = thread3, args=(soc, 'thread_count'))
	thread4_proce = multiprocessing.Process(target = thread4, args=(soc, 'thread_count'))
	thread5_proce = multiprocessing.Process(target = thread5, args=(soc, 'thread_count'))
	thread1_proce.start()
	thread2_proce.start()
	thread3_proce.start()
	thread4_proce.start()
	thread5_proce.start()
	returna = thread1_proce.join()
	returnb = thread2_proce.join()
	returnc = thread3_proce.join()
	returnd = thread4_proce.join()
	returne = thread5_proce.join()
	if returna==None and returnb==None and returnc==None and returnd==None and returne==None:
		main()
	else:
		print ("Wait other threads finishing.")

def six(soc):
	thread1_proce = multiprocessing.Process(target = thread1, args=(soc, 'thread_count'))
	thread2_proce = multiprocessing.Process(target = thread2, args=(soc, 'thread_count'))
	thread3_proce = multiprocessing.Process(target = thread3, args=(soc, 'thread_count'))
	thread4_proce = multiprocessing.Process(target = thread4, args=(soc, 'thread_count'))
	thread5_proce = multiprocessing.Process(target = thread5, args=(soc, 'thread_count'))
	thread6_proce = multiprocessing.Process(target = thread6, args=(soc, 'thread_count'))
	thread1_proce.start()
	thread2_proce.start()
	thread3_proce.start()
	thread4_proce.start()
	thread5_proce.start()
	thread6_proce.start()
	returna = thread1_proce.join()
	returnb = thread2_proce.join()
	returnc = thread3_proce.join()
	returnd = thread4_proce.join()
	returne = thread5_proce.join()
	returnf = thread6_proce.join()
	if returna==None and returnb==None and returnc==None and returnd==None and returne==None and returnf==None:
		main()
	else:
		print ("Wait other threads finishing.")

def seven(soc):
	thread1_proce = multiprocessing.Process(target = thread1, args=(soc, 'thread_count'))
	thread2_proce = multiprocessing.Process(target = thread2, args=(soc, 'thread_count'))
	thread3_proce = multiprocessing.Process(target = thread3, args=(soc, 'thread_count'))
	thread4_proce = multiprocessing.Process(target = thread4, args=(soc, 'thread_count'))
	thread5_proce = multiprocessing.Process(target = thread5, args=(soc, 'thread_count'))
	thread6_proce = multiprocessing.Process(target = thread6, args=(soc, 'thread_count'))
	thread7_proce = multiprocessing.Process(target = thread7, args=(soc, 'thread_count'))
	thread1_proce.start()
	thread2_proce.start()
	thread3_proce.start()
	thread4_proce.start()
	thread5_proce.start()
	thread6_proce.start()
	thread7_proce.start()
	returna = thread1_proce.join()
	returnb = thread2_proce.join()
	returnc = thread3_proce.join()
	returnd = thread4_proce.join()
	returne = thread5_proce.join()
	returnf = thread6_proce.join()
	returng = thread7_proce.join()
	if returna==None and returnb==None and returnc==None and returnd==None and returne==None and returnf==None and returng==None:
		main()
	else:
		print ("Wait other threads finishing.")

def eight(soc):
	thread1_proce = multiprocessing.Process(target = thread1, args=(soc, 'thread_count'))
	thread2_proce = multiprocessing.Process(target = thread2, args=(soc, 'thread_count'))
	thread3_proce = multiprocessing.Process(target = thread3, args=(soc, 'thread_count'))
	thread4_proce = multiprocessing.Process(target = thread4, args=(soc, 'thread_count'))
	thread5_proce = multiprocessing.Process(target = thread5, args=(soc, 'thread_count'))
	thread6_proce = multiprocessing.Process(target = thread6, args=(soc, 'thread_count'))
	thread7_proce = multiprocessing.Process(target = thread7, args=(soc, 'thread_count'))
	thread8_proce = multiprocessing.Process(target = thread8, args=(soc, 'thread_count'))
	thread1_proce.start()
	thread2_proce.start()
	thread3_proce.start()
	thread4_proce.start()
	thread5_proce.start()
	thread6_proce.start()
	thread7_proce.start()
	thread8_proce.start()
	returna = thread1_proce.join()
	returnb = thread2_proce.join()
	returnc = thread3_proce.join()
	returnd = thread4_proce.join()
	returne = thread5_proce.join()
	returnf = thread6_proce.join()
	returng = thread7_proce.join()
	returnh = thread8_proce.join()
	if returna==None and returnb==None and returnc==None and returnd==None and returne==None and returnf==None and returng==None and returnh==None:
		main()
	else:
		print ("Wait other threads finishing.")

def nine(soc):
	thread1_proce = multiprocessing.Process(target = thread1, args=(soc, 'thread_count'))
	thread2_proce = multiprocessing.Process(target = thread2, args=(soc, 'thread_count'))
	thread3_proce = multiprocessing.Process(target = thread3, args=(soc, 'thread_count'))
	thread4_proce = multiprocessing.Process(target = thread4, args=(soc, 'thread_count'))
	thread5_proce = multiprocessing.Process(target = thread5, args=(soc, 'thread_count'))
	thread6_proce = multiprocessing.Process(target = thread6, args=(soc, 'thread_count'))
	thread7_proce = multiprocessing.Process(target = thread7, args=(soc, 'thread_count'))
	thread8_proce = multiprocessing.Process(target = thread8, args=(soc, 'thread_count'))
	thread9_proce = multiprocessing.Process(target = thread9, args=(soc, 'thread_count'))
	thread1_proce.start()
	thread2_proce.start()
	thread3_proce.start()
	thread4_proce.start()
	thread5_proce.start()
	thread6_proce.start()
	thread7_proce.start()
	thread8_proce.start()
	thread9_proce.start()
	returna = thread1_proce.join()
	returnb = thread2_proce.join()
	returnc = thread3_proce.join()
	returnd = thread4_proce.join()
	returne = thread5_proce.join()
	returnf = thread6_proce.join()
	returng = thread7_proce.join()
	returnh = thread8_proce.join()
	returni = thread9_proce.join()
	if returna==None and returnb==None and returnc==None and returnd==None and returne==None and returnf==None and returng==None and returnh==None and returni==None:
		main()
	else:
		print ("Wait other threads finishing.")

def ten(soc):
	thread1_proce = multiprocessing.Process(target = thread1, args=(soc, 'thread_count'))
	thread2_proce = multiprocessing.Process(target = thread2, args=(soc, 'thread_count'))
	thread3_proce = multiprocessing.Process(target = thread3, args=(soc, 'thread_count'))
	thread4_proce = multiprocessing.Process(target = thread4, args=(soc, 'thread_count'))
	thread5_proce = multiprocessing.Process(target = thread5, args=(soc, 'thread_count'))
	thread6_proce = multiprocessing.Process(target = thread6, args=(soc, 'thread_count'))
	thread7_proce = multiprocessing.Process(target = thread7, args=(soc, 'thread_count'))
	thread8_proce = multiprocessing.Process(target = thread8, args=(soc, 'thread_count'))
	thread9_proce = multiprocessing.Process(target = thread9, args=(soc, 'thread_count'))
	thread10_proce = multiprocessing.Process(target = thread10, args=(soc, 'thread_count'))
	thread1_proce.start()
	thread2_proce.start()
	thread3_proce.start()
	thread4_proce.start()
	thread5_proce.start()
	thread6_proce.start()
	thread7_proce.start()
	thread8_proce.start()
	thread9_proce.start()
	thread10_proce.start()
	returna = thread1_proce.join()
	returnb = thread2_proce.join()
	returnc = thread3_proce.join()
	returnd = thread4_proce.join()
	returne = thread5_proce.join()
	returnf = thread6_proce.join()
	returng = thread7_proce.join()
	returnh = thread8_proce.join()
	returni = thread9_proce.join()
	returnj = thread10_proce.join()
	if returna==None and returnb==None and returnc==None and returnd==None and returne==None and returnf==None and returng==None and returnh==None and returni==None and returnj==None:
		main()
	else:
		print ("Wait other threads finishing.")

def thread1(soc, thread):
	global csv_file
	global chk_thread_count
	start = time_second()
	subprocess.call(['python3', '/home/workerpc5/Desktop/receiver1.py', 'data1', '6004'])
	end = time_second()
	receive = standard_time(int(end)-int(start))
	#record_csv(csv_file, receive+' Thread-1 job receiving time.')
	#soc.sendall("send1_finish".encode("utf8"))
	start1 = time_second()
	job_execute('data1', '6004', start1, 'thread1', 'e02bc3150457', soc)
	soc.close()
	return "THREAD-1" 


def thread2(soc, thread):
	global csv_file
	global chk_thread_count
	start = time_second()
	subprocess.call(['python3', '/home/workerpc5/Desktop/receiver1.py', 'data2', '6005'])
	end = time_second()
	receive = standard_time(int(end)-int(start))
	#record_csv(csv_file, receive+' Thread-2 job receiving time.')
	#soc.sendall("send2_finish".encode("utf8"))
	start1 = time_second()
	job_execute('data2', '6005', start1, 'thread2', 'cc775df9df0c', soc)
	soc.close()
	return "THREAD-2"

def thread3(soc, thread):
	global csv_file
	global chk_thread_count
	start = time_second()
	subprocess.call(['python3', '/home/workerpc5/Desktop/receiver1.py', 'data3', '6006'])
	end = time_second()
	receive = standard_time(int(end)-int(start))
	#record_csv(csv_file, receive+' Thread-1 job receiving time.')
	#soc.sendall("send3_finish".encode("utf8"))
	start1 = time_second()
	job_execute('data3', '6006', start1, 'thread3', '766c3e157745', soc)
	soc.close()
	return "THREAD-3"


def thread4(soc, thread):
	global csv_file
	global chk_thread_count
	start = time_second()
	subprocess.call(['python3', '/home/workerpc5/Desktop/receiver1.py', 'data4', '6007'])
	end = time_second()
	receive = standard_time(int(end)-int(start))
	#record_csv(csv_file, receive+' Thread-1 job receiving time.')
	#soc.sendall("send4_finish".encode("utf8"))
	start1 = time_second()
	job_execute('data4', '6007', start1, 'thread4', 'a685a2d167f9', soc)
	soc.close()
	return "THREAD-4"


def thread5(soc, thread):
	global csv_file
	global chk_thread_count
	start = time_second()
	subprocess.call(['python3', '/home/workerpc5/Desktop/receiver1.py', 'data5', '6008'])
	end = time_second()
	receive = standard_time(int(end)-int(start))
	#record_csv(csv_file, receive+' Thread-1 job receiving time.')
	#soc.sendall("send4_finish".encode("utf8"))
	start1 = time_second()
	job_execute('data5', '6008', start1, 'thread5', '56dc1f39133a', soc)
	soc.close()
	return "THREAD-5"


def thread6(soc, thread):
	global csv_file
	global chk_thread_count
	start = time_second()
	subprocess.call(['python3', '/home/workerpc5/Desktop/receiver1.py', 'data6', '6009'])
	end = time_second()
	receive = standard_time(int(end)-int(start))
	#record_csv(csv_file, receive+' Thread-1 job receiving time.')
	#soc.sendall("send4_finish".encode("utf8"))
	start1 = time_second()
	job_execute('data6', '6009', start1, 'thread6', '24a6d610e433', soc)
	soc.close()
	return "THREAD-6"


def thread7(soc, thread):
	global csv_file
	global chk_thread_count
	start = time_second()
	subprocess.call(['python3', '/home/workerpc5/Desktop/receiver1.py', 'data7', '6010'])
	end = time_second()
	receive = standard_time(int(end)-int(start))
	#record_csv(csv_file, receive+' Thread-1 job receiving time.')
	#soc.sendall("send4_finish".encode("utf8"))
	start1 = time_second()
	job_execute('data7', '6010', start1, 'thread7', 'b5ef0705b6d3', soc)
	soc.close()
	return "THREAD-7"


def thread8(soc, thread):
	global csv_file
	global chk_thread_count
	start = time_second()
	subprocess.call(['python3', '/home/workerpc5/Desktop/receiver1.py', 'data8', '6011'])
	end = time_second()
	receive = standard_time(int(end)-int(start))
	#record_csv(csv_file, receive+' Thread-1 job receiving time.')
	#soc.sendall("send4_finish".encode("utf8"))
	start1 = time_second()
	job_execute('data8', '6011', start1, 'thread8', '8c4256c8ef73', soc)
	soc.close()
	return "THREAD-8"


def thread9(soc, thread):
	global csv_file
	global chk_thread_count
	start = time_second()
	subprocess.call(['python3', '/home/workerpc5/Desktop/receiver1.py', 'data9', '6012'])
	end = time_second()
	receive = standard_time(int(end)-int(start))
	#record_csv(csv_file, receive+' Thread-1 job receiving time.')
	#soc.sendall("send4_finish".encode("utf8"))
	start1 = time_second()
	job_execute('data9', '6012', start1, 'thread9', 'e21bc3da3625', soc)
	soc.close()
	return "THREAD-9"


def thread10(soc, thread):
	global csv_file
	global chk_thread_count
	start = time_second()
	subprocess.call(['python3', '/home/workerpc5/Desktop/receiver1.py', 'data10', '6013'])
	end = time_second()
	receive = standard_time(int(end)-int(start))
	#record_csv(csv_file, receive+' Thread-1 job receiving time.')
	#soc.sendall("send4_finish".encode("utf8"))
	start1 = time_second()
	job_execute('data10', '6013', start1, 'thread10', 'cc26c46133a0', soc)
	soc.close()
	return "THREAD-10"


def job_execute(data, portt, start1, thread_name, container_name, soc):
	 global csv_file
	 directory = '/home/workerpc5/Desktop/'+data+'/'
	 #global soc
	 name_of_job = ""
	 for name_job in os.listdir(directory):
	 	name_of_job = name_job
	# subprocess.call(['python3', '/home/workerpc5/Desktop/receiver.py'])
	 subprocess.call(['chmod', '777', '-R', directory+name_of_job])
	 job = name_of_job.split('.')
	 plas_job = job[0].split('_')
	 eeplas_job = job[0].split('-')
	 eeeplas_job = eeplas_job[0].split('_')
	 if plas_job[2]=="EPLAS":
	 	zip_extract(name_of_job, directory)
	 	eplas_execute(name_of_job, directory)
	 	execute_job_plas(directory, job[0], soc, portt, start1, thread_name)
	 	main()
	 elif eeeplas_job[2]=="aplas":
	 	print ("This is the aplas job.")
	 	#start2 = time_second()
	 	zip_extract(name_of_job, directory)
	 	#end2 = time_second()
	 	#preparation_time = standard_time(int(end2)-int(start2))
	 	#record_csv(csv_file, preparation_time+thread_name+' job preparation_time.---->'+name_of_job)
	 	start3 = time_second()
	 	aplas_execute(name_of_job, directory, container_name)
	 	end3 = time_second()
	 	real_execution_time = str(int(end3)-int(start3))
	 	abc = name_of_job.split('-')
	 	ddd = abc[1].split('.')
	 	record_csv(csv_file, real_execution_time, ddd[0])
	 	execute_job_plas(directory, job[0], soc, portt, start1, thread_name)
	 	#soc_check(soc)
	 	#time.sleep(5)
	 	#main()
	 else:
	 	print ("This is a container.")
	 	main()

	#main()

#def soc_check(soc):
#	soc_check.counter +=1
#	print (soc_check.counter)

def aplas_execute(name_of_job,  directory, container_name):
	#subprocess.call(['scp', '-r', '/home/workerpc5/Desktop/android-container/latest/AplasClient.jar', '/home/workerpc5/Desktop/data/'])
	#subprocess.call(['chmod', '777', '-R', directory])
	aplas_zip_file = ''
	aplas_manifest_file = ''
	aplas_log = ''
	for filename in os.listdir(directory):
		job_separate = filename.split(".")
		aplas_log = job_separate[0]
		if job_separate[1]=="zip":
			aplas_zip_file=filename
		elif job_separate[1]=="manifest":
			aplas_manifest_file = filename
		else:
			print ("The file might be jar file.")
	subprocess.call(['docker', 'cp', directory+aplas_manifest_file, container_name+':/app'])
	subprocess.call(['docker', 'cp', directory+aplas_zip_file, container_name+':/app'])
	cmd = ['docker', 'exec', '-ti', container_name, 'sudo', 'java', '-jar', 'AplasClient.jar', '--workPath=/app/', '--zipFile='+aplas_zip_file, '--manifest='+aplas_manifest_file, '--sdkPath=/opt/android']

	with open(directory+job_separate[0]+'.log', 'w') as out:
	    return_code = subprocess.call(cmd, stdout=out)
	subprocess.call(['docker', 'cp', container_name+':/app/'+job_separate[0]+'.result', directory])
	#subprocess.call(['docker', 'run', '--cpus=20', '--privileged=true', '-i', '-v', '/home/workerpc5/Desktop/data/:/app', '-it', 'pollen5005:sunflower', 'sudo', 'java', '-jar', 'AplasClient.jar', '--workPath=/app/', '--zipFile='+aplas_zip_file, '--manifest='+aplas_manifest_file, '--sdkPath=/opt/android'])
	subprocess.call(['chmod', '777', '-R', directory])
	for filename in os.listdir(directory):
		try:
			job_separate = filename.split(".")
			if job_separate[1]=='result':
				print ("This is the result file.")
			elif job_separate[1]=='log':
				print ("This is the log file.")
			else:
				subprocess.call(['rm', '-r', directory+filename])
			#if job_separate[1]!='result' or job_separate[1]!='log':
			#	subprocess.call(['rm', '-r', directory+filename])
			#else:
			#	print ('This may be result file or log file.')
		except IndexError:
			print ('This is the topic file name.')
			subprocess.call(['rm', '-r', directory+filename])

def zip_extract(name_of_job, directory):
	file_name = directory+name_of_job
	zip_ref = zipfile.ZipFile(file_name)
	extracted = zip_ref.namelist()
	job_name_extract = extracted[0].split('/')
	zip_ref.extractall(directory)
	zip_ref.close()
	subprocess.call(['chmod', '777', '-R', directory])
	subprocess.call(['rm', '-r', directory+name_of_job])

def eplas_execute(name_of_job, directory):
	subprocess.call(['rm', '-r', directory+"Metadata"])
	subprocess.call(['docker', 'run', '-v', '/home/workerpc5/Desktop/data/:/data', '-it', 'seancook/openpose-cpu', '-display', '0', '-image_dir', '/data', '-write_images', '/data'])
	for jobs in os.listdir(directory):
		job_separate = jobs.split("_")
		job_loc = len(job_separate)-1
		if job_separate[job_loc][0]=="r":
			print (job_separate[job_loc],"-----------------")
		else:
			subprocess.call(['rm', '-r', directory+jobs])
			print ("Deleted......")

def execute_job_plas(directory, name_of_job, soc, portt, start1, thread_name):
	global csv_file
	subprocess.call(['chmod', '777', '-R', directory])
	result_dir = "/home/workerpc5/Desktop/result/"+name_of_job
	shutil.make_archive(result_dir, 'zip', directory)
	result = result_dir+".zip"
	end1 = time_second()
	receive1 = standard_time(int(end1)-int(start1))
	#record_csv(csv_file, receive1+ thread_name+' (Total) job execution time.---->'+ name_of_job)
	start2 = time_second()
	send_result(result, soc, directory, portt)
	end2 = time_second()
	receive2 = standard_time(int(end2)-int(start2))
	#record_csv(csv_file, receive2+ thread_name+' result sending time.---->'+ name_of_job)

def record_csv(csv_file, execution_time, name_of_job):
	with open(csv_file, 'a') as csvfile:
		csvwriter = csv.writer(csvfile)
		csvwriter.writerow([name_of_job, execution_time])

def time_second():
	start_total = (datetime.datetime.now().hour*3600)+(datetime.datetime.now().minute*60)+datetime.datetime.now().second
	start_time = str(datetime.datetime.now().hour)+":"+str(datetime.datetime.now().minute)+":"+str(datetime.datetime.now().second)
	start_date = str(datetime.datetime.now().day)+"/"+str(datetime.datetime.now().month)+"/"+str(datetime.datetime.now().year)
	#print ("Starting time(h:m:s)-"+start_time+" ("+start_date+")")
	return start_total

def standard_time(seconds): 
	min, sec = divmod(seconds, 60) 
	hour, min = divmod(min, 60) 
	return "%d(h):%02d(m):%02d(s)" % (hour, min, sec)

def send_result(result, soc, directory, portt):
	##soc.sendall(portt.encode("utf8"))
	#directory = '/home/workerpc5/Desktop/data/'
	delete_job = ""
	for jobs in os.listdir(directory):
		delete_job = jobs
		subprocess.call(['rm', '-r', directory+delete_job])
	time.sleep(2)
	#soc.sendall(str(number).encode("utf8"))
	##alarm = soc.recv(5120).decode("utf8")
	##if alarm=="ready":
	time.sleep(3)
	subprocess.call(['python3', '/home/workerpc5/Desktop/sender.py', result, '172.28.235.18', portt])
	subprocess.call(['rm', '-r', result])
		#subprocess.call(['python3', '/home/workerpc5/Desktop/sender.py', result, '172.28.235.18'])
	#subprocess.call(['rm', '-r', result])

if __name__ == "__main__":
	sys.setrecursionlimit(10**7)
	#soc_check.counter = 0
	main()