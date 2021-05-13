import socket
import sys, os
import datetime
import time
import subprocess
import csv
global counter
from pynput import keyboard
from threading import Thread
counter = 0
def checkpointi(chk_name):
	os.system('podman container checkpoint -l --export=/tmp/'+chk_name+'_checkpoint.tar.gz')

def on_press(key):
	if key == keyboard.Key.shift:
		global tha
		tha = True
		os.system('podman container checkpoint -l --export=/tmp/'+jobs_name+'_c.tar.gz')
		time.sleep(5)
		print ("Checkpoint finished <press Ctrl+C>")
		print ("KeyboardInterrupt is starting......................................")
		s7 = start()
		run_time = int(s7)-int(g)
		total_sec = ''
		print ("Checkpoint name:"+jobs_name)
		os.chdir('/tmp')
		soc.sendall(str(jobs_name+'_c.tar.gz').encode("utf8"))
		subprocess.call(['scp', jobs_name+'_c.tar.gz', 'root@192.168.56.100:/home/heinhtet/Desktop/Systematic-1/new_complete/PC1_c/'])
		subprocess.call(['rm', '-r', jobs_name+'_c.tar.gz'])

		e7 = end()
		print ("Checkpoint and Transfer time to the master:*******"+convert(int(e7)-int(s7))+"********")
		with open(measurement, 'a') as csvfile:
			csvwriter = csv.writer(csvfile)
			csvwriter.writerow(["Docker Container Checkpoint and Transfer time to the master of "+jobs_name+" is "+convert(int(e7)-int(s7))])

		with open('/home/pc4/Desktop/pc4_cputime.csv', 'rt')as f:
			reader = csv.reader(f)
			next(reader, None)
			for row in reader:
				if row[0]==check[1]:
					total_sec = row[1]
				else:
					print ("Not that job.")
		percentage = (run_time*100)/int(total_sec)

		s6 = start()
		checka = jobs_name.split("_")
		soc.sendall(str(checka[1]).encode("utf8"))
		time.sleep(5)
		print ("Finished percentage before interrupted", percentage)
		soc.sendall(str(percentage).encode("utf8"))
		time.sleep(5)

		fill_count = 0
		for fills_name in os.listdir(directory):
			fill_count = fill_count+1
		print ("Total no. of result files", fill_count)
		soc.sendall(str(fill_count).encode("utf8"))
		time.sleep(5)
		for fills_name in os.listdir(directory):
			print (fills_name)
			soc.sendall(str("1_"+fills_name).encode("utf8"))
			time.sleep(5)
			fa = open(directory+fills_name, 'rb')
			I = fa.read(5120)
			while(I):
				soc.send(I)
				time.sleep(5)
				I = fa.read(5120)
			fa.close()
			time.sleep(5)
		e6 = end()
		print ("Result transferring time:*******"+convert(int(e6)-int(s6))+"********")
		with open(measurement, 'a') as csvfile:
			csvwriter = csv.writer(csvfile)
			csvwriter.writerow(["-----------------------"])
			csvwriter.writerow(["Finished percentage before interrupted", percentage])
			csvwriter.writerow(["Docker Container result transferring time of "+jobs_name+" is "+convert(int(e6)-int(s6))])
			csvwriter.writerow(["-----------------------"])
		global tha1
		tha1 = True
		global listener
		listener.stop()

def get_current_key_input():
	global listener
	with keyboard.Listener(on_press=on_press) as listener:
		listener.join()

def main():
	global jobs_name
	jobs_name = ""
	global g
	g = ""
	global counter
	counter
	global tha
	tha = False
	global tha1
	tha1 = False
	global soc
	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	host = "192.168.56.100"
	port = 2000
	global measurement
	a = start()
	measurement = '/home/pc4/Desktop/conduct_measurement.csv'

	try:
		soc.connect((host, port))
	except:
		print("Connection error")
		sys.exit()
	time.sleep(5)
	print ("Counter no.", counter)
	if counter == 0:
		soc.sendall("PC4".encode("utf8"))
	else:
		soc.sendall('PC4_c'.encode("utf8"))

	global directory
	directory = '/home/upc/'
	jobs_no = soc.recv(5120).decode("utf8")
	if jobs_no=="no_job":
		soc.close()
	elif jobs_no=="check":
		global counter
		counter = 1
		print ("PC3 can still accept extra checkpoint jobs.")
		main()
	else:
		print ("No. of jobs at master", jobs_no)
		jobs_name = soc.recv(5120).decode("utf8")
		global check
		check = jobs_name.split("_")
		print ("Receive job names:", jobs_name)
		with open(measurement, 'a') as csvfile:
			csvwriter = csv.writer(csvfile)
			csvwriter.writerow(["-----------------------"])
			#csvwriter.writerow(["Total no. of jobs will be received from master is ", jobs_no])
			csvwriter.writerow(["Current received job is ", jobs_name])
			#csvwriter.writerow(["-----------------------"])
		dd = jobs_name.split("_")
		try:
			print ("Check error or not"+dd[2])
			print ("This is creating checkpoint empty container.")
			docker_name = 'pollen5005/'+dd[1]+":latest"
			print ("Container name:", docker_name)
			checkpoint_name = dd
			print ("Recive checkpoint Name:", checkpoint_name)
			#with open(measurement, 'a') as csvfile:
				#csvwriter = csv.writer(csvfile)
				#csvwriter.writerow(["-----------------------"])
				#csvwriter.writerow(["Received checkpoint name is ", checkpoint_name])
				#csvwriter.writerow(["-----------------------"])
			try:
				s_resume = start()
				
				subprocess.call(['python3', '/home/pc4/Desktop/receiver.py'])
				e_resume = end()
				with open(measurement, 'a') as csvfile:
					csvwriter = csv.writer(csvfile)
					csvwriter.writerow(["-----------------------"])
					csvwriter.writerow(["Interrupted job start-receiving time", convert(int(s_resume))])
					csvwriter.writerow(["Interrupted job end-receiving time", convert(int(e_resume))])
					csvwriter.writerow(["How long receiving time", convert(int(e_resume)-int(s_resume))])
					#csvwriter.writerow(["-----------------------"])
				s5 = start()
				subprocess.call(['podman', 'container', 'restore', '--import=/home/pc4/Desktop/'+jobs_name, '-n', 'oooo'])
				b5 = start()
				while True:
					tmm = os.popen("podman ps").read()
					counc = tmm.count("oooo")
					if (counc==0):
						print ("Job is still running. Job count is", counc)
						break
					print ("Executing......")
					time.sleep(5)
				print ("Finished executing.")
				subprocess.call(['rm', '-r', '/home/pc4/Desktop/'+jobs_name])
				e5 = end()
				print ("Docker Container checkpoint Running time:*******"+convert(int(e5)-int(s5))+"********")
				with open(measurement, 'a') as csvfile:
					csvwriter = csv.writer(csvfile)
					csvwriter.writerow(["-----------------------"])
					#csvwriter.writerow(["Start receiving time(downtime app) of "+jobs_name+" is "+convert(int(s5))])
					#csvwriter.writerow(["Checkpoint preparation(start) duration of "+jobs_name+" is "+convert(int(e_resume)-int(s_resume))])
					csvwriter.writerow(["Checkpoint restore time"+ convert(int(b5)-int(s5))])
					csvwriter.writerow(["Interrupted job checkpoint start-running time"+ convert(int(s5))])
					csvwriter.writerow(["Interrupted job checkpoint stop-running time"+ convert(int(e5))])
					csvwriter.writerow(["Except restoration time how long "+convert(int(e5)-int(b5))])
					csvwriter.writerow(["How long interrupted job checkpoint running time"+jobs_name+" is "+convert(int(e5)-int(s5))])
					#csvwriter.writerow(["-----------------------"])

				s6 = start()
				soc.sendall(str(jobs_name).encode("utf8"))
				time.sleep(5)

				fill_count = 0
				for fills_name in os.listdir(directory):
					fill_count = fill_count+1
				print ("Total no. of checkpoint result files", fill_count)
				soc.sendall(str(fill_count).encode("utf8"))
				time.sleep(5)
				soc.sendall(str('sss').encode("utf8"))
				time.sleep(5)
				for fills_name in os.listdir(directory):
					print (fills_name)
					soc.sendall(str(fills_name).encode("utf8"))
					time.sleep(5)
					fa = open(directory+fills_name, 'rb')
					I = fa.read(5120)
					while(I):
						soc.send(I)
						time.sleep(5)
						I = fa.read(5120)
					fa.close()
					time.sleep(5)
				e6 = end()
				print ("Checkpoint result transferring time:*******"+convert(int(e6)-int(s6))+"********")
				with open(measurement, 'a') as csvfile:
					csvwriter = csv.writer(csvfile)
					csvwriter.writerow(["-----------------------"])
					csvwriter.writerow(["Interrupted job result transferring time of "+jobs_name+" is "+convert(int(e6)-int(s6))])
					#csvwriter.writerow(["-----------------------"])


				
			except KeyboardInterrupt:
				print ("Checkpoint name:"+jobs_name)
				subprocess.call(['docker', 'checkpoint', 'create', '--checkpoint-dir=/tmp', jobs_name, check[0]+'_checkpoint'])
				os.chdir('/tmp')
				subprocess.call(['tar', 'czf', check[0]+'_checkpoint.tar.gz', check[0]+'_checkpoint'])
				soc.sendall(str(check[0]+'_checkpoint').encode("utf8"))
				#time.sleep(5)
				#subprocess.call(['python3', '/home/pc4/Desktop/sender.py', 'checkpoint'+check[0]+'.tar.gz', '172.28.235.18'])
				subprocess.call(['scp', check[0]+'_checkpoint.tar.gz', 'root@192.168.56.100:/home/heinhtet/Desktop/Systematic-1/new_complete/checkpoint_data/'])
				subprocess.call(['rm', '-r', check[0]+'_checkpoint', check[0]+'_checkpoint.tar.gz'])
		except IndexError:
			docker_name = 'pollen5005/'+dd[1]+":latest"
			print ("Container name:", docker_name)
			run_time = 0
			
			#print ('docker run --rm -it -v /home/workerpc1/Desktop/Receive_Jobs/:/opt', docker_name)
			sa = start()
			subprocess.call(['python3', '/home/pc4/Desktop/receiver.py'])
			s4 = start()
			subprocess.call(['podman', 'load', '-i', jobs_name])
			e4 = end()
			transmission = int(s4)-int(sa)
			loading = int(e4)-int(s4)
			print ("Docker Image Loading time:*******"+convert(int(e4)-int(s4))+"********")
			with open(measurement, 'a') as csvfile:
				csvwriter = csv.writer(csvfile)
				csvwriter.writerow(["-----------------------"])
				csvwriter.writerow(["Normal container name", str(docker_name)])
				csvwriter.writerow(["Docker Image transmission time of "+jobs_name+" is "+convert(int(s4)-int(sa))])
				csvwriter.writerow(["Docker Image loading time of "+jobs_name+" is "+convert(int(e4)-int(s4))])
				#csvwriter.writerow(["-----------------------"])
			os.remove(str(jobs_name))
			#while datetime.datetime.now().minute<=start_min:
			g = start()
			s5 = start()
			thread1 = Thread(target = get_current_key_input)
			thread1.start()
			
			#Thread(target = do_podman(jobs_name, docker_name,s5)).start()
			subprocess.call(['podman', 'run', '-t', '--name', jobs_name, '-v', '/home/upc/:/opt',docker_name])
			while True:
				
				e5 = end()
				with open(measurement, 'a') as csvfile:
					csvwriter = csv.writer(csvfile)
					csvwriter.writerow(["Interrupted time"+convert(int(e5))+" of job "+ str(jobs_name)])
				global tha
				if tha:
					while True:
						if tha1:
							break
					break
				print ("No interrupt..............................................................")
				print ("Docker Container Running time:*******"+convert(int(e5)-int(s5))+"********")
				running = int(e5)-int(s5)
				with open(measurement, 'a') as csvfile:
					csvwriter = csv.writer(csvfile)
					csvwriter.writerow(["Docker (without interrupt) Container Running time of "+jobs_name+" is "+convert(int(e5)-int(s5))])
					

				s6 = start()
				soc.sendall(str(jobs_name).encode("utf8"))
				time.sleep(5)

				fill_count = 0
				for fills_name in os.listdir(directory):
					fill_count = fill_count+1
				print ("Total no. of result files", fill_count)
				soc.sendall(str(fill_count).encode("utf8"))
				time.sleep(5)
				soc.sendall(str('sss').encode("utf8"))
				time.sleep(5)
				for fills_name in os.listdir(directory):
					print (fills_name)
					soc.sendall(str(fills_name).encode("utf8"))
					time.sleep(5)
					fa = open(directory+fills_name, 'rb')
					I = fa.read(5120)
					while(I):
						soc.send(I)
						time.sleep(5)
						I = fa.read(5120)
					fa.close()
					time.sleep(5)
				e6 = end()
				transferring = int(e6)-int(s6)
				total_without = loading+running+transferring
				total = transmission+loading+running+transferring
				print ("Result transferring time:*******"+convert(int(e6)-int(s6))+"********")
				with open(measurement, 'a') as csvfile:
					csvwriter = csv.writer(csvfile)
					csvwriter.writerow(["Docker Container result transferring time of "+jobs_name+" is "+convert(int(e6)-int(s6))])
					csvwriter.writerow(["Total running time with transmission"+jobs_name+" is "+convert(total)+" in seconds"+ str(total)+" )"])
					csvwriter.writerow(["Total running time "+jobs_name+" is "+convert(total_without)+" in seconds"+ str(total_without)+" )"])
				break
	soc.sendall("finish".encode("utf8"))
	for fills_name in os.listdir(directory):
		os.remove(str(directory+fills_name))
	time.sleep(5)
	subprocess.call(['podman', 'container', 'prune'])
	soc.close()
	#main()
	
	print("Enter 'quit' to exit")
	message = input(" -> ")

	while message != 'quit':
		soc.sendall(message.encode("utf8"))

		if soc.recv(5120).decode("utf8") == "-":
			pass        # null operation

		message = input(" -> ")

	soc.send(b'--quit--')

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

if __name__ == "__main__":
	main()
