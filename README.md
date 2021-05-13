# UPC System
There are mainly three components:
1. UPC Web Server
2. UPC Master
3. UPC Worker

### Pre-requisit
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
- For the APLAS that has own public ip address for the server, it allows SSH connection for the UPC. UPC grabs the job using SSHFS protocol 
## UPC Master
![Picture12](https://user-images.githubusercontent.com/79504426/118064888-e6b61d00-b3d6-11eb-92e9-4cbcd7bc621a.png)
## UPC Worker
![Picture13](https://user-images.githubusercontent.com/79504426/118064996-1cf39c80-b3d7-11eb-9d55-ba5e11fb3fd9.png)
### Brief explanation of working flow
1. User can submit jobs by clicking the submit/download button.
2. To submit the last job, click the last job button.
3. All user submitted jobs are saved in under submit_download directory.
4. When the last job button clicked, the jobs under submit_download are synchronized to the UPC master server using ssh file transfer protocol.
5. UPC master performs the job management and execution process collaborating with UPC workers.
6. When UPC master obtains the results from the worker PCs, it synchronizes these reults with the UPC Web server and store under submit_download directory.
7. When results appear on the web interface, user can download by clicking the results.
(Currently, you can only check submit/download button to upload jobs and by clicking this job you can also download again because there are other things necessary to carry out to connect with UPC master. Soon, I can provide you. Thank you very much.) 
