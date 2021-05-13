import shutil
import datetime
import time
import os, zipfile
import subprocess
import socket
import sys
from threading import Thread
import traceback
import time
import csv
import re

def main():
	global measurement
	global pc1_count
	pc1_count = 0
	global pc2_count
	pc2_count = 0
	global pc3_count
	pc3_count = 0
	global pc4_count
	pc4_count = 0
	global pc6_count
	pc6_count = 0
	measurement = '/home/heinhtet/Desktop/Systematic-1/new_complete/migrate/conduct_measurement1.csv'
	start_server_new()

def start_server_new():
	directory = '/home/heinhtet/Desktop/Systematic-1/new_complete/remove_zip/'
	host = "192.168.56.100"
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

	directorya = '/home/heinhtet/Desktop/Systematic-1/new_complete/'
	
	worker_names1 = []
	global my_dict
	with open('/home/heinhtet/Desktop/Systematic-1/new_complete/assign12.csv') as f:
		reader = csv.reader(f)
		next(reader, None)
		for row in reader:
			worker_names1.append(row[0])
	mylist = list( dict.fromkeys(worker_names1) )
	my_dict = {i:worker_names1.count(i) for i in worker_names1}
	print ('mylist', mylist)
	print ('mydict', my_dict)
	print (my_dict[mylist[0]])

	global pc1
	global pc2
	global pc3
	global pc4
	global pc6

	global cc1
	global cc2
	global cc3
	global cc4
	global cc6
	pc6 = directorya+"PC6/"
	pc4 = directorya+"PC4/"
	pc3 = directorya+"PC3/"
	pc2 = directorya+"PC2/"
	pc1 = directorya+"PC1/"
	pc1_chk = directorya+"PC1_c/"
	pc2_chk = directorya+"PC2_c/"
	pc3_chk = directorya+"PC3_c/"
	pc4_chk = directorya+"PC4_c/"
	pc6_chk = directorya+"PC6_c/"

	#cc6 = my_dict["PC6"]
	#cc4 = my_dict["PC4"]
	#cc3 = my_dict["PC3"]
	#cc2 = my_dict["PC2"]
	#cc1 = my_dict["PC1"]


	subprocess.call(['mkdir', pc6, pc4, pc3, pc2, pc1, pc1_chk, pc2_chk, pc3_chk, pc4_chk, pc6_chk])
	subprocess.call(['chmod', '777', '-R', pc6, pc4, pc3, pc2, pc1, pc1_chk, pc2_chk, pc3_chk, pc4_chk, pc6_chk])

	#for assign in mylist:
	#	subprocess.call(['mkdir', directorya+assign])
	#	subprocess.call(['chmod', '777', '-R', directorya+assign])

	for assign in mylist:
		up_to = my_dict[assign]
		flag = 1
		with open('/home/heinhtet/Desktop/Systematic-1/new_complete/assign12.csv') as f:
			reader = csv.reader(f)
			next(reader, None)
			for row in reader:
				if assign==row[0]:
					print (my_dict[assign], row[1])
					#subprocess.call(['mkdir', row[1]])
					#subprocess.call(['chmod', '777', '-R', directory+row[1]])
					shutil.move(directory+row[1],directorya)
					new_name = str(flag)+'_'+row[1]
					os.rename(os.path.join(directorya, row[1]), os.path.join(directorya,new_name))
					shutil.move(directorya+new_name,directorya+row[0])
					flag =  flag+1

	
	print ("UPC Master is now listening the workers")
	print ("-------------------------------------")
	while True:
		connection, address = soc.accept()
		ip, port = str(address[0]), str(address[1])
		print ("-------------------------------------")
		print ("A worker node connected with "+ip+" : "+port)

		time.sleep(5)
		pc_name = connection.recv(5120).decode("utf8")  #very first receive(PC_Name)
		if (pc_name=="PC1"):
			try:
				global pc1_count
				pc1_count = pc1_count+1
				Thread(target=client_thread_newa, args=(connection, ip, port, pc1, pc1_count, pc_name)).start()
			except:
				print ("Thread could not start.")
				traceback.print_exc()

		elif (pc_name=="PC2"):
			try:
				global pc2_count
				pc2_count = pc2_count+1
				Thread(target=client_thread_newa, args=(connection, ip, port, pc2, pc2_count,pc_name)).start()
			except:
				print ("Thread could not start.")
				traceback.print_exc()

		elif (pc_name=="PC3"):
			try:
				global pc3_count
				pc3_count = pc3_count+1
				Thread(target=client_thread_newa, args=(connection, ip, port, pc3, pc3_count,pc_name)).start()
			except:
				print ("Thread could not start.")
				traceback.print_exc()

		elif (pc_name=="PC4"):
			try:
				global pc4_count
				pc4_count = pc4_count+1
				Thread(target=client_thread_newa, args=(connection, ip, port, pc4, pc4_count,pc_name)).start()
			except:
				print ("Thread could not start.")
				traceback.print_exc()

		elif (pc_name=="PC6"):
			try:
				global pc6_count
				pc6_count = pc6_count+1
				Thread(target=client_thread_newa, args=(connection, ip, port, pc6, pc6_count,pc_name)).start()
			except:
				print ("Thread could not start.")
				traceback.print_exc()
		elif (pc_name=="PC1_c"):
			try:
				Thread(target=client_thread_new, args=(connection, ip, port, pc1_chk,pc_name)).start()
			except:
				print ("Thread could not start.")
				traceback.print_exc()

		elif (pc_name=="PC2_c"):
			try:
				Thread(target=client_thread_new, args=(connection, ip, port, pc2_chk,pc_name)).start()
			except:
				print ("Thread could not start.")
				traceback.print_exc()
		elif (pc_name=="PC3_c"):
			try:
				Thread(target=client_thread_new, args=(connection, ip, port, pc3_chk,pc_name)).start()
			except:
				print ("Thread could not start.")
				traceback.print_exc()
		elif (pc_name=="PC4_c"):
			try:
				Thread(target=client_thread_new, args=(connection, ip, port, pc4_chk,pc_name)).start()
			except:
				print ("Thread could not start.")
				traceback.print_exc()
		elif (pc_name=="PC6_c"):
			try:
				Thread(target=client_thread_new, args=(connection, ip, port, pc6_chk,pc_name)).start()
			except:
				print ("Thread could not start.")
				traceback.print_exc()
		else:
			print ("There is no job remaining.")
	soc.close()

def client_thread_new(connection, ip, port, directory,pc_name, max_buffer_size = 5120):
	lista = os.listdir(directory)
	if (len(lista)==0):
		connection.sendall("check".encode("utf8"))
		print ("There is no checkpoint job and so, it is waiting.")
	else:
		for jobs in os.listdir(directory):
			aa = jobs.split("_")
			if (len(aa)==1):
				connection.sendall("check".encode("utf8"))
			else:
				connection.sendall("data".encode("utf8"))
				send_receive_jobs_new(connection, ip, port, directory, pc_name)

def client_thread_newa(connection, ip, port, directory, pc_count, pc_name, max_buffer_size = 5120):
	for jobs in os.listdir(directory):
		aa = jobs.split("_")
		if (len(aa)==1):
			connection.sendall("check".encode("utf8"))
		else:
			connection.sendall("data".encode("utf8"))
			send_receive_jobs_newa(connection, ip, port, directory, pc_count, pc_name)

def send_receive_jobs_new(connection, ip, port, directory, pc_name):
	for jobs in os.listdir(directory):
		connection.sendall(str(jobs).encode("utf8"))
		time.sleep(5)
		s4 = start()
		subprocess.call(['python3', '/home/heinhtet/Desktop/Systematic-1/sender.py', directory+jobs, ip])
		e4 = end()
		with open(measurement, 'a') as csvfile:
			csvwriter = csv.writer(csvfile)
			csvwriter.writerow(["------------------------------------"])
			
			csvwriter.writerow(["Start-transfer time of "+jobs+" is "+convert(int(s4))+" to "+pc_name])
			csvwriter.writerow(["End-transfer time of "+jobs+" is "+convert(int(e4))+" to "+pc_name])
			csvwriter.writerow(["How long job transmission time of "+jobs+"from master to "+pc_name+" is "+convert(int(e4)-int(s4))])
			#csvwriter.writerow(["------------------------------------"])
		
		foldName = connection.recv(5120).decode("utf8")
		time.sleep(5)
		nn = connection.recv(5120).decode("utf8")
		time.sleep(5)
		done_percent = connection.recv(5120).decode("utf8")
		if(foldName==jobs):
			
			print ("Receive from worker:"+foldName)
			os.remove(str(directory+foldName))
			dirName = directory+foldName+"/"
			os.makedirs(dirName)
			subprocess.call(['chmod', '777', '-R', dirName])
			s5 = start()
			print ("Files count:", nn)
			time.sleep(5)

			for account in range(int(nn)):
				filees_name = connection.recv(5120).decode("utf8")
				time.sleep(5)
				with open(dirName+filees_name, 'wb')as f:
					datta = connection.recv(5120)
					time.sleep(5)
					if not datta:
						f.close()
						print ("File is closed.")
					f.write(datta)
				print ("Successfully get the file.")
				time.sleep(5)
			e5 = end()
			with open(measurement, 'a') as csvfile:
				csvwriter = csv.writer(csvfile)
				csvwriter.writerow(["------------------------------------"])
				csvwriter.writerow(["Start-receiving time of final result "+str(foldName)+" is "+convert(int(s5))+" from "+pc_name])
				csvwriter.writerow(["End-receiving time of final result "+str(foldName)+" is "+convert(int(e5))+" from "+pc_name])
				csvwriter.writerow(["How long job receiving time of final result "+str(foldName)+"from "+pc_name+"to master is "+convert(int(e5)-int(s5))])
				#csvwriter.writerow(["Receiving time of successfully finished job - "+str(foldName)+" from worker "+pc_name+" is "+convert(int(rer))])
				csvwriter.writerow(["Number of final result received files - "+str(nn)])
				#csvwriter.writerow(["------------------------------------"])
		else:
			print ("Receive from worker checkpoint file (unfinished):"+foldName)
			#print ("Possible worker with such job:"+nn)
			print ("done percentage of job- "+nn+" is "+done_percent+"%")
			time.sleep(5)
			#new_pc1 = '/home/heinhtet/Desktop/Systematic-1/new_complete/'+pc_name+'_c/'
			#new_pc2 = '/home/heinhtet/Desktop/Systematic-1/new_complete/PC2/'
			#new_pc3 = '/home/heinhtet/Desktop/Systematic-1/new_complete/PC3/'
			#new_pc4 = '/home/heinhtet/Desktop/Systematic-1/new_complete/PC4/'
			#new_pc6 = '/home/heinhtet/Desktop/Systematic-1/new_complete/PC6/'
			#shutil.copy(new_pc1+foldName, new_pc2)
			#shutil.copy(new_pc1+foldName, new_pc3)
			#shutil.copy(new_pc1+foldName, new_pc4)
			#shutil.copy(new_pc1+foldName, new_pc6)
			os.remove(str(directory+jobs))
			dirName = directory+nn+"/"
			os.makedirs(dirName)
			subprocess.call(['chmod', '777', '-R', dirName])
			s6 = start()
			files_count = connection.recv(5120).decode("utf8")
			print ("Files count:", files_count)
			time.sleep(5)

			for account in range(int(files_count)):
				filees_name = connection.recv(5120).decode("utf8")
				time.sleep(5)
				with open(dirName+filees_name, 'wb')as f:
					datta = connection.recv(5120)
					time.sleep(5)
					if not datta:
						f.close()
						print ("File is closed.")
					f.write(datta)
				print ("Successfully get the file.")
				time.sleep(5)
			e6 = end()
			with open(measurement, 'a') as csvfile:
				csvwriter = csv.writer(csvfile)
				csvwriter.writerow(["------------------------------------"])
				csvwriter.writerow(["Start-receiving time of unfinished result "+str(foldName)+" is "+convert(int(s6))+" from "+pc_name])
				csvwriter.writerow(["End-receiving time of unfinished result "+str(foldName)+" is "+convert(int(e6))+" from "+pc_name])
				csvwriter.writerow(["How long job receiving time of unfinished result "+str(foldName)+"from "+pc_name+"to master is "+convert(int(e6)-int(s6))])
				#csvwriter.writerow(["Receiving time of successfully finished job - "+str(foldName)+" from worker "+pc_name+" is "+convert(int(rer))])
				#csvwriter.writerow(["Number of final result received files - "+str(nn)])
			back_data = connection.recv(5120).decode("utf8")
			if "finish" in back_data:
				print ("Check is there any other jobs")
				time.sleep(5)
				connection.close()
				exit()
def send_receive_jobs_newa(connection, ip, port, directory, pc_count, pc_name):
	print ("PC count", pc_count)
	for jobs in os.listdir(directory):
		data = jobs.split("_")
		if (data[0]==str(pc_count)):
			connection.sendall(str(jobs).encode("utf8"))
			time.sleep(5)
			s4 = start()
			subprocess.call(['python3', '/home/heinhtet/Desktop/Systematic-1/sender.py', directory+jobs, ip])
			e4 = end()
			with open(measurement, 'a') as csvfile:
				csvwriter = csv.writer(csvfile)
				csvwriter.writerow(["------------------------------------"])
				
				csvwriter.writerow(["Start-transfer time of "+jobs+" is "+convert(int(s4))+" to "+pc_name])
				csvwriter.writerow(["End-transfer time of "+jobs+" is "+convert(int(e4))+" to "+pc_name])
				csvwriter.writerow(["How long job transmission time of "+jobs+"from master to "+pc_name+" is "+convert(int(e4)-int(s4))])
				#csvwriter.writerow(["------------------------------------"])
			
			foldName = connection.recv(5120).decode("utf8")
			time.sleep(5)
			nn = connection.recv(5120).decode("utf8")
			time.sleep(5)
			done_percent = connection.recv(5120).decode("utf8")
			if(foldName==jobs):
				
				print ("Receive from worker:"+foldName)
				os.remove(str(directory+foldName))
				dirName = directory+foldName+"/"
				os.makedirs(dirName)
				subprocess.call(['chmod', '777', '-R', dirName])
				s5 = start()
				print ("Files count:", nn)
				time.sleep(5)

				for account in range(int(nn)):
					filees_name = connection.recv(5120).decode("utf8")
					time.sleep(5)
					with open(dirName+filees_name, 'wb')as f:
						datta = connection.recv(5120)
						time.sleep(5)
						if not datta:
							f.close()
							print ("File is closed.")
						f.write(datta)
					print ("Successfully get the file.")
					time.sleep(5)
				e5 = end()
				with open(measurement, 'a') as csvfile:
					csvwriter = csv.writer(csvfile)
					csvwriter.writerow(["------------------------------------"])
					csvwriter.writerow(["Start-receiving time of final result "+str(foldName)+" is "+convert(int(s5))+" from "+pc_name])
					csvwriter.writerow(["End-receiving time of final result "+str(foldName)+" is "+convert(int(e5))+" from "+pc_name])
					csvwriter.writerow(["How long job receiving time of final result "+str(foldName)+"from "+pc_name+"to master is "+convert(int(e5)-int(s5))])
					#csvwriter.writerow(["Receiving time of successfully finished job - "+str(foldName)+" from worker "+pc_name+" is "+convert(int(rer))])
					csvwriter.writerow(["Number of final result received files - "+str(nn)])
					#csvwriter.writerow(["------------------------------------"])
			else:
				print ("Receive from worker checkpoint file (unfinished):"+foldName)
				#print ("Possible worker with such job:"+nn)
				print ("done percentage of job- "+nn+" is "+done_percent+"%")
				time.sleep(5)
				#new_pc1 = '/home/heinhtet/Desktop/Systematic-1/new_complete/'+pc_name+'_c/'
				#new_pc2 = '/home/heinhtet/Desktop/Systematic-1/new_complete/PC2/'
				#new_pc3 = '/home/heinhtet/Desktop/Systematic-1/new_complete/PC3/'
				#new_pc4 = '/home/heinhtet/Desktop/Systematic-1/new_complete/PC4/'
				#new_pc6 = '/home/heinhtet/Desktop/Systematic-1/new_complete/PC6/'
				#shutil.copy(new_pc1+foldName, new_pc2)
				#shutil.copy(new_pc1+foldName, new_pc3)
				#shutil.copy(new_pc1+foldName, new_pc4)
				#shutil.copy(new_pc1+foldName, new_pc6)
				os.remove(str(directory+jobs))
				dirName = directory+nn+"/"
				os.makedirs(dirName)
				subprocess.call(['chmod', '777', '-R', dirName])
				s6 = start()
				files_count = connection.recv(5120).decode("utf8")
				print ("Files count:", files_count)
				time.sleep(5)

				for account in range(int(files_count)):
					filees_name = connection.recv(5120).decode("utf8")
					time.sleep(5)
					with open(dirName+filees_name, 'wb')as f:
						datta = connection.recv(5120)
						time.sleep(5)
						if not datta:
							f.close()
							print ("File is closed.")
						f.write(datta)
					print ("Successfully get the file.")
					time.sleep(5)
				e6 = end()
				with open(measurement, 'a') as csvfile:
					csvwriter = csv.writer(csvfile)
					csvwriter.writerow(["------------------------------------"])
					csvwriter.writerow(["Start-receiving time of unfinished result "+str(foldName)+" is "+convert(int(s6))+" from "+pc_name])
					csvwriter.writerow(["End-receiving time of unfinished result "+str(foldName)+" is "+convert(int(e6))+" from "+pc_name])
					csvwriter.writerow(["How long job receiving time of unfinished result "+str(foldName)+"from "+pc_name+"to master is "+convert(int(e6)-int(s6))])
					#csvwriter.writerow(["Receiving time of successfully finished job - "+str(foldName)+" from worker "+pc_name+" is "+convert(int(rer))])
					#csvwriter.writerow(["Number of final result received files - "+str(nn)])
				back_data = connection.recv(5120).decode("utf8")
				if "finish" in back_data:
					print ("Check is there any other jobs")
					time.sleep(5)
					connection.close()
					exit()
		else:
			print ("Flase.........................................")

def start():
	start_total = (datetime.datetime.now().hour*3600)+(datetime.datetime.now().minute*60)+datetime.datetime.now().second
	start_time = str(datetime.datetime.now().hour)+":"+str(datetime.datetime.now().minute)+":"+str(datetime.datetime.now().second)
	start_date = str(datetime.datetime.now().day)+"/"+str(datetime.datetime.now().month)+"/"+str(datetime.datetime.now().year)
	print ("Starting time(h:m:s)-"+start_time+" ("+start_date+")")
	return start_total
def end():
	finish_total = (datetime.datetime.now().hour*3600)+(datetime.datetime.now().minute*60)+datetime.datetime.now().second
	finish_time = str(datetime.datetime.now().hour)+":"+str(datetime.datetime.now().minute)+":"+str(datetime.datetime.now().second)
	finish_date = str(datetime.datetime.now().day)+"/"+str(datetime.datetime.now().month)+"/"+str(datetime.datetime.now().year)
	print ("Finishing time(h:m:s)-"+finish_time+" ("+finish_date+")")
	return finish_total

def convert(seconds):
	min, sec = divmod(seconds, 60)
	hour, min = divmod(min, 60)
	return "%d(h):%02d(m):%02d(s)" % (hour, min, sec)
if __name__=="__main__":
	main()	
