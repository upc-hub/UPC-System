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

def main():
	connect_master()

def connect_master():
	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	host = "172.28.235.18"
	port = 2000
	try:
		soc.connect((host, port))
		print ("Worker workerpc3 is connected to the UPC Master.")
	except:
		print("Connection error")
		sys.exit()
	soc.sendall("PC3".encode("utf8"))
	master_response = soc.recv(5120).decode("utf8")
	if master_response=="wait":
		print ("There is no job at master.")
		time.sleep(5)
		main()
	else:
		print ("Please execute this job.", master_response)
		receive_job(master_response, soc)

def receive_job(name_of_job, soc):
	directory = '/home/workerpc3/Desktop/data/'
	subprocess.call(['python3', '/home/workerpc3/Desktop/receiver.py'])
	subprocess.call(['chmod', '777', '-R', directory+name_of_job])
	job = name_of_job.split('.')
	if len(job)>1:
		zip_extract(name_of_job, directory)
		execute_job(directory, job[0], soc)
	else:
		print ("This is a container.")

	main()

def zip_extract(name_of_job, directory):
	file_name = directory+name_of_job
	zip_ref = zipfile.ZipFile(file_name)
	extracted = zip_ref.namelist()
	job_name_extract = extracted[0].split('/')
	zip_ref.extractall(directory)
	zip_ref.close()
	subprocess.call(['chmod', '777', '-R', directory])
	subprocess.call(['rm', '-r', directory+name_of_job])
	subprocess.call(['rm', '-r', directory+"Metadata"])
	subprocess.call(['docker', 'run', '-v', '/home/workerpc3/Desktop/data/:/data', '-it', 'seancook/openpose-cpu', '-display', '0', '-image_dir', '/data', '-write_images', '/data'])
	for jobs in os.listdir(directory):
		job_separate = jobs.split("_")
		job_loc = len(job_separate)-1
		if job_separate[job_loc][0]=="r":
			print (job_separate[job_loc],"-----------------")
		else:
			subprocess.call(['rm', '-r', directory+jobs])
			print ("Deleted......")

def execute_job(directory, name_of_job, soc):
	subprocess.call(['chmod', '777', '-R', directory])
	result_dir = "/home/workerpc3/Desktop/result/"+name_of_job
	shutil.make_archive(result_dir, 'zip', directory)
	result = result_dir+".zip"
	send_result(result, soc)

def send_result(result, soc):
	soc.sendall("result".encode("utf8"))
	directory = '/home/workerpc3/Desktop/data/'
	delete_job = ""
	for jobs in os.listdir(directory):
		delete_job = jobs
		subprocess.call(['rm', '-r', directory+delete_job])
	time.sleep(2)
	subprocess.call(['python3', '/home/workerpc3/Desktop/sender.py', result, '172.28.235.18'])
	subprocess.call(['rm', '-r', result])

if __name__ == "__main__":
	main()
