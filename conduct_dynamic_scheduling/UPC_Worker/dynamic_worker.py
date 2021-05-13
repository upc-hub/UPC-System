import socket
import sys
import datetime
import time
import os
import csv
import subprocess
from threading import Thread

def main():
	global busy
	busy = 0
	global job_flag
	job_flag = 0
	global measurement
	measurement = '/home/workerpc3/Desktop/upc_dynamic_client.csv'
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
	total_job = soc.recv(5120).decode("utf8")
	global job_flag
	job_flag = job_flag+1
	#print ("Job flag :", job_flag)
	while job_flag<=int(total_job):
		soc.sendall(str(job_flag).encode("utf8"))
		time.sleep(2)
		response = soc.recv(5120).decode("utf8")
		time.sleep(2)
		name_of_job = soc.recv(5120).decode("utf8")
		#print ("Receive from master", response)
		if response=="yes":
			receive_job(job_flag, name_of_job, soc)
		elif response=="last_job":
			receive_last_job(job_flag, soc, name_of_job)
		else:
			time.sleep(5)

def receive_job(job_flag, name_of_job, soc):
	global measurement
	job_start_receive = time_second()
	data = name_of_job+ " start receiving time at workerpc3 is ["+str(job_start_receive)+" second]--["+standard_time(job_start_receive)+"]<<<<"
	record_csv(measurement, data)
	print ("Job No.",job_flag, "is received and ")
	total_time = job_execution(job_flag, name_of_job, soc)
	value = check_job_time(name_of_job)
	total = total_time+value
	data = "Total time is ["+str(total)+" second]--["+standard_time(total)+"]"
	record_csv(measurement, data)
	print ("Finished Job No.", job_flag, "and request master to send the next job.")
	connect_master()

def receive_last_job(job_flag, soc, name_of_job):
	global measurement
	job_start_receive = time_second()
	data = name_of_job+ " start receiving time at workerpc3 is ["+str(job_start_receive)+" second]--["+standard_time(job_start_receive)+"]<<<<"
	record_csv(measurement, data)
	print ("Job No.",job_flag, "is received and ")
	total_time = job_execution(job_flag, name_of_job, soc)
	value = check_job_time(name_of_job)
	total = total_time+value
	data = "Total time is ["+str(total)+" second]--["+standard_time(total)+"]"
	record_csv(measurement, data)
	print ("This is the last job and no more job to assign me. I will leave. Bye...")
	soc.close()
	os._exit(os.EX_OK)

def job_execution(job_flag, name_of_job, soc):
	global measurement
	directory = '/home/workerpc3/Desktop/'
	
	s1 = time_second()
	subprocess.call(['python3', '/home/workerpc3/Desktop/receiver.py'])
	e1 = time_second()
	job_receiving_time = int(e1)-int(s1)
	data1 = "Receiving time is ["+str(job_receiving_time)+" second]--["+standard_time(job_receiving_time)+"]"
	record_csv(measurement, data1)

	s2 = time_second()
	subprocess.call(['podman', 'load', '-i', name_of_job])
	e2 = time_second()
	job_loading_time = int(e2)-int(s2)
	data2 = "Loading time is ["+str(job_loading_time)+" second]--["+standard_time(job_loading_time)+"]"
	record_csv(measurement, data2)

	dd = name_of_job.split('_')
	docker_name = 'pollen5005/'+dd[1]+":latest"

	s3 = time_second()
	subprocess.call(['podman', 'run', '-t', '--name', name_of_job, '-v', '/home/upc/:/opt',docker_name])
	e3 = time_second()
	job_executing_time = int(e3)-int(s3)
	data3 = "Executing time is ["+str(job_executing_time)+" second]--["+standard_time(job_executing_time)+"]"
	record_csv(measurement, data3)

	subprocess.call(['podman', 'container', 'prune'])
	os.remove(str(directory+name_of_job))
	soc.sendall("result".encode("utf8"))
	time.sleep(2)
	result_dir = '/home/upc/'
	fill_count = 0
	for fills_name in os.listdir(result_dir):
		fill_count = fill_count+1
	soc.sendall(str(fill_count).encode("utf8"))
	time.sleep(2)
	soc.sendall(name_of_job.encode("utf8"))
	time.sleep(2)

	s4 = time_second()
	for fills_name in os.listdir(result_dir):
		soc.sendall(str(fills_name).encode("utf8"))
		time.sleep(5)
		fa = open(result_dir+fills_name, 'rb')
		I = fa.read(5120)
		while(I):
			soc.send(I)
			time.sleep(5)
			I = fa.read(5120)
		fa.close()
		time.sleep(5)
	e4 = time_second()
	result_transferring_time = int(e4)-int(s4)
	data4 = "Result transferring time is ["+str(result_transferring_time)+" second]--["+standard_time(result_transferring_time)+"]"
	record_csv(measurement, data4)
	subprocess.call(['podman', 'rmi', docker_name])

	for fills_name in os.listdir(result_dir):
		os.remove(str(result_dir+fills_name))

	total_time = job_receiving_time+job_loading_time+job_executing_time+result_transferring_time
	data5 = "Total time is ["+str(total_time)+" second]--["+standard_time(total_time)+"]"
	record_csv(measurement, data5)
	return total_time

def record_csv(csv_file, data):
	with open(csv_file, 'a') as csvfile:
		csvwriter = csv.writer(csvfile)
		csvwriter.writerow([data])

def check_job_time(name_of_job):
	dd = name_of_job.split('_')
	with open('/home/workerpc3/Desktop/pc_loadtime.csv', 'rt')as f:
		reader = csv.reader(f)
		next(reader, None)
		for row in reader:
			if row[0]==dd[1]:
				value = int(row[1])
				time.sleep(int(value))
				return value
			else:
				print ("Not that job.")
	#if (dd[1]=="dcgana"):
	#	value = 255
	#	time.sleep(255)
	#	return value
	#elif (dd[1]=="dcganb"):
	#	value = 255
	#	time.sleep(255)
	#	return value
	#elif (dd[1]=="opma"):
	#	value = 109
	#	time.sleep(109)
	#	return value
	#else:
	#	value = 109
	#	time.sleep(109)
	#	return value

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

if __name__ == "__main__":
	main()
