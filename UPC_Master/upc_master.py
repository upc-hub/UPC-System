from datetime import date
from threading import Thread
import shutil
import datetime
import time
import schedule
import os
import json
import subprocess
import zipfile
import socket
import traceback
import csv
import filetype

global token_counter_today
token_counter_today = 0
global available_list           #current available worker list connected to UPC Master
available_list = []

def main():
	Thread(target = master_connection_open).start()             #UPC Master allows connection for the workers
	while True:
		schedule.run_pending()
		time.sleep(1)

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
	while True:                                                         #Master automatically issue a thread for the incoming worker
		connection, address = soc.accept()
		ip, port = str(address[0]), str(address[1])
		pc_name = connection.recv(5120).decode("utf8")
		if (pc_name=='PC1'):
			try:
				job_flag = 1
				Thread(target=check_send_job, args=(connection, ip, pc_name, job_flag)).start()        #enter to the available worker list, if job exists, worker can accept that job to be processed.Otherwise, keep connected to Master
			except:
				print ("Thread could not start.")
				traceback.print_exc()
		elif (pc_name=='PC2'):
			try:
				job_flag = 1
				Thread(target=check_send_job, args=(connection, ip, pc_name, job_flag)).start()        #enter to the available worker list, if job exists, worker can accept that job to be processed.Otherwise, keep connected to Master
			except:
				print ("Thread could not start.")
				traceback.print_exc()
		elif (pc_name=='PC3'):
			try:
				job_flag = 1
				Thread(target=check_send_job, args=(connection, ip, pc_name, job_flag)).start()        #enter to the available worker list, if job exists, worker can accept that job to be processed.Otherwise, keep connected to Master
			except:
				print ("Thread could not start.")
				traceback.print_exc()
		elif (pc_name=='PC4'):
			try:
				job_flag = 1
				Thread(target=check_send_job, args=(connection, ip, pc_name, job_flag)).start()        #enter to the available worker list, if job exists, worker can accept that job to be processed.Otherwise, keep connected to Master
			except:
				print ("Thread could not start.")
				traceback.print_exc()
		elif (pc_name=='PC5'):
			try:
				job_flag = 1
				Thread(target=check_send_job, args=(connection, ip, pc_name, job_flag)).start()        #enter to the available worker list, if job exists, worker can accept that job to be processed.Otherwise, keep connected to Master
			except:
				print ("Thread could not start.")
				traceback.print_exc()
		elif (pc_name=='PC6'):
			try:
				job_flag = 1
				Thread(target=check_send_job, args=(connection, ip, pc_name, job_flag)).start()        #enter to the available worker list, if job exists, worker can accept that job to be processed.Otherwise, keep connected to Master
			except:
				print ("Thread could not start.")
				traceback.print_exc()
		else:
			print ("There is still no jobs.")

def check_send_job(connection, ip, pc_name, job_flag):                        #each worker pc obtains a channel and enter to the available worker list
	print (pc_name+" is connected and plese check jobs.")
	global available_list
	reply = update_worker(pc_name)
	if reply[0]=="No job":
		connection.sendall("wait".encode("utf8"))
	else:
		check_job_to_execute(connection, ip, pc_name)

def rename_job():                                          #submitted jobs are renamed to be compactible with the system requirements e.g. currentToken_ddmmyyyy_jobName
	global token_counter_today
	global available_list
	print ("Currently available worker : ", available_list)
	EPLAS_dir = '/home/heinhtet/Desktop/UPC_Master/EPLAS/newJobs/'            #EPLAS job directory (EPLAS system assigns jobs through pCloud-https)
	APLAS_dir = '/home/heinhtet/Desktop/UPC_Master/APLAS/newJobs/'			  #APLAS job directory (APLAS system assigns jobs through FTP)
	local_dir = '/home/heinhtet/Desktop/UPC_Master/local_user/newJobs/'       #Local user job directory (local user assigns jobs through LAN_static-https)
	all_job_dir = '/home/heinhtet/Desktop/UPC_Master/temporary_queue/'        #group all submitted jobs from various system
	com_job_dir = '/home/heinhtet/Desktop/UPC_Master/common_queue/'           #renamed all submitted jobs Queue
	subprocess.call(['scp', '-r', APLAS_dir+'.', all_job_dir])
	subprocess.call(['rm', '-r', APLAS_dir])
	subprocess.call(['scp', '-r', local_dir+'.', all_job_dir])
	subprocess.call(['rm', '-r', local_dir])
	subprocess.call(['scp', '-r', EPLAS_dir+'.', all_job_dir])
	try:
		subprocess.call(['rm', '-r', EPLAS_dir])
	except:
		print ("No files to move")
	
	for file_name in os.listdir(all_job_dir):
		job_name = str(file_name)
		if (job_name[0].isdigit()):							#check renamed or not
			print ()
		token_counter_today = token_counter_today + 1
		token = initiate_job_token()
		os.rename(os.path.join(all_job_dir, file_name), os.path.join(all_job_dir,token+'_'+file_name))          #renaming process
		shutil.move(all_job_dir+token+'_'+file_name, com_job_dir)											    #renamed jobs are moved to common Queue
		zip_extract(token+'_'+file_name, com_job_dir)      													    #extract jobs's zips

schedule.every(30).seconds.do(rename_job)                  #UPC Master checks jobs arrive from UPC Web Server every 30 seconds

def initiate_job_token():								   #generate currentToken for the submitted jobs
	global token_counter_today
	if check_day_change():                                 #check change to the next day or not for reseting the token
		token_counter_today = 0
	today_date = date.today()
	day = str(today_date.day)
	month = str(today_date.month)
	year = str(today_date.year)
	generate_token = str(token_counter_today)+"_"+day+month+year
	return generate_token

def check_day_change():                                    #check change to the next day or not			  						
	hour = datetime.datetime.now().hour
	minute = datetime.datetime.now().minute
	second = datetime.datetime.now().second
	if (hour == '23' and minute == '59' and second == '59'):
		return True

def zip_extract(job_name, directory):                      #extract job's zip file and read the Metadata of job 
	zip_name = job_name.split('.')
	zip_name_container = job_name.split('_')
	file_name = directory+job_name
	zip_ref = zipfile.ZipFile(file_name)
	extracted = zip_ref.namelist()
	name_of_job = extracted[0].split('/')
	zip_ref.extractall(directory)
	zip_ref.close()
	os.rename(os.path.join(directory, name_of_job[0]), os.path.join(directory,zip_name[0]))       #extracted zip's name may be different from the renames by the System
	os.remove(file_name)                                                                          #previous zip files are removed
	subprocess.call(['chmod', '777', '-R', directory])
	job_dir = directory+zip_name[0]
	check_container_require(zip_name_container[0], job_dir, zip_name[0])                          #check container is needed to build or not by reading job's Metadata

def check_container_require(zip_name_container, job_dir, sys_name):
	global available_list
	container_queue = '/home/heinhtet/Desktop/UPC_Master/container_queue/'
	common_queue = '/home/heinhtet/Desktop/UPC_Master/common_queue/'
	docker_template = '/home/heinhtet/Desktop/UPC_Master/Dockerfile'               #Dokerfile template if job is necessary to build a container
	base_directory = '/home/heinhtet/Desktop/UPC_Master/'
	detect_system = sys_name.split('_')
	local = detect_system[2]
	if(local[0]=='l'):                                                             #differentiate between local and outsider systems
		detect_system[2]='local_user'
	with open(job_dir+"/Metadata") as json_file:
		data = json.load(json_file)
		for p in data['job']:
			if p['Container_require']=='no':
				subprocess.call(['scp', '-r', common_queue+sys_name, base_directory+detect_system[2]+'/jobStatus/waiting/'])          #after necessary checking, jobs are moved to the waiting queue of correspondance system. It can be seen on Web interface.
				shutil.move(job_dir, container_queue)                              #All checked jobs are reached to the container queue and then, moved to the correspondance worker queue
				available_worker = current_available_worker()                      #checked is there any worker already connected to master before jobs arrived
				if available_worker=="":                                           #if there is no available worker, assign null
					print ()
				else:
					shutil.move(container_queue+str(sys_name), base_directory+str(available_worker))      #if there is a worker for the current job, this job is moved from the container queue to that worker queue 
				update_job_list(sys_name, available_worker)                                               #record current job and worker's tates
				try:
					print (available_list[0], "<<<<this worker will be poped from the list.")             #If a job is assigned to the worker, that worker is removed from the available worker list.
					pop_worker(available_list[0])
				except IndexError:
					print ()
			else:                                                                  #if job needs to build container, modify the Dockerfile template in accordance with the information stated in Metadata
				shutil.copy(docker_template, job_dir)
				docker_directory = job_dir+"/Dockerfile"
				f = open(docker_template, 'r')
				message = f.read()
				message = message.replace('#MAINTAINER',p['System_name'])
				message = message.replace('#FROM',p['Type of program'])
				message = message.replace('#WORKDIR','/app')
				message = message.replace('#COPY','. /app')
				message = message.replace('#RUN','pip install -r '+p['Dependency file name'])
				message = message.replace('ADD','#ADD')
				message = message.replace('#CMD',p['Execute command'])
				message = message.replace('ENV','#ENV')
				message = message.replace('ENTRYPOINT','#ENTRYPOINT')
				message = message.replace('EXPOSE','#EXPOSE')
				with open(docker_directory, 'w')as f:
					f.write(message)
				f.close()
				subprocess.call(['docker', 'build', '-t', 'pollen5005/'+p['System_name'].lower()+":latest", job_dir])                                   #build the docker image accordance with Dockerfile
				transform_job = container_queue+zip_name_container+"_"+p['System_name'].lower()
				subprocess.call(['docker', 'save', '-o', transform_job, 'pollen5005/'+p['System_name'].lower()+":latest"])                              #container job is put under container queue
				subprocess.call(['rm', '-r', job_dir])
				subprocess.call(['chmod', '777', '-R', transform_job])
				subprocess.call(['touch', base_directory+detect_system[2]+'/jobStatus/waiting/'+zip_name_container+"_"+p['System_name'].lower()])       #Job state can be seen on the web interface according to the system 
				available_worker = current_available_worker()                                                                                           #checked is there any worker already connected to master before jobs arrived
				if available_worker=="":                                                                                                                #if there is no available worker, assign null
					print ()
				else:
					shutil.move(container_queue+str(zip_name_container+"_"+p['System_name'].lower()), base_directory+str(available_worker))             #if there is a worker for the current job, this job is moved from the container queue to that worker queue 
				update_job_list(zip_name_container+"_"+p['System_name'].lower(), available_worker)
				try:
					print (available_list[0], "<<<<this worker will be poped from the list.")                                                           #If a job is assigned to the worker, that worker is removed from the available worker list.
					pop_worker(available_list[0])
				except IndexError:
					print ()
				print('System_name: ' + p['System_name'])                                                                                               #Metadata of container needed job
				print('Container_require: ' + p['Container_require'])
				print('Job_name: ' + p['Job_name'])
				print('')

def update_job_list(job_name, status):                                                 #record job and worker status
	job_list_loc = '/home/heinhtet/Desktop/UPC_Master/job_list_status.csv'
	with open(job_list_loc, 'a') as csvfile1:
		fieldnames1 = ['Job', 'Status']
		writerpp1 = csv.DictWriter(csvfile1, fieldnames=fieldnames1)
		writerpp1.writerow({'Job': job_name, 'Status': status})


def current_available_worker():                                                        #check is there any available worker in the list for the current job
	global available_list
	try:
		return available_list[0]
	except IndexError:
		null_str = ""
		return null_str
		print ("All worker are busy.")
	

def update_worker(pc):                                                                 #connected workers update 
	global available_list
	container_queue = '/home/heinhtet/Desktop/UPC_Master/container_queue/'
	base_directory = '/home/heinhtet/Desktop/UPC_Master/'
	print (available_list, "Check job by worker")
	print ("This is the length", len(available_list))
	if len(available_list)==0:                                                         #check connected worker is already in the available worker list
		push_worker(pc)                                                                #if not, that worker is added to the available worker list
		print ("This is the first time join.")                                        
	else:                                                                              #connected worker is already in the avaialable list
		break_out_flag1 = False
		print ("This is not the first time.")
		for worker in range(0, len(available_list)):
			if pc in available_list[worker]:
				break_out_flag1 = True
				break
		if break_out_flag1:
			print (pc, "This worker is already added.")
		else:
			push_worker(pc)
			print (pc, "This worker is added to the available list.")
	send_job = ""
	send_worker = ""
	no_job = ""
	no_worker = ""
	with open('/home/heinhtet/Desktop/UPC_Master/job_list_status.csv') as f:          #update job and worker list (this time is adding current connected worker to the status file.)
		reader = csv.reader(f)
		lines = list(reader)
		try:
			if lines[1][0] == "":
				no_job = "No job"
				no_worker = "No worker"
			else:                                                                     #if job already added in the status file but there is no worker for this job. (Update that place)
				break_out_flag = False
				for i in range(len(lines)):
					for j in range(len(lines[i])):
						if lines[i][j]=="":
							lines[i][j] = available_list[0]
							send_job = lines[i][j-1]
							send_worker = lines[i][j]
							break_out_flag = True
							pop_worker(pc)
							break
						else:
							print ()
					if break_out_flag:
						break

				with open('/home/heinhtet/Desktop/UPC_Master/job_list_status.csv', 'w') as csvfile:
					csvwriter = csv.writer(csvfile)
					csvwriter.writerows(lines)
				print ("There is a job.")
				try:
					shutil.move(container_queue+send_job, base_directory+send_worker)                      #Update job is moved to the correspondance worker queue
				except shutil.Error:
					print ()

				return send_job, send_worker

		except IndexError:
			send_job = "No job"
			send_worker = "No worker"
			print ("There is no job.")
			return send_job, send_worker

def check_job_to_execute(connection, ip, pc_name):                               
	container_queue = '/home/heinhtet/Desktop/UPC_Master/container_queue/'
	base_directory = '/home/heinhtet/Desktop/UPC_Master/'
	if len(os.listdir(base_directory+pc_name))== 0:                                 #each connected worker check its correspondance queue for the jobs exist or not
		print ("empty")
		connection.sendall("wait".encode("utf8"))                                   #if there is no job, send  'wait' message by Master to that worker
	else:                                                                           #if there are jobs, grab only the first job in its queue
		job = ""
		for entry_name in os.listdir(base_directory+pc_name):
			job = entry_name
			print (entry_name, "Job name")
			break
		path = base_directory+pc_name+"/"
		
		try:                                                                        #for the container needed jobs
			kind = filetype.guess(path+job)
			connection.sendall(job.encode("utf8"))                                  #job name is sent to the worker 
			print ("This job will send soon >>>>>", job)
			sys_name = job.split("_")
			time.sleep(5)                                                           #give some time to the worker for job accept 
			subprocess.call(['python3', '/home/heinhtet/Desktop/UPC_Master/sender.py', base_directory+pc_name+"/"+job, ip])              #job is sent to the worker
			shutil.move(base_directory+'local_user/jobStatus/waiting/'+job, base_directory+'local_user/jobStatus/running/')              #update the web interface for the job state
			subprocess.call(['rm', '-r', base_directory+pc_name+"/"+job])                                                                #sent job is removed from the worker correspondacne queue
			result_alert = connection.recv(5120).decode("utf8")                                                                          #listening the result acknowledge from the worker
			if result_alert=="result":
				print (result_alert, "result..............")
				results_accept(connection, pc_name, "local_user", job)                                                                   #prepare to accept the results
		except IsADirectoryError:                                                                                                        #jobs that are not required to build container
			create_zip = job+".zip"
			#subprocess.call(['zip', '-r', path+create_zip, path])
			shutil.make_archive(base_directory+pc_name+"/"+job, 'zip', base_directory+pc_name+"/"+job)
			subprocess.call(['chmod', '777', '-R', path])
			subprocess.call(['rm', '-r', path+job])
			connection.sendall(create_zip.encode("utf8"))                                                                                #job name is sent to the worker
			print ("This job will send soon >>>>>", create_zip)
			sys_name = job.split("_")
			time.sleep(5)                                                                                                                #give some time to the worker for job accept 
			subprocess.call(['python3', '/home/heinhtet/Desktop/UPC_Master/sender.py', base_directory+pc_name+"/"+job+".zip", ip])       #job is sent to the worker
			shutil.move(base_directory+sys_name[2]+'/jobStatus/waiting/'+job, base_directory+sys_name[2]+'/jobStatus/running/')          #update the web interface for the job state
			subprocess.call(['rm', '-r', base_directory+pc_name+"/"+job+".zip"])                                                         #sent job is removed from the worker correspondacne queue
			result_alert = connection.recv(5120).decode("utf8")                                                                          #listening the result acknowledge from the worker
			if result_alert=="result":
				print (result_alert, "result..............")
				results_accept(connection, pc_name, sys_name[2], job)                                                                    #prepare to accept the results

def results_accept(connection, pc_name, sys_name, name_job):                                                    #to accept the results from the worker
	print ("I will accept the result.")
	subprocess.call(['python3', '/home/heinhtet/Desktop/UPC_Master/receiver.py', sys_name])
	running_directory = '/home/heinhtet/Desktop/UPC_Master/'+sys_name+'/jobStatus/running/'+name_job            #update the web interface and results can be seen under finished directory.
	subprocess.call(['rm', '-r', running_directory])
	
def push_worker(pc):                                                        #workers are pushed to the available woker list
	global available_list
	if pc=="PC1":
		available_list.append("PC1")
	elif pc=="PC2":
		available_list.append("PC2")
	elif pc=="PC3":
		available_list.append("PC3")
	elif pc=="PC4":
		available_list.append("PC4")
	elif pc=="PC5":
		available_list.append("PC5")
	else:
		available_list.append("PC6")

def pop_worker(pc):                                                         #workers are removed from the available worker list
	global available_list
	print (available_list, "pop_worker")
	for worker in range(0, len(available_list)):
		if pc in available_list[worker]:
			if pc=="PC1":
				available_list.remove("PC1")
			elif pc=="PC2":
				available_list.remove("PC2")
			elif pc=="PC3":
				available_list.remove("PC3")
			elif pc=="PC4":
				available_list.remove("PC4")
			elif pc=="PC5":
				available_list.remove("PC5")
			else:
				available_list.remove("PC6")
		else:
			print ("This worker is already not free.")

if __name__ == "__main__":                                                 #Starting point of the program
	main()
