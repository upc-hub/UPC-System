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
import sys
import multiprocessing

global token_counter_today
token_counter_today = 0
global available_list           #current available worker list connected to UPC Master
available_list = []
#global chk_aplas_jobs
#chk_aplas_jobs = []
global csv_file
csv_file = '/home/heinhtet/Desktop/UPC_Master/Sam_pc6_master/ten/thread_proportional_time.csv'

def main():
	Thread(target = master_connection_open).start()             #UPC Master allows connection for the workers
	Thread(target = rename_job).start()
	#while True:
	#	schedule.run_pending()
	#	time.sleep(1)

def master_connection_open():
	#host = "172.28.235.18"
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

def aplas_job_zipping():
	#global chk_aplas_jobs
	chk_aplas_jobs = []
	global token_counter_today
	APLAS_dir = '/home/heinhtet/Desktop/UPC_Master/APLAS/newJobs/'
	APLAS_umount = '/home/heinhtet/Desktop/UPC_Master/aplas_umount/'
	all_job_dir = '/home/heinhtet/Desktop/UPC_Master/temporary_queue/'        #group all submitted jobs from various system
	com_job_dir = '/home/heinhtet/Desktop/UPC_Master/common_queue/'           #renamed all submitted jobs Queue
	for aplas_umount in os.listdir(APLAS_dir):
		shutil.move(APLAS_dir+aplas_umount, APLAS_umount)
		chk_aplas_jobs.append(aplas_umount)

	print ("jobs list", chk_aplas_jobs)

	for file_name in chk_aplas_jobs:
		separate_ext = file_name.split('.')
		file = separate_ext[0]
		extension = separate_ext[1]
		if not os.path.exists(APLAS_umount+file):
			subprocess.call(['mkdir', APLAS_umount+file])
			subprocess.call(['chmod', '777', '-R', APLAS_umount+file])
	#time.sleep(60)
	for file_name1 in chk_aplas_jobs:
		separate_ext1 = file_name1.split('.')
		file1 = separate_ext1[0]
		extension1 = separate_ext1[1]
		print (file1, extension1)
		print ("***********")
		for file_name2 in chk_aplas_jobs:
			separate_ext2 = file_name2.split('.')
			file2 = separate_ext2[0]
			extension2 = separate_ext2[1]
			print (file2, extension2)
			print ("........")
			if file1 == file2:
				if extension1 !=extension2:
					try:
						subprocess.call(['mv', APLAS_umount+file_name1, APLAS_umount+file1])
						subprocess.call(['mv', APLAS_umount+file_name2, APLAS_umount+file1])
						shutil.make_archive(APLAS_umount+file1, 'zip', APLAS_umount+file1)
						subprocess.call(['rm', '-r', APLAS_umount+file1])
						subprocess.call(['chmod', '777', '-R', APLAS_umount+file1+'.zip'])
						#chk_aplas_jobs.remove(file_name1)
						#chk_aplas_jobs.remove(file_name2)
						subprocess.call(['mv', APLAS_umount+file1+'.zip', all_job_dir])
						#time.sleep(5)
					except:
						print ("No job.")
					#print (file1, extension1, extension2)

def rename_job():                                          #submitted jobs are renamed to be compactible with the system requirements e.g. currentToken_ddmmyyyy_jobName
	global token_counter_today
	global available_list
	print ("Currently available worker : ", available_list)
	EPLAS_dir = '/home/heinhtet/Desktop/UPC_Master/EPLAS/newJobs/'            #EPLAS job directory (EPLAS system assigns jobs through pCloud-https)
	APLAS_dir = '/home/heinhtet/Desktop/UPC_Master/APLAS/newJobs/'			  #APLAS job directory (APLAS system assigns jobs through FTP)
	local_dir = '/home/heinhtet/Desktop/UPC_Master/local_user/newJobs/'       #Local user job directory (local user assigns jobs through LAN_static-https)
	all_job_dir = '/home/heinhtet/Desktop/UPC_Master/temporary_queue/'        #group all submitted jobs from various system
	com_job_dir = '/home/heinhtet/Desktop/UPC_Master/common_queue/'           #renamed all submitted jobs Queue
	aplas_job_zipping()
	# detect_aplas = []
	# for file_name in os.listdir(APLAS_dir):
	# 	detect_aplas.append(file_name)
	# print ("file name:", detect_aplas)
	# for filename in detect_aplas:
	# 	namme = filename.split('.')
	# 	nammea = namme[0]
	# 	nammeb = namme[1]
	# 	for filenamea in detect_aplas:
	# 		nammc = filenamea.split('.')
	# 		nammca = nammc[0]
	# 		nammcb = nammc[1]
	# 		if nammea == nammca:
	# 			if nammeb!=nammcb:
	# 				print ("manifest", filename, "zip", filenamea)
	# 				subprocess.call(['mkdir', APLAS_dir+nammea])
	# 				subprocess.call(['chmod', '777', '-R', APLAS_dir+nammea])
	# 				subprocess.call(['mv', APLAS_dir+filename, APLAS_dir+nammea])
	# 				subprocess.call(['mv', APLAS_dir+filenamea, APLAS_dir+nammea])
	# 				#shutil.move(APLAS_dir+filename, APLAS_dir+nammea)
	# 				#shutil.move(APLAS_dir+filenamea, APLAS_dir+nammea)
	# 				shutil.make_archive(APLAS_dir+nammea, 'zip', APLAS_dir+nammea)
	# 				subprocess.call(['rm', '-r', APLAS_dir+nammea])
	# 				subprocess.call(['chmod', '777', '-R', APLAS_dir+nammea+'.zip'])
	# 				break
	# 	#print ("Detect", filename)
	# subprocess.call(['scp', '-r', APLAS_dir+'.', all_job_dir])
	# subprocess.call(['rm', '-r', APLAS_dir])
	####later##subprocess.call(['scp', '-r', local_dir+'.', all_job_dir])
	####later##subprocess.call(['rm', '-r', local_dir])
	####later##subprocess.call(['scp', '-r', EPLAS_dir+'.', all_job_dir])
	####later##try:
	####later##	subprocess.call(['rm', '-r', EPLAS_dir])
	####later##except:
	####later##	print ("No files to move")
	
	for file_name in os.listdir(all_job_dir):
		job_name = str(file_name)
		if (job_name[0].isdigit()):							#check renamed or not
			print ()
		token_counter_today = token_counter_today + 1
		token = initiate_job_token()
		os.rename(os.path.join(all_job_dir, file_name), os.path.join(all_job_dir,token+'_'+file_name))          #renaming process
		shutil.move(all_job_dir+token+'_'+file_name, com_job_dir)											    #renamed jobs are moved to common Queue
		start = total_second()
		zip_extract(token+'_'+file_name, com_job_dir)      													    #extract jobs's zips
		end = total_second()
		job_preparation_time = convert(int(end)-int(start))
		record_csv(csv_file, str(job_preparation_time)+ " job_preparation_time of"+token+'_'+file_name)      													    #extract jobs's zips
	
	check_tick = True
	while check_tick:
		current_total = 0
		for entry_name in os.listdir(APLAS_dir):
			current_total = current_total+1
		if current_total>1:
			time.sleep(5)
			print ("New jobs.")
			check_tick = False
			rename_job()
		else:
			time.sleep(10)
			print ("No new jobs.")
			check_tick=True

#schedule.every(10).seconds.do(rename_job)                  #UPC Master checks jobs arrive from UPC Web Server every 30 seconds

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
	aplas_name_container = zip_name[0].split('-')
	aplas_name_container1 = aplas_name_container[0].split('_')
	if aplas_name_container1[2]=='aplas':
		file_name = directory+job_name
		file_name1 = directory+zip_name[0]
		subprocess.call(['mkdir', file_name1])
		subprocess.call(['mv', file_name, file_name1+'/'])
		file_name2 = file_name1+'/'+job_name
		
		zip_ref = zipfile.ZipFile(file_name2)
		extracted = zip_ref.namelist()
		name_of_job = extracted[0].split('/')
		zip_ref.extractall(file_name1)
		zip_ref.close()
		os.remove(file_name2)
		subprocess.call(['chmod', '777', '-R', file_name1])
		job_dir = directory+zip_name[0]
		check_container_require(zip_name_container[0], job_dir, zip_name[0])
		#os.rename(os.path.join(directory, name_of_job[0]), os.path.join(directory,zip_name[0]))       #extracted zip's name may be different from the renames by the System
		
		print ("APLAS............")
		#os.remove(file_name)
	else:
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
	#print ("zip name", zip_name[0])
	#print ("zip container name", zip_name_container[0])

def check_container_require(zip_name_container, job_dir, sys_name):
	global available_list
	container_queue = '/home/heinhtet/Desktop/UPC_Master/container_queue/'
	common_queue = '/home/heinhtet/Desktop/UPC_Master/common_queue/'
	docker_template = '/home/heinhtet/Desktop/UPC_Master/Dockerfile'               #Dokerfile template if job is necessary to build a container
	base_directory = '/home/heinhtet/Desktop/UPC_Master/'
	detect_system = sys_name.split('_')
	detect_systema = sys_name.split('-')
	detect_systemb = detect_systema[0].split('_')
	local = detect_system[2]
	if(local[0]=='l'):                                                             #differentiate between local and outsider systems
		detect_system[2]='local_user'
	if detect_system[2]=='EPLAS':
		print ("This is the EPLAS. We don't need to check Metadata.")
		subprocess.call(['scp', '-r', common_queue+sys_name, base_directory+detect_system[2]+'/jobStatus/waiting/'])          #after necessary checking, jobs are moved to the waiting queue of correspondance system. It can be seen on Web interface.
		shutil.move(job_dir, container_queue)                              #All checked jobs are reached to the container queue and then, moved to the correspondance worker queue
		available_worker = current_available_worker()                      #checked is there any worker already connected to master before jobs arrived
		if available_worker=="":                                           #if there is no available worker, assign null
			print ()
		else:
			shutil.move(container_queue+str(sys_name), base_directory+str(available_worker))      #if there is a worker for the current job, this job is moved from the container queue to that worker queue 
		#update_job_list(sys_name, available_worker)                                               #record current job and worker's tates
		try:
			print (available_list[0], "<<<<this worker will be poped from the list.")             #If a job is assigned to the worker, that worker is removed from the available worker list.
			pop_worker(available_list[0])
		except IndexError:
			print ()

	elif detect_systemb[2]=="aplas":
		print ("This is the APLAS. We don't need to check Metadata.")
		subprocess.call(['scp', '-r', common_queue+sys_name, base_directory+str(detect_systemb[2]).upper()+'/jobStatus/waiting/'])          #after necessary checking, jobs are moved to the waiting queue of correspondance system. It can be seen on Web interface.
		shutil.make_archive(job_dir, 'zip', job_dir)
		subprocess.call(['rm', '-r', job_dir])
		shutil.move(job_dir+'.zip', container_queue)                              #All checked jobs are reached to the container queue and then, moved to the correspondance worker queue
		subprocess.call(['chmod', '777', '-R', container_queue])
		subprocess.call(['scp', '-r', container_queue+str(sys_name)+'.zip', base_directory+'PC11'])
		subprocess.call(['chmod', '777', '-R', base_directory+'PC11'])
		subprocess.call(['scp', '-r', container_queue+str(sys_name)+'.zip', base_directory+'PC66'])
		subprocess.call(['chmod', '777', '-R', base_directory+'PC66'])
		subprocess.call(['scp', '-r', container_queue+str(sys_name)+'.zip', base_directory+'PC33'])
		subprocess.call(['chmod', '777', '-R', base_directory+'PC33'])
		subprocess.call(['scp', '-r', container_queue+str(sys_name)+'.zip', base_directory+'PC44'])
		subprocess.call(['chmod', '777', '-R', base_directory+'PC44'])
		subprocess.call(['scp', '-r', container_queue+str(sys_name)+'.zip', base_directory+'PC55'])
		subprocess.call(['chmod', '777', '-R', base_directory+'PC55'])
		#subprocess.call(['rm', '-r', container_queue+str(sys_name)+'.zip'])
		available_worker = current_available_worker()                      #checked is there any worker already connected to master before jobs arrived
		if available_worker=="":                                           #if there is no available worker, assign null
			print ()
		else:
			#shutil.move(container_queue+str(sys_name), base_directory+str(available_worker))      #if there is a worker for the current job, this job is moved from the container queue to that worker queue 
		#update_job_list(sys_name, available_worker)                                               #record current job and worker's tates
			try:
				print (available_list[0], "<<<<this worker will be poped from the list.")             #If a job is assigned to the worker, that worker is removed from the available worker list.
				pop_worker(available_list[0])
			except IndexError:
				print ()
		#update_job_list(sys_name, available_worker)

	else:
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
					#update_job_list(sys_name, available_worker)                                               #record current job and worker's tates
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
					#update_job_list(zip_name_container+"_"+p['System_name'].lower(), available_worker)
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
		print (lines, "lines ************************")
		print ("")
		print (len(lines), "length of lines ************************")
		pc1_count = 1
		pc1_limit = 1
		pc3_count = 1
		pc3_limit = 10
		pc4_count = 1
		pc4_limit = 1
		pc5_count = 1
		pc5_limit = 10
		pc6_count = 1
		pc6_limit = 2
		try:
			if pc=="PC4":
				for entry_name in os.listdir(base_directory+'PC44/'):
					if pc4_count>pc4_limit:
						break
					else:
						shutil.move(base_directory+'PC44/'+entry_name, base_directory+"PC4")
						print ('PC44 moved jobs.')
						pc4_count = pc4_count+1
			elif pc=="PC5":
				for entry_name in os.listdir(base_directory+'PC55/'):
					if pc5_count>pc5_limit:
						break
					else:
						shutil.move(base_directory+'PC55/'+entry_name, base_directory+"PC5")
						print ('PC55 moved jobs.')
						pc5_count = pc5_count+1
			elif pc=="PC6":
				for entry_name in os.listdir(base_directory+'PC66/'):
					if pc6_count>pc6_limit:
						break
					else:
						shutil.move(base_directory+'PC66/'+entry_name, base_directory+"PC6")
						pc6_count = pc6_count+1
			elif pc=="PC3":
				for entry_name in os.listdir(base_directory+'PC33/'):
					if pc3_count>pc3_limit:
						break
					else:
						shutil.move(base_directory+'PC33/'+entry_name, base_directory+"PC3")
						pc3_count = pc3_count+1
			elif pc=="PC1":
				for entry_name in os.listdir(base_directory+'PC11/'):
					if pc1_count>pc1_limit:
						break
					else:
						shutil.move(base_directory+'PC11/'+entry_name, base_directory+"PC1")
						pc1_count = pc1_count+1
			else:
				print ("csv file error.........................")

			#subprocess.call(['rm', '-r', base_directory+'PC66/*'])
			#subprocess.call(['rm', '-r', base_directory+'PC55/*'])
			#subprocess.call(['rm', '-r', base_directory+'PC44/*'])
			#subprocess.call(['rm', '-r', base_directory+'PC33/*'])
			#subprocess.call(['rm', '-r', base_directory+'PC11/*'])
			#subprocess.call(['rm', '-r', container_queue+'*'])
			return "aa", "bb"
			# if lines[1][0] == "":
			# 	no_job = "No job"
			# 	no_worker = "No worker"
			# else:                                                                     #if job already added in the status file but there is no worker for this job. (Update that place)
			# 	break_out_flag = False
			# 	for i in range(len(lines)):
			# 		for j in range(len(lines[i])):
			# 			if lines[i][j]=="":
			# 				print (i, 'and', j, 'i and j print...*****************')
			# 				lines[i][j] = available_list[0]
			# 				send_job = lines[i][j-1]
			# 				send_worker = lines[i][j]
			# 				break_out_flag = True
			# 				pop_worker(pc)
			# 				break
			# 			else:
			# 				print ()
			# 		if break_out_flag:
			# 			break

			# 	with open('/home/heinhtet/Desktop/UPC_Master/job_list_status.csv', 'w') as csvfile:
			# 		csvwriter = csv.writer(csvfile)
			# 		csvwriter.writerows(lines)
			# 	print ("There is a job.")
			# 	try:
			# 		shutil.move(container_queue+send_job+'.zip', base_directory+send_worker)                      #Update job is moved to the correspondance worker queue
			# 	except shutil.Error:
			# 		print ()

			# 	return send_job, send_worker

		except IndexError:
			send_job = "No job"
			send_worker = "No worker"
			print ("There is no job.")
			return "aa", send_worker

def check_job_to_execute(connection, ip, pc_name):                               
	container_queue = '/home/heinhtet/Desktop/UPC_Master/container_queue/'
	base_directory = '/home/heinhtet/Desktop/UPC_Master/'
	if len(os.listdir(base_directory+pc_name))== 0:                                 #each connected worker check its correspondance queue for the jobs exist or not
		print ("empty")
		connection.sendall("wait".encode("utf8"))                                   #if there is no job, send  'wait' message by Master to that worker
	else:                                                                           #if there are jobs, grab only the first job in its queue
		aplas_directory = '/home/heinhtet/Desktop/UPC_Master/'+pc_name+'/'
		ip6 = '172.28.235.217'
		ip5 = '172.28.235.214'
		ip4 = '172.28.235.207'
		ip3 = '172.28.235.208'
		ip1 = '172.28.235.203'
		ip = ""
		pc6_limitt = 2
		pc5_limitt = 10
		pc4_limitt = 1
		pc3_limitt = 10
		pc1_limitt = 1
		counter = 0
		current_total = 0
		token_jobs = []
		# for entry_name in os.listdir(container_queue):
		# 	split_name = entry_name.split('-')
		# 	split_name1 = split_name[0].split('_')
		# 	if split_name1[2]=="aplas":
		# 		shutil.move(container_queue+entry_name, aplas_directory)
				
		for entry_name in os.listdir(aplas_directory):
			current_total = current_total+1

		print ("Current total.......................", current_total)
		if pc_name=="PC6" and current_total<pc6_limitt:
			ip = ip6
			for entry_name in os.listdir(aplas_directory):
				token_jobs.append(entry_name)
			print (token_jobs)
		elif pc_name=="PC5" and current_total<pc5_limitt:
			ip = ip5
			for entry_name in os.listdir(aplas_directory):
				token_jobs.append(entry_name)
		elif pc_name=="PC4" and current_total<pc4_limitt:
			ip = ip4
			for entry_name in os.listdir(aplas_directory):
				token_jobs.append(entry_name)
		elif pc_name=="PC3" and current_total<pc3_limitt:
			ip = ip3
			for entry_name in os.listdir(aplas_directory):
				token_jobs.append(entry_name)
		elif pc_name=="PC1" and current_total<pc1_limitt:
			ip = ip1
			for entry_name in os.listdir(aplas_directory):
				token_jobs.append(entry_name)
		else:
			for entry_name in os.listdir(aplas_directory):
				token_jobs.append(entry_name)
				counter = counter+1
				if pc_name=="PC6" and counter==pc6_limitt:
					ip = ip6
					break
				elif pc_name=="PC5" and counter==pc5_limitt:
					ip = ip5
					break
				elif pc_name=="PC4" and counter==pc4_limitt:
					ip = ip4
					break
				elif pc_name=="PC3" and counter==pc3_limitt:
					ip = ip3
					break
				elif pc_name=="PC1" and counter==pc1_limitt:
					ip = ip1
					break
				else:
					print ("Unknown worker......")
			print (token_jobs)

		if len(token_jobs)==1:
			connection.sendall("one".encode("utf8"))
			one_thread(pc_name, connection, aplas_directory, token_jobs[0], ip, pc_name[2]+'004')
		elif len(token_jobs)==2:
			connection.sendall("two".encode("utf8"))
			two_thread(pc_name, connection, aplas_directory, token_jobs[0], token_jobs[1], ip, pc_name[2]+'004', pc_name[2]+'005')
		elif len(token_jobs)==3:
			connection.sendall("three".encode("utf8"))
			three_thread(pc_name, connection, aplas_directory, token_jobs[0], token_jobs[1], token_jobs[2], ip, pc_name[2]+'004', pc_name[2]+'005', pc_name[2]+'006')
		elif len(token_jobs)==4:
			connection.sendall("four".encode("utf8"))
			four_thread(pc_name, connection, aplas_directory, token_jobs[0], token_jobs[1], token_jobs[2], token_jobs[3], ip, pc_name[2]+'004', pc_name[2]+'005', pc_name[2]+'006', pc_name[2]+'007')
		elif len(token_jobs)==5:
			connection.sendall("five".encode("utf8"))
			five_thread(pc_name, connection, aplas_directory, token_jobs[0], token_jobs[1], token_jobs[2], token_jobs[3], token_jobs[4], ip, pc_name[2]+'004', pc_name[2]+'005', pc_name[2]+'006', pc_name[2]+'007', pc_name[2]+'008')
		elif len(token_jobs)==6:
			connection.sendall("six".encode("utf8"))
			six_thread(pc_name, connection, aplas_directory, token_jobs[0], token_jobs[1], token_jobs[2], token_jobs[3], token_jobs[4], token_jobs[5], ip, pc_name[2]+'004', pc_name[2]+'005', pc_name[2]+'006', pc_name[2]+'007', pc_name[2]+'008', pc_name[2]+'009')
		elif len(token_jobs)==7:
			connection.sendall("seven".encode("utf8"))
			seven_thread(pc_name, connection, aplas_directory, token_jobs[0], token_jobs[1], token_jobs[2], token_jobs[3], token_jobs[4], token_jobs[5], token_jobs[6], ip, pc_name[2]+'004', pc_name[2]+'005', pc_name[2]+'006', pc_name[2]+'007', pc_name[2]+'008', pc_name[2]+'009', pc_name[2]+'010')
		elif len(token_jobs)==8:
			connection.sendall("eight".encode("utf8"))
			eight_thread(pc_name, connection, aplas_directory, token_jobs[0], token_jobs[1], token_jobs[2], token_jobs[3], token_jobs[4], token_jobs[5], token_jobs[6], token_jobs[7], ip, pc_name[2]+'004', pc_name[2]+'005', pc_name[2]+'006', pc_name[2]+'007', pc_name[2]+'008', pc_name[2]+'009', pc_name[2]+'010', pc_name[2]+'011')
		elif len(token_jobs)==9:
			connection.sendall("nine".encode("utf8"))
			nine_thread(pc_name, connection, aplas_directory, token_jobs[0], token_jobs[1], token_jobs[2], token_jobs[3], token_jobs[4], token_jobs[5], token_jobs[6], token_jobs[7], token_jobs[8], ip, pc_name[2]+'004', pc_name[2]+'005', pc_name[2]+'006', pc_name[2]+'007', pc_name[2]+'008', pc_name[2]+'009', pc_name[2]+'010', pc_name[2]+'011', pc_name[2]+'012')
		else:
			connection.sendall("ten".encode("utf8"))
			ten_thread(pc_name, connection, aplas_directory, token_jobs[0], token_jobs[1], token_jobs[2], token_jobs[3], token_jobs[4], token_jobs[5], token_jobs[6], token_jobs[7], token_jobs[8], token_jobs[9], ip, pc_name[2]+'004', pc_name[2]+'005', pc_name[2]+'006', pc_name[2]+'007', pc_name[2]+'008', pc_name[2]+'009', pc_name[2]+'010', pc_name[2]+'011', pc_name[2]+'012', pc_name[2]+'013')



		# job = ""
		# for entry_name in os.listdir(base_directory+pc_name):
		# 	job = entry_name
		# 	print (entry_name, "Job name")
		# 	break
		# path = base_directory+pc_name+"/"
		
		# try:                                                                        #for the container needed jobs
		# 	kind = filetype.guess(path+job)
		# 	connection.sendall(job.encode("utf8"))                                  #job name is sent to the worker 
		# 	print ("This container job will send soon >>>>>", job)
		# 	sys_name = job.split("_")
		# 	sys_name1 = job.split("-")
		# 	sys_name2 = sys_name1[0].split("_")
		# 	time.sleep(5)                                                           #give some time to the worker for job accept 
		# 	subprocess.call(['python3', '/home/heinhtet/Desktop/UPC_Master/sender.py', base_directory+pc_name+"/"+job, ip])              #job is sent to the worker
		# 	if sys_name2[2]=="aplas":
		# 		shutil.move(base_directory+'APLAS/jobStatus/waiting/'+job, base_directory+'APLAS/jobStatus/running/')
		# 		subprocess.call(['rm', '-r', base_directory+pc_name+"/"+job])
				
		# 		result_alert = connection.recv(5120).decode("utf8")
		# 		if result_alert=="result":
		# 			print (result_alert, "result.....")
		# 			results_accept(connection, pc_name, "APLAS", job)
		# 	else:
		# 		shutil.move(base_directory+'local_user/jobStatus/waiting/'+job, base_directory+'local_user/jobStatus/running/')              #update the web interface for the job state
		# 		subprocess.call(['rm', '-r', base_directory+pc_name+"/"+job])                                                                #sent job is removed from the worker correspondacne queue
			
		# 		result_alert = connection.recv(5120).decode("utf8")                                                                          #listening the result acknowledge from the worker
		# 		if result_alert=="result":
		# 			print (result_alert, "result..............")
		# 			results_accept(connection, pc_name, "local_user", job)                                                                   #prepare to accept the results
		# except IsADirectoryError:                                                                                                        #jobs that are not required to build container
		# 	create_zip = job+".zip"
		# 	#subprocess.call(['zip', '-r', path+create_zip, path])
		# 	shutil.make_archive(base_directory+pc_name+"/"+job, 'zip', base_directory+pc_name+"/"+job)
		# 	subprocess.call(['chmod', '777', '-R', path])
		# 	subprocess.call(['rm', '-r', path+job])
		# 	connection.sendall(create_zip.encode("utf8"))                                                                                #job name is sent to the worker
		# 	print ("This job will send soon >>>>>", create_zip)
		# 	sys_name = job.split("_")
		# 	time.sleep(5)                                                                                                                #give some time to the worker for job accept 
		# 	subprocess.call(['python3', '/home/heinhtet/Desktop/UPC_Master/sender.py', base_directory+pc_name+"/"+job+".zip", ip])       #job is sent to the worker
		# 	shutil.move(base_directory+sys_name[2]+'/jobStatus/waiting/'+job, base_directory+sys_name[2]+'/jobStatus/running/')          #update the web interface for the job state
		# 	subprocess.call(['rm', '-r', base_directory+pc_name+"/"+job+".zip"])                                                         #sent job is removed from the worker correspondacne queue
		# 	result_alert = connection.recv(5120).decode("utf8")                                                                          #listening the result acknowledge from the worker
		# 	if result_alert=="result":
		# 		print (result_alert, "result..............")
		# 		results_accept(connection, pc_name, sys_name[2], job)                                                                    #prepare to accept the results

def one_thread(pc_name, connection, directory, job1, ip, port1):

	send_one_proce = multiprocessing.Process(target = send_one, args=(connection, directory, job1, ip, port1))
	result1_proce = multiprocessing.Process(target = result1, args=(connection, port1, pc_name))
	send_one_proce.start()
	result1_proce.start()
	#print ("terminate.....................")
	#send_one_proce.terminate()
	#result1_proce.terminate()
	#accept_result(connection, 'one')
	#Thread(target = one, args=(connection, directory,job1,ip,port1)).start()

def two_thread(pc_name, connection, directory, job1, job2, ip, port1, port2):
	send_one_proce = multiprocessing.Process(target = send_one, args=(connection, directory, job1, ip, port1))
	send_two_proce = multiprocessing.Process(target = send_two, args=(connection, directory, job2, ip, port2))
	result1_proce = multiprocessing.Process(target = result1, args=(connection, port1, pc_name))
	result2_proce = multiprocessing.Process(target = result2, args=(connection, port2, pc_name))
	send_one_proce.start()
	#return_val = send_one_proce.join()
	send_two_proce.start()
	result1_proce.start()
	result2_proce.start()
	#time.sleep(50)
	#print ('------------------------------------------------------------------------')
	#print (return_val)
	#print ("terminate.....................")
	#send_one_proce.terminate()
	#send_two_proce.terminate()
	#result1_proce.terminate()
	#result2_proce.terminate()
	#accept_result(connection, 'two')
	#Thread(target = two, args=(connection, directory,job1,job2,ip,port1,port2)).start()

def three_thread(pc_name, connection, directory, job1, job2, job3, ip, port1, port2, port3):
	send_one_proce = multiprocessing.Process(target = send_one, args=(connection, directory, job1, ip, port1))
	send_two_proce = multiprocessing.Process(target = send_two, args=(connection, directory, job2, ip, port2))
	send_three_proce = multiprocessing.Process(target = send_three, args=(connection, directory, job3, ip, port3))
	result1_proce = multiprocessing.Process(target = result1, args=(connection, port1, pc_name))
	result2_proce = multiprocessing.Process(target = result2, args=(connection, port2, pc_name))
	result3_proce = multiprocessing.Process(target = result3, args=(connection, port3, pc_name))
	send_one_proce.start()
	send_two_proce.start()
	send_three_proce.start()
	result1_proce.start()
	result2_proce.start()
	result3_proce.start()
	#print ("terminate.....................")
	#send_one_proce.terminate()
	#send_two_proce.terminate()
	#send_three_proce.terminate()
	#result1_proce.terminate()
	#result2_proce.terminate()
	#result3_proce.terminate()
	#accept_result(connection, 'three')
	#Thread(target = three, args=(connection, directory,job1,job2,job3,ip,port1,port2,port3)).start()

def four_thread(pc_name, connection, directory, job1, job2, job3, job4, ip, port1, port2, port3, port4):
	send_one_proce = multiprocessing.Process(target = send_one, args=(connection, directory, job1, ip, port1))
	send_two_proce = multiprocessing.Process(target = send_two, args=(connection, directory, job2, ip, port2))
	send_three_proce = multiprocessing.Process(target = send_three, args=(connection, directory, job3, ip, port3))
	send_four_proce = multiprocessing.Process(target = send_four, args=(connection, directory, job4, ip, port4))
	result1_proce = multiprocessing.Process(target = result1, args=(connection, port1, pc_name))
	result2_proce = multiprocessing.Process(target = result2, args=(connection, port2, pc_name))
	result3_proce = multiprocessing.Process(target = result3, args=(connection, port3, pc_name))
	result4_proce = multiprocessing.Process(target = result4, args=(connection, port4, pc_name))
	send_one_proce.start()
	send_two_proce.start()
	send_three_proce.start()
	send_four_proce.start()
	result1_proce.start()
	result2_proce.start()
	result3_proce.start()
	result4_proce.start()

def five_thread(pc_name, connection, directory, job1, job2, job3, job4, job5, ip, port1, port2, port3, port4, port5):
	send_one_proce = multiprocessing.Process(target = send_one, args=(connection, directory, job1, ip, port1))
	send_two_proce = multiprocessing.Process(target = send_two, args=(connection, directory, job2, ip, port2))
	send_three_proce = multiprocessing.Process(target = send_three, args=(connection, directory, job3, ip, port3))
	send_four_proce = multiprocessing.Process(target = send_four, args=(connection, directory, job4, ip, port4))
	send_five_proce = multiprocessing.Process(target = send_five, args=(connection, directory, job5, ip, port5))
	result1_proce = multiprocessing.Process(target = result1, args=(connection, port1, pc_name))
	result2_proce = multiprocessing.Process(target = result2, args=(connection, port2, pc_name))
	result3_proce = multiprocessing.Process(target = result3, args=(connection, port3, pc_name))
	result4_proce = multiprocessing.Process(target = result4, args=(connection, port4, pc_name))
	result5_proce = multiprocessing.Process(target = result5, args=(connection, port5, pc_name))
	send_one_proce.start()
	send_two_proce.start()
	send_three_proce.start()
	send_four_proce.start()
	send_five_proce.start()
	result1_proce.start()
	result2_proce.start()
	result3_proce.start()
	result4_proce.start()
	result5_proce.start()

def six_thread(pc_name, connection, directory, job1, job2, job3, job4, job5, job6, ip, port1, port2, port3, port4, port5, port6):
	send_one_proce = multiprocessing.Process(target = send_one, args=(connection, directory, job1, ip, port1))
	send_two_proce = multiprocessing.Process(target = send_two, args=(connection, directory, job2, ip, port2))
	send_three_proce = multiprocessing.Process(target = send_three, args=(connection, directory, job3, ip, port3))
	send_four_proce = multiprocessing.Process(target = send_four, args=(connection, directory, job4, ip, port4))
	send_five_proce = multiprocessing.Process(target = send_five, args=(connection, directory, job5, ip, port5))
	send_six_proce = multiprocessing.Process(target = send_six, args=(connection, directory, job6, ip, port6))
	result1_proce = multiprocessing.Process(target = result1, args=(connection, port1, pc_name))
	result2_proce = multiprocessing.Process(target = result2, args=(connection, port2, pc_name))
	result3_proce = multiprocessing.Process(target = result3, args=(connection, port3, pc_name))
	result4_proce = multiprocessing.Process(target = result4, args=(connection, port4, pc_name))
	result5_proce = multiprocessing.Process(target = result5, args=(connection, port5, pc_name))
	result6_proce = multiprocessing.Process(target = result6, args=(connection, port6, pc_name))
	send_one_proce.start()
	send_two_proce.start()
	send_three_proce.start()
	send_four_proce.start()
	send_five_proce.start()
	send_six_proce.start()
	result1_proce.start()
	result2_proce.start()
	result3_proce.start()
	result4_proce.start()
	result5_proce.start()
	result6_proce.start()

def seven_thread(pc_name, connection, directory, job1, job2, job3, job4, job5, job6, job7, ip, port1, port2, port3, port4, port5, port6, port7):
	send_one_proce = multiprocessing.Process(target = send_one, args=(connection, directory, job1, ip, port1))
	send_two_proce = multiprocessing.Process(target = send_two, args=(connection, directory, job2, ip, port2))
	send_three_proce = multiprocessing.Process(target = send_three, args=(connection, directory, job3, ip, port3))
	send_four_proce = multiprocessing.Process(target = send_four, args=(connection, directory, job4, ip, port4))
	send_five_proce = multiprocessing.Process(target = send_five, args=(connection, directory, job5, ip, port5))
	send_six_proce = multiprocessing.Process(target = send_six, args=(connection, directory, job6, ip, port6))
	send_seven_proce = multiprocessing.Process(target = send_seven, args=(connection, directory, job7, ip, port7))
	result1_proce = multiprocessing.Process(target = result1, args=(connection, port1, pc_name))
	result2_proce = multiprocessing.Process(target = result2, args=(connection, port2, pc_name))
	result3_proce = multiprocessing.Process(target = result3, args=(connection, port3, pc_name))
	result4_proce = multiprocessing.Process(target = result4, args=(connection, port4, pc_name))
	result5_proce = multiprocessing.Process(target = result5, args=(connection, port5, pc_name))
	result6_proce = multiprocessing.Process(target = result6, args=(connection, port6, pc_name))
	result7_proce = multiprocessing.Process(target = result7, args=(connection, port7, pc_name))
	send_one_proce.start()
	send_two_proce.start()
	send_three_proce.start()
	send_four_proce.start()
	send_five_proce.start()
	send_six_proce.start()
	send_seven_proce.start()
	result1_proce.start()
	result2_proce.start()
	result3_proce.start()
	result4_proce.start()
	result5_proce.start()
	result6_proce.start()
	result7_proce.start()

def eight_thread(pc_name, connection, directory, job1, job2, job3, job4, job5, job6, job7, job8, ip, port1, port2, port3, port4, port5, port6, port7, port8):
	send_one_proce = multiprocessing.Process(target = send_one, args=(connection, directory, job1, ip, port1))
	send_two_proce = multiprocessing.Process(target = send_two, args=(connection, directory, job2, ip, port2))
	send_three_proce = multiprocessing.Process(target = send_three, args=(connection, directory, job3, ip, port3))
	send_four_proce = multiprocessing.Process(target = send_four, args=(connection, directory, job4, ip, port4))
	send_five_proce = multiprocessing.Process(target = send_five, args=(connection, directory, job5, ip, port5))
	send_six_proce = multiprocessing.Process(target = send_six, args=(connection, directory, job6, ip, port6))
	send_seven_proce = multiprocessing.Process(target = send_seven, args=(connection, directory, job7, ip, port7))
	send_eight_proce = multiprocessing.Process(target = send_eight, args=(connection, directory, job8, ip, port8))
	result1_proce = multiprocessing.Process(target = result1, args=(connection, port1, pc_name))
	result2_proce = multiprocessing.Process(target = result2, args=(connection, port2, pc_name))
	result3_proce = multiprocessing.Process(target = result3, args=(connection, port3, pc_name))
	result4_proce = multiprocessing.Process(target = result4, args=(connection, port4, pc_name))
	result5_proce = multiprocessing.Process(target = result5, args=(connection, port5, pc_name))
	result6_proce = multiprocessing.Process(target = result6, args=(connection, port6, pc_name))
	result7_proce = multiprocessing.Process(target = result7, args=(connection, port7, pc_name))
	result8_proce = multiprocessing.Process(target = result8, args=(connection, port8, pc_name))
	send_one_proce.start()
	send_two_proce.start()
	send_three_proce.start()
	send_four_proce.start()
	send_five_proce.start()
	send_six_proce.start()
	send_seven_proce.start()
	send_eight_proce.start()
	result1_proce.start()
	result2_proce.start()
	result3_proce.start()
	result4_proce.start()
	result5_proce.start()
	result6_proce.start()
	result7_proce.start()
	result8_proce.start()

def nine_thread(pc_name, connection, directory, job1, job2, job3, job4, job5, job6, job7, job8, job9, ip, port1, port2, port3, port4, port5, port6, port7, port8, port9):
	send_one_proce = multiprocessing.Process(target = send_one, args=(connection, directory, job1, ip, port1))
	send_two_proce = multiprocessing.Process(target = send_two, args=(connection, directory, job2, ip, port2))
	send_three_proce = multiprocessing.Process(target = send_three, args=(connection, directory, job3, ip, port3))
	send_four_proce = multiprocessing.Process(target = send_four, args=(connection, directory, job4, ip, port4))
	send_five_proce = multiprocessing.Process(target = send_five, args=(connection, directory, job5, ip, port5))
	send_six_proce = multiprocessing.Process(target = send_six, args=(connection, directory, job6, ip, port6))
	send_seven_proce = multiprocessing.Process(target = send_seven, args=(connection, directory, job7, ip, port7))
	send_eight_proce = multiprocessing.Process(target = send_eight, args=(connection, directory, job8, ip, port8))
	send_nine_proce = multiprocessing.Process(target = send_nine, args=(connection, directory, job9, ip, port9))
	result1_proce = multiprocessing.Process(target = result1, args=(connection, port1, pc_name))
	result2_proce = multiprocessing.Process(target = result2, args=(connection, port2, pc_name))
	result3_proce = multiprocessing.Process(target = result3, args=(connection, port3, pc_name))
	result4_proce = multiprocessing.Process(target = result4, args=(connection, port4, pc_name))
	result5_proce = multiprocessing.Process(target = result5, args=(connection, port5, pc_name))
	result6_proce = multiprocessing.Process(target = result6, args=(connection, port6, pc_name))
	result7_proce = multiprocessing.Process(target = result7, args=(connection, port7, pc_name))
	result8_proce = multiprocessing.Process(target = result8, args=(connection, port8, pc_name))
	result9_proce = multiprocessing.Process(target = result9, args=(connection, port9, pc_name))
	send_one_proce.start()
	send_two_proce.start()
	send_three_proce.start()
	send_four_proce.start()
	send_five_proce.start()
	send_six_proce.start()
	send_seven_proce.start()
	send_eight_proce.start()
	send_nine_proce.start()
	result1_proce.start()
	result2_proce.start()
	result3_proce.start()
	result4_proce.start()
	result5_proce.start()
	result6_proce.start()
	result7_proce.start()
	result8_proce.start()
	result9_proce.start()

def ten_thread(pc_name, connection, directory, job1, job2, job3, job4, job5, job6, job7, job8, job9, job10, ip, port1, port2, port3, port4, port5, port6, port7, port8, port9, port10):
	send_one_proce = multiprocessing.Process(target = send_one, args=(connection, directory, job1, ip, port1))
	send_two_proce = multiprocessing.Process(target = send_two, args=(connection, directory, job2, ip, port2))
	send_three_proce = multiprocessing.Process(target = send_three, args=(connection, directory, job3, ip, port3))
	send_four_proce = multiprocessing.Process(target = send_four, args=(connection, directory, job4, ip, port4))
	send_five_proce = multiprocessing.Process(target = send_five, args=(connection, directory, job5, ip, port5))
	send_six_proce = multiprocessing.Process(target = send_six, args=(connection, directory, job6, ip, port6))
	send_seven_proce = multiprocessing.Process(target = send_seven, args=(connection, directory, job7, ip, port7))
	send_eight_proce = multiprocessing.Process(target = send_eight, args=(connection, directory, job8, ip, port8))
	send_nine_proce = multiprocessing.Process(target = send_nine, args=(connection, directory, job9, ip, port9))
	send_ten_proce = multiprocessing.Process(target = send_ten, args=(connection, directory, job10, ip, port10))
	result1_proce = multiprocessing.Process(target = result1, args=(connection, port1, pc_name))
	result2_proce = multiprocessing.Process(target = result2, args=(connection, port2, pc_name))
	result3_proce = multiprocessing.Process(target = result3, args=(connection, port3, pc_name))
	result4_proce = multiprocessing.Process(target = result4, args=(connection, port4, pc_name))
	result5_proce = multiprocessing.Process(target = result5, args=(connection, port5, pc_name))
	result6_proce = multiprocessing.Process(target = result6, args=(connection, port6, pc_name))
	result7_proce = multiprocessing.Process(target = result7, args=(connection, port7, pc_name))
	result8_proce = multiprocessing.Process(target = result8, args=(connection, port8, pc_name))
	result9_proce = multiprocessing.Process(target = result9, args=(connection, port9, pc_name))
	result10_proce = multiprocessing.Process(target = result10, args=(connection, port10, pc_name))
	send_one_proce.start()
	send_two_proce.start()
	send_three_proce.start()
	send_four_proce.start()
	send_five_proce.start()
	send_six_proce.start()
	send_seven_proce.start()
	send_eight_proce.start()
	send_nine_proce.start()
	send_ten_proce.start()
	result1_proce.start()
	result2_proce.start()
	result3_proce.start()
	result4_proce.start()
	result5_proce.start()
	result6_proce.start()
	result7_proce.start()
	result8_proce.start()
	result9_proce.start()
	result10_proce.start()
	#print ('------------------------------------------------------------------------')
	#print (send_one_proce.result)
	#print ("terminate.....................")
	#send_one_proce.terminate()
	#send_two_proce.terminate()
	#send_three_proce.terminate()
	#send_four_proce.terminate()
	#result1_proce.terminate()
	#result2_proce.terminate()
	#result3_proce.terminate()
	#result4_proce.terminate()
	#accept_result(connection, 'four')
	#Thread(target = four, args=(connection, directory,job1,job2,job3,job4,ip,port1,port2,port3,port4)).start()

# def one(connection, directory,job1,ip,port1):
# 	subprocess.call(['python3', 'sender1.py', directory+job1, ip, port1])
# 	accept_result(connection, 'one')

# def two(connection, directory,job1,job2,ip,port1,port2):
# 	subprocess.call(['python3', 'sender1.py', directory+job1, ip, port1])
# 	subprocess.call(['python3', 'sender1.py', directory+job2, ip, port2])
# 	accept_result(connection, 'two')

# def three(connection, directory,job1,job2,job3,ip,port1,port2,port3):
# 	subprocess.call(['python3', 'sender1.py', directory+job1, ip, port1])
# 	subprocess.call(['python3', 'sender1.py', directory+job2, ip, port2])
# 	subprocess.call(['python3', 'sender1.py', directory+job3, ip, port3])
# 	accept_result(connection, 'three')

# def four(connection, directory,job1,job2,job3,job4,ip,port1,port2,port3,port4):
# 	subprocess.call(['python3', 'sender1.py', directory+job1, ip, port1])
# 	subprocess.call(['python3', 'sender1.py', directory+job2, ip, port2])
# 	subprocess.call(['python3', 'sender1.py', directory+job3, ip, port3])
# 	subprocess.call(['python3', 'sender1.py', directory+job4, ip, port4])
# 	accept_result(connection, 'four')
def record_csv(csv_file, data):
	with open(csv_file, 'a')as csvfile:
		csvwriter = csv.writer(csvfile)
		csvwriter.writerow([data])

def total_second():
    start_total = (datetime.datetime.now().hour*3600)+(datetime.datetime.now().minute*60)+datetime.datetime.now().second
    start_time = str(datetime.datetime.now().hour)+":"+str(datetime.datetime.now().minute)+":"+str(datetime.datetime.now().second)
    start_date = str(datetime.datetime.now().day)+"/"+str(datetime.datetime.now().month)+"/"+str(datetime.datetime.now().year)
    return start_total

def convert(seconds): 
    min, sec = divmod(seconds, 60) 
    hour, min = divmod(min, 60) 
    return "%d(h):%02d(m):%02d(s)" % (hour, min, sec)

def send_one(connection, directory, job1, ip, port1):
	global csv_file
	start = total_second()
	time.sleep(5)
	subprocess.call(['python3', 'sender1.py', directory+job1, ip, port1])
	end = total_second()
	send = convert(int(end)-int(start))
	record_csv(csv_file, send+ ' Thread-1 job sending time --->'+job1)
	subprocess.call(['rm', '-r', directory+job1])

def send_two(connection, directory, job2, ip, port2):
	global csv_file
	start = total_second()
	time.sleep(5)
	subprocess.call(['python3', 'sender1.py', directory+job2, ip, port2])
	end = total_second()
	send = convert(int(end)-int(start))
	record_csv(csv_file, send+ ' Thread-2 job sending time --->'+job2)
	subprocess.call(['rm', '-r', directory+job2])

def send_three(connection, directory, job3, ip, port3):
	global csv_file
	start = total_second()
	subprocess.call(['python3', 'sender1.py', directory+job3, ip, port3])
	end = total_second()
	send = convert(int(end)-int(start))
	record_csv(csv_file, send+ ' Thread-3 job sending time --->'+job3)
	subprocess.call(['rm', '-r', directory+job3])

def send_four(connection, directory, job4, ip, port4):
	global csv_file
	start = total_second()
	subprocess.call(['python3', 'sender1.py', directory+job4, ip, port4])
	end = total_second()
	send = convert(int(end)-int(start))
	record_csv(csv_file, send+ ' Thread-4 job sending time --->'+job4)
	subprocess.call(['rm', '-r', directory+job4])

def send_five(connection, directory, job5, ip, port5):
	global csv_file
	start = total_second()
	subprocess.call(['python3', 'sender1.py', directory+job5, ip, port5])
	end = total_second()
	send = convert(int(end)-int(start))
	record_csv(csv_file, send+ ' Thread-5 job sending time --->'+job5)
	subprocess.call(['rm', '-r', directory+job5])

def send_six(connection, directory, job6, ip, port6):
	global csv_file
	start = total_second()
	subprocess.call(['python3', 'sender1.py', directory+job6, ip, port6])
	end = total_second()
	send = convert(int(end)-int(start))
	record_csv(csv_file, send+ ' Thread-6 job sending time --->'+job6)
	subprocess.call(['rm', '-r', directory+job6])

def send_seven(connection, directory, job7, ip, port7):
	global csv_file
	start = total_second()
	subprocess.call(['python3', 'sender1.py', directory+job7, ip, port7])
	end = total_second()
	send = convert(int(end)-int(start))
	record_csv(csv_file, send+ ' Thread-7 job sending time --->'+job7)
	subprocess.call(['rm', '-r', directory+job7])

def send_eight(connection, directory, job8, ip, port8):
	global csv_file
	start = total_second()
	subprocess.call(['python3', 'sender1.py', directory+job8, ip, port8])
	end = total_second()
	send = convert(int(end)-int(start))
	record_csv(csv_file, send+ ' Thread-8 job sending time --->'+job8)
	subprocess.call(['rm', '-r', directory+job8])

def send_nine(connection, directory, job9, ip, port9):
	global csv_file
	start = total_second()
	subprocess.call(['python3', 'sender1.py', directory+job9, ip, port9])
	end = total_second()
	send = convert(int(end)-int(start))
	record_csv(csv_file, send+ ' Thread-9 job sending time --->'+job9)
	subprocess.call(['rm', '-r', directory+job9])

def send_ten(connection, directory, job10, ip, port10):
	global csv_file
	start = total_second()
	subprocess.call(['python3', 'sender1.py', directory+job10, ip, port10])
	end = total_second()
	send = convert(int(end)-int(start))
	record_csv(csv_file, send+ ' Thread-10 job sending time --->'+job10)
	subprocess.call(['rm', '-r', directory+job10])


def accept_result(connection, number):
	if number=='one':
		result_one(connection)
	elif number=='two':
		result_two(connection)
	elif number=='three':
		result_three(connection)
	else:
		result_four(connection)
	

def result_one(connection):
	Thread(target = result1, args=(connection, 'aa')).start()

def result_two(connection):
	Thread(target = result1, args=(connection, 'aa')).start()
	Thread(target = result2, args=(connection, 'aa')).start()

def result_three(connection):
	Thread(target = result1, args=(connection, 'aa')).start()
	Thread(target = result2, args=(connection, 'aa')).start()
	Thread(target = result3, args=(connection, 'aa')).start()

def result_four(connection):
	Thread(target = result1, args=(connection, 'aa')).start()
	Thread(target = result2, args=(connection, 'aa')).start()
	Thread(target = result3, args=(connection, 'aa')).start()
	Thread(target = result4, args=(connection, 'aa')).start()

def result_five(connection):
	Thread(target = result1, args=(connection, 'aa')).start()
	Thread(target = result2, args=(connection, 'aa')).start()
	Thread(target = result3, args=(connection, 'aa')).start()
	Thread(target = result4, args=(connection, 'aa')).start()
	Thread(target = result5, args=(connection, 'aa')).start()

def result_six(connection):
	Thread(target = result1, args=(connection, 'aa')).start()
	Thread(target = result2, args=(connection, 'aa')).start()
	Thread(target = result3, args=(connection, 'aa')).start()
	Thread(target = result4, args=(connection, 'aa')).start()
	Thread(target = result5, args=(connection, 'aa')).start()
	Thread(target = result6, args=(connection, 'aa')).start()

def result_seven(connection):
	Thread(target = result1, args=(connection, 'aa')).start()
	Thread(target = result2, args=(connection, 'aa')).start()
	Thread(target = result3, args=(connection, 'aa')).start()
	Thread(target = result4, args=(connection, 'aa')).start()
	Thread(target = result5, args=(connection, 'aa')).start()
	Thread(target = result6, args=(connection, 'aa')).start()
	Thread(target = result7, args=(connection, 'aa')).start()

def result_eight(connection):
	Thread(target = result1, args=(connection, 'aa')).start()
	Thread(target = result2, args=(connection, 'aa')).start()
	Thread(target = result3, args=(connection, 'aa')).start()
	Thread(target = result4, args=(connection, 'aa')).start()
	Thread(target = result5, args=(connection, 'aa')).start()
	Thread(target = result6, args=(connection, 'aa')).start()
	Thread(target = result7, args=(connection, 'aa')).start()
	Thread(target = result8, args=(connection, 'aa')).start()

def result_nine(connection):
	Thread(target = result1, args=(connection, 'aa')).start()
	Thread(target = result2, args=(connection, 'aa')).start()
	Thread(target = result3, args=(connection, 'aa')).start()
	Thread(target = result4, args=(connection, 'aa')).start()
	Thread(target = result5, args=(connection, 'aa')).start()
	Thread(target = result6, args=(connection, 'aa')).start()
	Thread(target = result7, args=(connection, 'aa')).start()
	Thread(target = result8, args=(connection, 'aa')).start()
	Thread(target = result9, args=(connection, 'aa')).start()

def result_ten(connection):
	Thread(target = result1, args=(connection, 'aa')).start()
	Thread(target = result2, args=(connection, 'aa')).start()
	Thread(target = result3, args=(connection, 'aa')).start()
	Thread(target = result4, args=(connection, 'aa')).start()
	Thread(target = result5, args=(connection, 'aa')).start()
	Thread(target = result6, args=(connection, 'aa')).start()
	Thread(target = result7, args=(connection, 'aa')).start()
	Thread(target = result8, args=(connection, 'aa')).start()
	Thread(target = result9, args=(connection, 'aa')).start()
	Thread(target = result10, args=(connection, 'aa')).start()

def result1(connection, aa, pc_name):
	#result_alert = connection.recv(5120).decode("utf8")
	print ("5004...........")
	#if result_alert=='5004':
	#connection.sendall("ready".encode("utf8"))
	subprocess.call(['python3', '/home/heinhtet/Desktop/UPC_Master/thread_receiver.py', 'Thread_results/'+pc_name+'/', aa])

def result2(connection, aa, pc_name):
	#result_alert = connection.recv(5120).decode("utf8")
	print ("5005...........")
	#if result_alert=='5005':
	#connection.sendall("ready".encode("utf8"))
	subprocess.call(['python3', '/home/heinhtet/Desktop/UPC_Master/thread_receiver.py', 'Thread_results/'+pc_name+'/', aa])

def result3(connection, aa, pc_name):
	#result_alert = connection.recv(5120).decode("utf8")
	print ("5006...........")
	#if result_alert=='5006':
	#connection.sendall("ready".encode("utf8"))
	subprocess.call(['python3', '/home/heinhtet/Desktop/UPC_Master/thread_receiver.py', 'Thread_results/'+pc_name+'/', aa])

def result4(connection, aa, pc_name):
	#result_alert = connection.recv(5120).decode("utf8")
	print ("5007...........")
	#if result_alert=='5007':
	#connection.sendall("ready".encode("utf8"))
	subprocess.call(['python3', '/home/heinhtet/Desktop/UPC_Master/thread_receiver.py', 'Thread_results/'+pc_name+'/', aa])

def result5(connection, aa, pc_name):
	print ("5008...........")
	subprocess.call(['python3', '/home/heinhtet/Desktop/UPC_Master/thread_receiver.py', 'Thread_results/'+pc_name+'/', aa])

def result6(connection, aa, pc_name):
	print ("5009...........")
	subprocess.call(['python3', '/home/heinhtet/Desktop/UPC_Master/thread_receiver.py', 'Thread_results/'+pc_name+'/', aa])

def result7(connection, aa, pc_name):
	print ("5010...........")
	subprocess.call(['python3', '/home/heinhtet/Desktop/UPC_Master/thread_receiver.py', 'Thread_results/'+pc_name+'/', aa])

def result8(connection, aa, pc_name):
	print ("5011...........")
	subprocess.call(['python3', '/home/heinhtet/Desktop/UPC_Master/thread_receiver.py', 'Thread_results/'+pc_name+'/', aa])

def result9(connection, aa, pc_name):
	print ("5012...........")
	subprocess.call(['python3', '/home/heinhtet/Desktop/UPC_Master/thread_receiver.py', 'Thread_results/'+pc_name+'/', aa])

def result10(connection, aa, pc_name):
	print ("5013...........")
	subprocess.call(['python3', '/home/heinhtet/Desktop/UPC_Master/thread_receiver.py', 'Thread_results/'+pc_name+'/', aa])


def results_accept(connection, pc_name, sys_name, name_job):                                                    #to accept the results from the worker
	print ("I will accept the result.")
	subprocess.call(['python3', '/home/heinhtet/Desktop/UPC_Master/receiver.py', sys_name])
	running_directory = '/home/heinhtet/Desktop/UPC_Master/'+sys_name+'/jobStatus/running/'+name_job            #update the web interface and results can be seen under finished directory.
	subprocess.call(['rm', '-r', running_directory])
	extract_dir = '/home/heinhtet/Desktop/UPC_Master/'+sys_name+'/jobStatus/finished/'
	result_dir = '/home/heinhtet/Desktop/UPC_Master/'+sys_name+'/results/'
	for extract_name in os.listdir(extract_dir):
			extract_split = extract_name.split('_')
			#extract_splita = extract_split[0]
			if extract_split[2]=="EPLAS":
				extract_zip_EPLAS(extract_name, extract_dir)
				subprocess.call(['rm', '-r', extract_dir+extract_name])
				break
	for extract_name in os.listdir(extract_dir):
		shutil.move(extract_dir+extract_name, result_dir)


def extract_zip_EPLAS(name_of_job, directory):
	file_name = directory+name_of_job
	zip_ref = zipfile.ZipFile(file_name)
	extracted = zip_ref.namelist()
	job_name_extract = extracted[0].split('/')
	zip_ref.extractall(directory)
	zip_ref.close()
		
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