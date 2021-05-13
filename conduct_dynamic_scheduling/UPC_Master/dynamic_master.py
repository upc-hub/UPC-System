import shutil
import csv
import datetime
import time
import socket
import traceback
import sys
import os
import glob
import subprocess
from threading import Thread

def main():
	global flag1
	flag1 = 0
	global flag2
	flag2 = 0
	global flag3
	flag3 = 0
	global flag4
	flag4 = 0
	global flag5
	flag5 = 0
	global flag6
	flag6 = 0
	global measurement
	measurement = '/home/heinhtet/Desktop/Systematic-1/new_complete/upc_dynamic_results.csv'
	
	Thread(target = master_connection_open).start()
	Thread(target = dynamic_job_assignment).start()

def master_connection_open():
	host = "172.28.235.18"
	port = 2000
	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	print ("-------------------------------------")
	print ("Elastic UPC Master is started.")
	try:
		soc.bind((host, port))
	except:
		print ("Bind failed error:"+ str(sys.exc_info()))
		sys.exit()
	soc.listen(120)
	print ("-------------------------------------")
	print ("UPC Master is now listening the workers")
	while True:
		connection, address = soc.accept()
		ip, port = str(address[0]), str(address[1])
		pc_name = connection.recv(5120).decode("utf8")
		if (pc_name=='PC1'):
			try:
				total_send_job = jobs_by_worker(pc_name)
				connection.sendall(str(total_send_job).encode("utf8"))
				job_flag = connection.recv(5120).decode("utf8")
				time.sleep(2)
				Thread(target=check_send_job1, args=(connection, ip, pc_name, job_flag)).start()
			except:
				print ("Thread could not start.")
				traceback.print_exc()
		elif (pc_name=='PC2'):
			try:
				total_send_job = jobs_by_worker(pc_name)
				connection.sendall(str(total_send_job).encode("utf8"))
				job_flag = connection.recv(5120).decode("utf8")
				time.sleep(2)
				Thread(target=check_send_job1, args=(connection, ip, pc_name, job_flag)).start()
			except:
				print ("Thread could not start.")
				traceback.print_exc()
		elif (pc_name=='PC3'):
			try:
				total_send_job = jobs_by_worker(pc_name)
				connection.sendall(str(total_send_job).encode("utf8"))
				job_flag = connection.recv(5120).decode("utf8")
				time.sleep(2)
				Thread(target=check_send_job1, args=(connection, ip, pc_name, job_flag)).start()
			except:
				print ("Thread could not start.")
				traceback.print_exc()
		elif (pc_name=='PC4'):
			try:
				total_send_job = jobs_by_worker(pc_name)
				connection.sendall(str(total_send_job).encode("utf8"))
				job_flag = connection.recv(5120).decode("utf8")
				time.sleep(2)
				Thread(target=check_send_job1, args=(connection, ip, pc_name, job_flag)).start()
			except:
				print ("Thread could not start.")
				traceback.print_exc()
		elif (pc_name=='PC5'):
			try:
				total_send_job = jobs_by_worker(pc_name)
				connection.sendall(str(total_send_job).encode("utf8"))
				job_flag = connection.recv(5120).decode("utf8")
				time.sleep(2)
				Thread(target=check_send_job1, args=(connection, ip, pc_name, job_flag)).start()
			except:
				print ("Thread could not start.")
				traceback.print_exc()
		elif (pc_name=='PC6'):
			try:
				total_send_job = jobs_by_worker(pc_name)
				connection.sendall(str(total_send_job).encode("utf8"))
				job_flag = connection.recv(5120).decode("utf8")
				time.sleep(2)
				Thread(target=check_send_job1, args=(connection, ip, pc_name, job_flag)).start()
			except:
				print ("Thread could not start.")
				traceback.print_exc()
		else:
			print ("There is still no jobs.")


	soc.close()

def check_send_job1(connection, ip, pc_name, job_flag):
	correspond_job_dir = '/home/heinhtet/Desktop/Systematic-1/new_complete/'
	job_search = correspond_job_dir+pc_name+'/'
	total_send_job = jobs_by_worker(pc_name)
	if glob.glob(job_search+job_flag+"*"):
		remove_job = glob.glob(job_search+job_flag+"*")
		#print (remove_job)
		#print ("job flag", job_flag, "Total send job", str(total_send_job))
		send_job(connection, pc_name, job_flag, total_send_job, ip, remove_job[0])
		subprocess.call(['rm', '-r', remove_job[0]])
	else:
		if job_flag == '1':
			print ("-----Please wait worker ", pc_name, ". Jobs are not arrived.")
		else:
			print ("Worker", pc_name, "is busy and please wait to send the job.")
		time.sleep(5)
		check_send_job1(connection, ip, pc_name, job_flag)
	

def send_job(connection, pc_name, job_flag, total_send_job, ip, job):
	if str(job_flag)==str(total_send_job):
		print ("Job No.", job_flag, "is sent to the worker ", pc_name, ". This is the last job.")
		connection.sendall("last_job".encode("utf8"))
		time.sleep(2)
		name_of_job = job.split('/')
		connection.sendall(name_of_job[7].encode("utf8"))
		job_to_execute(connection,ip,job)
		result_alert = connection.recv(5120).decode("utf8")
		if result_alert=="result":
			results_accept(connection, pc_name)
	else:
		print ("Job No.", job_flag, "is sent to the worker ", pc_name)
		connection.sendall("yes".encode("utf8"))
		time.sleep(2)
		name_of_job = job.split('/')
		connection.sendall(name_of_job[7].encode("utf8"))
		job_to_execute(connection,ip,job)
		result_alert = connection.recv(5120).decode("utf8")
		time.sleep(2)
		if result_alert=="result":
			results_accept(connection, pc_name)

def job_to_execute(connection, ip, job):
	time.sleep(3)
	subprocess.call(['python3', '/home/heinhtet/Desktop/Systematic-1/sender.py', job, ip])

def results_accept(connection, pc_name):
	print ("I will accept the result.")
	correspond_job_dir = '/home/heinhtet/Desktop/Systematic-1/new_complete/'
	result_dir = correspond_job_dir+pc_name+"_c/"
	files_count = connection.recv(5120).decode("utf8")
	time.sleep(2)
	jobname = connection.recv(5120).decode("utf8")
	os.makedirs(result_dir+jobname)
	subprocess.call(['chmod', '777', '-R', result_dir+jobname])
	time.sleep(2)
	for account in range(int(files_count)):
		filees_name = connection.recv(5120).decode("utf8")
		time.sleep(5)
		with open(result_dir+jobname+"/"+filees_name, 'wb')as f:
			datta = connection.recv(5120)
			time.sleep(5)
			if not datta:
				f.close()
				#print ("File is closed.")
			f.write(datta)
		print ("Successfully get the file.")

def find_current_flag(pc_name):
	global flag1
	global flag2
	global flag3
	global flag4
	global flag5
	global flag6
	if pc_name=="PC1":
		return flag1
	elif pc_name=="PC2":
		return flag2
	elif pc_name=="PC3":
		return flag3
	elif pc_name=="PC4":
		return flag4
	elif pc_name=="PC5":
		return flag5
	else:
		return flag6


def jobs_by_worker(pc_name):
	workers = []
	flag_job = []
	
	with open('/home/heinhtet/Desktop/Systematic-1/new_complete/timeline.csv') as f:
		reader = csv.reader(f)
		next(reader, None)
		for row in reader:
			workers.append(row[0])
	mylist = list( dict.fromkeys(workers) )
	my_dict = {i:workers.count(i) for i in workers}
	for worker_job_separate in range(len(mylist)):
		flag_job.append(my_dict[mylist[worker_job_separate]])
	#print (mylist, flag_job)
	index = mylist.index(pc_name)
	#print ("The number of jobs at worker:", pc_name, "is ", flag_job[index])
	return flag_job[index]

def dynamic_job_assignment():
	all_job_dir = '/home/heinhtet/Desktop/Systematic-1/new_complete/add_zip/'
	global correspond_job_dir
	correspond_job_dir = '/home/heinhtet/Desktop/Systematic-1/new_complete/'
	global measurement
	modify_time_second = []
	modify_time_standard = []
	jobs = []
	workers = []
	program_starting_time = time_second()
	with open('/home/heinhtet/Desktop/Systematic-1/new_complete/timeline.csv') as f:
		reader = csv.reader(f)
		next(reader, None)
		for row in reader:
			modify_time_second.append(int(program_starting_time)+int(row[2]))
			modify_time_standard.append(time_standard(int(program_starting_time)+int(row[2])))
			jobs.append(row[1])
			workers.append(row[0])
	jobs_count = 0
	jobs_remaining = True

	while jobs_remaining:
		timeline = time_second()
		if (timeline == modify_time_second[jobs_count]):
			print ('Job:', jobs[jobs_count], 'arrives and assign to worker : ', workers[jobs_count],"'s job queue at master [", str(timeline),"]--[",time_standard(timeline),"]<<<<<<")
			data = 'Job:'+ str(jobs[jobs_count])+ 'arrives and assign to worker : '+ str(workers[jobs_count])+"'s job queue at master ["+ str(timeline)+"]--[",time_standard(timeline)+"]<<<<<<"
			record_csv(measurement, data)
			current_flag = flag_for_current_worker(workers[jobs_count])
			os.rename(os.path.join(all_job_dir, jobs[jobs_count]), os.path.join(all_job_dir,str(current_flag)+'_'+jobs[jobs_count]))
			shutil.move(all_job_dir+str(current_flag)+'_'+jobs[jobs_count], correspond_job_dir+workers[jobs_count])
			jobs_count = jobs_count+1
			if jobs_count == len(modify_time_second):
				jobs_remaining = False

def record_csv(csv_file, data):
	with open(csv_file, 'a') as csvfile:
		csvwriter = csv.writer(csvfile)
		csvwriter.writerow([data]) 
	
def flag_for_current_worker(pc_name):
	global flag1
	global flag2
	global flag3
	global flag4
	global flag5
	global flag6
	if pc_name=="PC1":
		flag1 = flag1+1
		return flag1
	elif pc_name=="PC2":
		flag2 = flag2+1
		return flag2
	elif pc_name=="PC3":
		flag3 = flag3+1
		return flag3
	elif pc_name=="PC4":
		flag4 = flag4+1
		return flag4
	elif pc_name=="PC5":
		flag5 = flag5+1
		return flag5
	else:
		flag6 = flag6+1
		return flag6

def time_second():
	start_total = (datetime.datetime.now().hour*3600)+(datetime.datetime.now().minute*60)+datetime.datetime.now().second
	start_time = str(datetime.datetime.now().hour)+":"+str(datetime.datetime.now().minute)+":"+str(datetime.datetime.now().second)
	start_date = str(datetime.datetime.now().day)+"/"+str(datetime.datetime.now().month)+"/"+str(datetime.datetime.now().year)
	return start_total

def time_standard(seconds):
	min, sec = divmod(seconds, 60)
	hour, min = divmod(min, 60)
	return "%d(h):%02d(m):%02d(s)" % (hour, min, sec)


if __name__=="__main__":
	main()	
