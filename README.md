# UPC System
There are three main components in our UPC system:
1. UPC Web Server
2. UPC Master
3. UPC Worker

### Prerequisite
nodejs, NPM, and Python should be installed.
For more details (necessary modules), check in the requirements.txt 

### How to get the project
Just download zip folder or clone the repo using git command on your system.

### Start server with default port 1200
```
node server.js
```
### Start server with specific port 4200
```
node server.js 4200
```
### Open in browser, show download/upload UPC Web Server UI
```
e.g https://localhost:1200
e.g https://your_server_ip:1200
e.g https://your_server_ip:1200/APLAS
e.g https://your_server_ip:1200/EPLAS
```
## UPC Web Server
![Picture11](https://user-images.githubusercontent.com/79504426/118064692-76a79700-b3d6-11eb-996c-3e35e58490c1.png)
- UPC web server is located under the local area network.
- User in the same network can access UPC Web interface directly through the web browser for submitting the jobs.
- For the EPLAS that doesn't have the public ip address for it's own server. In this case, they can submit the jobs by adding to the pCLoud.
- For the APLAS that has own public ip address for the server, it allows SSH connection for the UPC. UPC grabs the job from APLAS server using SSHFS protocol.
- According to the above figure, all necessary directories are needed to create at Web Server storage due to synchronize with the UPC Master.
## UPC Master
![Picture12](https://user-images.githubusercontent.com/79504426/118064888-e6b61d00-b3d6-11eb-92e9-4cbcd7bc621a.png)
- Every 3o seconds, UPC Master checks the jobs from the Web Server. If there is job, it is moved to the temporary queue. Jobs in the temporary queue are renamed and put in the common queue.
- Jobs in the common queue are extracted and read the Metadata of each job to differentiate docker image is needed to build or not. 
- After doing the necessary things on the jobs, they are waiting in the container queue until the workers are not joined 
- If the workers are already in the available worker list, jobs are assigned to the correspondance worker queue.
## UPC Worker
![Picture13](https://user-images.githubusercontent.com/79504426/118064996-1cf39c80-b3d7-11eb-9d55-ba5e11fb3fd9.png)
- Workers join the master and update the available worker list in the Master and check the jobs.
- Every five seconds, workers check new jobs are arrived or not.
### Brief explanation of User-PC Computing System(UPC) Study
1. We develop a platform named UPC.
2. We study static and dynamic scheduling for the UPC system.
3. We investigate the job migration when one user pc cannnot keep executing our UPC jobs.
