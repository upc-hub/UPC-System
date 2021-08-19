import requests
import json
import os
import codecs
import subprocess

typea_count = 0
typeb_count = 0
typec_count = 0
S1 = "BasixAppX\r\n"
S2 = "ColorGameX\r\n"
S3 = "SoccerMatch\r\n"
jobs_type = []
extract = ""
APLAS_dir = '/home/heinhtet/Desktop/UPC_Master/APLAS/newJobs/'
for jobs in os.listdir(APLAS_dir):
  extract_job = jobs.split('.')
  if extract_job[1]=="manifest":
    manifest = open('/home/heinhtet/Desktop/UPC_Master/APLAS/newJobs/'+jobs, 'rb')
    for line in manifest:
      #if line.startswith('PROJECT='):
      line = line.decode('UTF-8')
      extract = line
      split_extract = extract.split('=')
      
      if split_extract[0]=='PROJECT' and split_extract[1]==S1:
        typea_count+=1
        jobs_type.append(split_extract[1])
      elif split_extract[0]=='PROJECT' and split_extract[1]==S2:
        typeb_count+=1
        jobs_type.append(split_extract[1])
      elif split_extract[0]=='PROJECT' and split_extract[1]==S3:
        typec_count+=1
        jobs_type.append(split_extract[1])
        #jobs_type.append(split_extract[1])
print ("BasixAppX", typea_count)
print ("ColorGameX", typeb_count)
print ("SoccerMatch", typec_count)
print (jobs_type)
subprocess.call(['python3', '/home/heinhtet/Desktop/UPC_Master/call_sam_scheduling.py', str(typea_count), str(typeb_count), str(typec_count)])
ff = open('/home/heinhtet/Desktop/UPC_Master/data.json', 'r')
data = json.loads(ff.read())
for i in range(3):
  for a in range(4):
  	print (data['data'][0]['result_details'][0]['job_amount'])