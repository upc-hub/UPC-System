# UPC Web Server
Built based on Node.JS to upload the job programs and download the results

### Pre-requisit
**Nothing** No NPM Module dependency, as it is written using pure Node.JS API. Only nodejs should be installed.


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
e.g http://localhost:1200
e.g http://your_server_ip:1200
```

### Brief explanation of working flow
1. User can submit jobs by clicking the submit/download button.
2. To submit the last job, click the last job button.
3. All user submitted jobs are saved in under submit_download directory.
4. When the last job button clicked, the jobs under submit_download are synchronized to the UPC master server using ssh file transfer protocol.
5. UPC master performs the job management and execution process collaborating with UPC workers.
6. When UPC master obtains the results from the worker PCs, it synchronizes these reults with the UPC Web server and store under submit_download directory.
7. When results appear on the web interface, user can download by clicking the results.
(Currently, you can only check submit/download button to upload jobs and by clicking this job you can also download again because there are other things necessary to carry out to connect with UPC master. Soon, I can provide you. Thank you very much.) 
