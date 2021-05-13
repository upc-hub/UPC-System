import socket
import sys, os
import datetime
import time
import subprocess
import csv
global counter
from pynput import keyboard
from threading import Thread
#from pynput import keyboard
counter = 0

def checkpointi(chk_name):
	os.system('podman container checkpoint -l --export=/tmp/'+chk_name+'_checkpoint.tar.gz')
#def do_podman(jobs_name, docker_name,s5):
	

def on_press(key):
	if key == keyboard.Key.shift: # handles if key press is shift
		#print('foo', end='')

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
		#checkpointi(check[0])
		#subprocess.call(['podman', 'container', 'checkpoint', '-l', '--export=/tmp/', check[0]+'_checkpoint.tar.gz'])
		os.chdir('/tmp')
		#subprocess.call(['tar', 'czf', check[0]+'_checkpoint.tar.gz', check[0]+'_checkpoint'])
		soc.sendall(str(jobs_name+'_c.tar.gz').encode("utf8"))
		#time.sleep(5)
		#subprocess.call(['python3', '/home/worker3/Desktop/sender.py', 'checkpoint'+check[0]+'.tar.gz', '172.28.235.18'])
		subprocess.call(['scp', jobs_name+'_c.tar.gz', 'root@192.168.56.100:/home/heinhtet/Desktop/Systematic-1/new_complete/c_PC2/'])
		subprocess.call(['rm', '-r', jobs_name+'_c.tar.gz'])
		e7 = end()
		print ("Checkpoint and Transfer time to the master:*******"+convert(int(e7)-int(s7))+"********")
		with open(measurement, 'a') as csvfile:
			csvwriter = csv.writer(csvfile)
			csvwriter.writerow(["Docker Container Checkpoint and Transfer time to the master of "+jobs_name+" is "+convert(int(e7)-int(s7))])
		with open('/home/workerpc3/Desktop/pc2_cputime.csv', 'rt')as f:
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
	
	#start_min = datetime.datetime.now().minute+2
	#print (start_min)
	global soc
	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	host = "192.168.56.100"
	port = 2000
	global measurement
	a = start()
	measurement = '/home/workerpc3/Desktop/conduct_measurement.csv'

	try:
		soc.connect((host, port))
	except:
		print("Connection error")
		sys.exit()
	time.sleep(5)
	print ("Counter no.", counter)
	if counter == 0:
		soc.sendall("PC3".encode("utf8"))
	else:
		soc.sendall('PC3_cc'.encode("utf8"))

	global directory
	directory = '/home/upc/'
	#global jobs_name
	jobs_no = soc.recv(5120).decode("utf8") #1st_receive(no_of_projects)
	if jobs_no=="no_job":
		
		#send ready message
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
			csvwriter.writerow(["Total no. of jobs will be received from master is ", jobs_no])
			csvwriter.writerow(["Current received job is ", jobs_name])
			csvwriter.writerow(["-----------------------"])
		#if (int(jobs_no)==0):
		#    soc.send(b'--quit--')
		
		dd = jobs_name.split("_")
		
		try:
			print ("Check error or not"+dd[2])
			print ("This is creating checkpoint empty container.")
			docker_name = 'pollen5005/'+dd[1]+":latest"
			print ("Container name:", docker_name)
			checkpoint_name = dd
			print ("Recive checkpoint Name:", checkpoint_name)
			with open(measurement, 'a') as csvfile:
				csvwriter = csv.writer(csvfile)
				csvwriter.writerow(["-----------------------"])
				csvwriter.writerow(["Received container name is ", docker_name, "and received checkpoint name is ", checkpoint_name])
				csvwriter.writerow(["-----------------------"])
			
			#print ('docker create -t --name -v /home/workerpc1/Desktop/Receive_Jobs/:/opt', docker_name)
			#while datetime.datetime.now().minute<=start_min:
			try:
				s_resume = start()
				with open(measurement, 'a') as csvfile:
					csvwriter = csv.writer(csvfile)
					csvwriter.writerow(["-----------------------"])
					csvwriter.writerow(["Interrupted job receiving time", convert(int(s_resume))])
					csvwriter.writerow(["-----------------------"])
				subprocess.call(['python3', '/home/workerpc3/Desktop/receiver.py'])
				#subprocess.call(['docker', 'create', '-t', '--name', jobs_name+'_'+dd[0], '-v', '/home/worker3/Desktop/Receive_Jobs/:/opt', docker_name])
				#subprocess.call(['podman', 'run', '-t', '--name', jobs_name, '-v', '/home/upc/:/opt',docker_name])
				#soc.sendall(str("zip").encode("utf8"))
				#time.sleep(5)
				#os.chdir('/tmp')
				#subprocess.call(['tar', 'xzf', checkpoint_name])
				#time.sleep(5)
				#one_break = checkpoint_name.split(".")
				#print ("Real checkpoint Name:", one_break[0])

				#subprocess.call("mv /tmp/"+one_break[0]+" /var/lib/docker/containers/$(docker ps -aq --no-trunc --filter name="+jobs_name+"_"+dd[0]+")/checkpoints/", shell=True)
				e_resume = end()
				#subprocess.call(['mv', '/tmp/1_checkpoint', '/var/lib/docker/containers/$(docker ps -aq --no-trunc --filter name='+jobs_name+'_'+dd[0]+')/checkpoints/'])
				s5 = start()
				subprocess.call(['podman', 'container', 'restore', '--import=/tmp/'+jobs_name, '-n', 'ooo'])
				while True:
					tmm = os.popen("podman ps").read()
					counc = tmm.count("ooo")
					if (counc==0):
						print ("Job is still running. Job count is", counc)
						break
					print ("Executing......")
					time.sleep(5)
				print ("Finished executing.")
				#while True:
				#	fil = len(os.listdir("/home/upc/"))
				#	print ("File count", fil)
				#	if (fil==2):
				#		print ("Both obtained")
				#		break
				#	elif (fil==1):
				#		print ("One obtained")
				#	print ("No File")
				#	time.sleep(5)
				subprocess.call(['rm', '-r', '/tmp/'+jobs_name])
				e5 = end()
				print ("Docker Container checkpoint Running time:*******"+convert(int(e5)-int(s5))+"********")
				with open(measurement, 'a') as csvfile:
					csvwriter = csv.writer(csvfile)
					csvwriter.writerow(["-----------------------"])
					#csvwriter.writerow(["Start receiving time(downtime app) of "+jobs_name+" is "+convert(int(s5))])
					#csvwriter.writerow(["Checkpoint preparation(start) duration of "+jobs_name+" is "+convert(int(e_resume)-int(s_resume))])
					csvwriter.writerow(["Interrupted job checkpoint starting time"+ convert(int(s5))])
					csvwriter.writerow(["Docker Container checkpoint Running time of interrupted job - "+jobs_name+" is "+convert(int(e5)-int(s5))])
					csvwriter.writerow(["Interrupted job checkpoint finishing time"+ convert(int(e5))])
					csvwriter.writerow(["-----------------------"])

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
					csvwriter.writerow(["Docker Container checkpoint result transferring time of "+jobs_name+" is "+convert(int(e6)-int(s6))])
					csvwriter.writerow(["-----------------------"])


				
			except KeyboardInterrupt:
				print ("Checkpoint name:"+jobs_name)
				subprocess.call(['docker', 'checkpoint', 'create', '--checkpoint-dir=/tmp', jobs_name, check[0]+'_checkpoint'])
				os.chdir('/tmp')
				subprocess.call(['tar', 'czf', check[0]+'_checkpoint.tar.gz', check[0]+'_checkpoint'])
				soc.sendall(str(check[0]+'_checkpoint').encode("utf8"))
				#time.sleep(5)
				#subprocess.call(['python3', '/home/worker3/Desktop/sender.py', 'checkpoint'+check[0]+'.tar.gz', '172.28.235.18'])
				subprocess.call(['scp', check[0]+'_checkpoint.tar.gz', 'root@192.168.56.100:/home/heinhtet/Desktop/Systematic-1/new_complete/checkpoint_data/'])
				subprocess.call(['rm', '-r', check[0]+'_checkpoint', check[0]+'_checkpoint.tar.gz'])
		except IndexError:
			docker_name = 'pollen5005/'+dd[1]+":latest"
			print ("Container name:", docker_name)
			run_time = 0
			
			#print ('docker run --rm -it -v /home/workerpc1/Desktop/Receive_Jobs/:/opt', docker_name)
			sa = start()
			subprocess.call(['python3', '/home/workerpc3/Desktop/receiver.py'])
			s4 = start()
			subprocess.call(['podman', 'load', '-i', jobs_name])
			e4 = end()
			print ("Docker Image Loading time:*******"+convert(int(e4)-int(s4))+"********")
			with open(measurement, 'a') as csvfile:
				csvwriter = csv.writer(csvfile)
				csvwriter.writerow(["-----------------------"])
				csvwriter.writerow(["Normal container name", str(docker_name)])
				csvwriter.writerow(["Normal job received time", convert(int(sa))])
				csvwriter.writerow(["Docker Image loading time of "+jobs_name+" is "+convert(int(e4)-int(s4))])
				csvwriter.writerow(["-----------------------"])
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
				print ("Result transferring time:*******"+convert(int(e6)-int(s6))+"********")
				with open(measurement, 'a') as csvfile:
					csvwriter = csv.writer(csvfile)
					csvwriter.writerow(["Docker Container result transferring time of "+jobs_name+" is "+convert(int(e6)-int(s6))])
				break
				#tha = True
			
			#thread1.start()
			#thread2.start()

			#thread1.join()
			#thread2.join()
					#subprocess.call(['podman', 'run', '-t', '--name', jobs_name, '-v', '/home/upc/:/opt',docker_name])
					#if keyboard.is_pressed('q'):
					#	print('You Pressed A Key!')
					#	break  # finishing the loop
					







			#if KeyboardInterrupt:
			#	print ("Interrupting ....................")
			#subprocess.call(['docker', 'checkpoint', 'create', '--checkpoint-dir=/tmp', jobs_name, 'checkpoint1'])
			#if (docker_name=="pollen5005/apc:latest"):
				#subprocess.call(['docker', 'run', '--rm', '-it', docker_name])
			#    subprocess.call(['docker', 'run', '--rm', '-it', '-v', '/home/worker3/Desktop/Receive_Jobs/:/opt', docker_name])
			#else:
			#    subprocess.call(['docker', 'run', '--rm', '-it', '-v', '/home/worker3/Desktop/Receive_Jobs/:/opt', docker_name])
		






	soc.sendall("finish".encode("utf8"))
	for fills_name in os.listdir(directory):
		os.remove(str(directory+fills_name))
	time.sleep(5)
	subprocess.call(['podman', 'container', 'prune'])
	main()
	
	print("Enter 'quit' to exit")
	message = input(" -> ")

	while message != 'quit':
		soc.sendall(message.encode("utf8"))

		if soc.recv(5120).decode("utf8") == "-":
			pass        # null operation

		message = input(" -> ")

	soc.send(b'--quit--')
	


def file_extent_python(docker_directory, file_name, directory1, s2):
	print ("This is a python program")
	f = open(docker_directory, 'r')
	message = f.read()
	message = message.replace('#MAINTAINER','Hein Htet <p58g9ad2@s.okayama-u.ac.jp>')
	message = message.replace('#FROM','pollen5005/py_program:latest')
	#message = message.replace('#WORKDIR','/app')
	#message = message.replace('#COPY','requirements.txt ./')
	#message = message.replace('#RUN','pip install -r requirements.txt')
	message = message.replace('#ADD',file_name+' /app')
	message = message.replace('#CMD','["python3", "'+file_name+'"]')
	#message = message.replace('ENV','#ENV')
	#message = message.replace('ENTRYPOINT','#ENTRYPOINT')
	#message = message.replace('EXPOSE','#EXPOSE')
	
	with open(docker_directory, 'w')as f:
		f.write(message)
	
	f.close()
	subprocess.call(['docker', 'build', '-t', 'pollen5005/'+file_name.lower()+":latest", directory1])
	e2 = end()
	print ("Docker Image Building time:"+convert(int(e2)-int(s2)))
	##subprocess.call(['docker', 'push', 'pollen5005/'+file_name.lower()+':latest'])
	s3 = start()
	subprocess.call(['docker', 'run', '-it', '--rm', 'pollen5005/'+file_name.lower()+":latest"])
	e3 = end()
	print ("Docker Image Running time:"+convert(int(e3)-int(s3)))

def file_extent_c(docker_directory, file_name, directory1, s2):
	print ("This is a C program")
	name, ext = os.path.splitext(file_name)
	f = open(docker_directory, 'r')
	message = f.read()
	message = message.replace('#MAINTAINER','Hein Htet <p58g9ad2@s.okayama-u.ac.jp>')
	message = message.replace('#FROM','gcc:4.9')
	message = message.replace('#COPY','. /usr/src/c_program_space')
	message = message.replace('#WORKDIR','/usr/src/c_program_space')
	message = message.replace('#RUN','gcc -o '+name+' '+file_name)
	message = message.replace('#CMD','["./'+name+'"]')
	message = message.replace('ENV','#ENV')
	message = message.replace('ENTRYPOINT','#ENTRYPOINT')
	message = message.replace('ADD','#ADD')
	message = message.replace('EXPOSE','#EXPOSE')

	with open(docker_directory, 'w')as f:
		f.write(message)
	
	f.close()
	subprocess.call(['docker', 'build', '-t', 'pollen5005/'+file_name.lower()+":latest", directory1])
	e2 = end()
	print ("Docker Image Building time:"+convert(int(e2)-int(s2)))
	s3 = start()
	subprocess.call(['docker', 'run', '-it', '--rm', 'pollen5005/'+file_name.lower()+":latest"])
	e3 = end()
	print ("Docker Image Running time:"+convert(int(e3)-int(s3)))
	
	##subprocess.call(['docker', 'push', 'pollen5005/'+file_name.lower()+'latest'])

def file_extent_java(docker_directory, file_name, directory1, s2):
	print ("This is a Java program")
	name, ext = os.path.splitext(file_name)
	f = open(docker_directory, 'r')
	message = f.read()
	message = message.replace('#MAINTAINER','Hein Htet <p58g9ad2@s.okayama-u.ac.jp>')
	#message = message.replace('#FROM','openjdk:8u131-jre-alpine')
	message = message.replace('#FROM','alpine:latest')
	message = message.replace('#ENV','HW_HOME=/opt/java_program_space')
	message = message.replace('#RUN','apk --update add openjdk8-jre')
	#message = message.replace('RUN','#RUN')
	message = message.replace('#ADD',name+'.class $HW_HOME/')
	message = message.replace('#WORKDIR','$HW_HOME')
	message = message.replace('#ENTRYPOINT','["java", "'+name+'"]')
	message = message.replace('CMD','#CMD')
	message = message.replace('COPY','#COPY')
	message = message.replace('EXPOSE','#EXPOSE')
	#message = message.replace('#FROM','alpine:latest')
	#message = message.replace('#RUN','apk --update add openjdk8-jre')
	#message = message.replace('#ENTRYPOINT','["java", "-Djava.security.egd=file:/dev/./urandom", "HelloWorld"]')
	with open(docker_directory, 'w')as f:
		f.write(message)
	
	f.close()
	subprocess.call(['docker', 'run', '-it', '-v', directory1+':/build', 'openjdk:8u131-jdk-alpine', 'javac', '/build/'+file_name])
	subprocess.call(['docker', 'build', '-t', 'pollen5005/'+file_name.lower()+":latest", directory1])
	e2 = end()
	print ("Docker Image Building time:"+convert(int(e2)-int(s2)))
	s3 = start()
	subprocess.call(['docker', 'run', '-it', '--rm', 'pollen5005/'+file_name.lower()+":latest"])
	e3 = end()
	print ("Docker Image Running time:"+convert(int(e3)-int(s3)))
	
	##subprocess.call(['docker', 'push', 'pollen5005/'+file_name.lower()+':latest'])

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
