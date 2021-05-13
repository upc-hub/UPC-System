const http = require('http');
const https = require('https');
const fs = require('fs');
const path = require('path');
const syncRequest = require('sync-request');
const request = require('request');
const schedule = require('node-schedule');

class PcloudClinet {
  accessToken = "EMWL7ZTsJ8P3KnNQSZ6P3GG7ZEPG5k0HKW6L7nHs2Dvs9WS8TxEvX";

  listFolder(path) {
    var options = {
      'method': 'GET',
      'url': 'https://api.pcloud.com/listfolder',
    };
    options.url = options.url +
      "?access_token=" + this.accessToken +
      "&path=" + path;
    return JSON.parse(syncRequest('GET', options.url).body);
  }

  uploadFile(fileName, localFilePath, cloudFilePath) {
    var options = {
      'method': 'POST',
      'url': 'https://api.pcloud.com/uploadfile',
      formData: {
        'files': {
          'value': fs.createReadStream(localFilePath),
          'options': {
            'filename': fileName,
            'contentType': null
          }
        }
      }
    };
    options.url = options.url +
      "?access_token=" + this.accessToken +
      "&filename=" + fileName +
      "&path=" + cloudFilePath;
    request(options, function (error, response) {
      if (error) throw new Error(error);
      console.log(response.body);
    });
  }

  downloadFile(fileLink, fileName) {
    var dest = path.join("/home/upc_web_server/Desktop/UPC-System-sam/EPLAS/newJobs", fileName);
    fileLink = "http://" + fileLink;
    let stream = fs.createWriteStream(dest);
    request(fileLink).pipe(stream).on("close", function (err) {
      console.log("file[" + fileName + "]downloaded");
    });
  }


  moveFile(path, toPath) {
    var options = {
      'method': 'GET',
      'url': 'https://api.pcloud.com/renamefile',
    };
    options.url = options.url +
      "?access_token=" + this.accessToken + "&path=" + path + "&topath=" + toPath;
    return JSON.parse(syncRequest('GET', options.url).body);
  }

  getFileLink(filePath) {
    var options = {
      'method': 'GET',
      'url': 'https://api.pcloud.com/getfilelink',
    };
    options.url = options.url +
      "?access_token=" + this.accessToken +
      "&path=" + filePath;
    var res = JSON.parse(syncRequest('GET', options.url).body);
    return res.hosts[0] + res.path;
  }

}


let port = process.argv[2] || 1200;
const httpServer = http.createServer(requestHandler);
const pcloudCLient = new PcloudClinet();
httpServer.listen(port, () => {
  console.log('server is listening on port ' + port)
});

function requestHandler(req, res) {
  if (req.url === '/') {
    sendIndexHtml(res);
  } else if (req.url === '/list') {
    sendListOfUploadedFiles(res);
  } else if (req.url === '/alocalResults') {
    sendListOfUploadedFileslocalResults(res);
  } else if (req.url === '/alocalWaiting') {
    sendListOfUploadedFileslocalWaiting(res);
  } else if (req.url === '/alocalRunning') {
    sendListOfUploadedFileslocalRunning(res);
  } else if (req.url === '/alocalFinished') {
    sendListOfUploadedFileslocalFinished(res);
  } else if (req.url === '/EPLAS') {
  	sendIndexHtmlpCLoud(res)
  } else if (req.url === '/ppEPLAS') {
    sendListOfUploadedFilespCloud(res);
  } else if (req.url === '/ppEPLASResults') {
    sendListOfUploadedFilespCloudResults(res);
  } else if (req.url === '/ppEPLASWaiting') {
    sendListOfUploadedFilespCloudWaiting(res);
  } else if (req.url === '/ppEPLASRunning') {
    sendListOfUploadedFilespCloudRunning(res);
  } else if (req.url === '/ppEPLASFinished') {
    sendListOfUploadedFilespCloudFinished(res);
  } else if (req.url === '/APLAS') {
  	sendIndexHtmlAPLAS(res)
  } else if (req.url === '/aaplas') {
    sendListOfUploadedFilesFTP(res);
  } else if (req.url === '/aaplasResults') {
    sendListOfUploadedFilesFTPResults(res);
  } else if (req.url === '/aaplasWaiting') {
    sendListOfUploadedFilesFTPWaiting(res);
  } else if (req.url === '/aaplasRunning') {
    sendListOfUploadedFilesFTPRunning(res);
  } else if (req.url === '/aaplasFinished') {
    sendListOfUploadedFilesFTPFinished(res);
  } else if (/\/local_user\/[^\/]+$/.test(req.url)) {
    sendUploadedFile(req.url, res);
  } else if (/\/upload\/[^\/]+$/.test(req.url)) {
    saveUploadedFile(req, res)
  } else if (/\/execute\/[^\/]+$/.test(req.url)) {
    executeUploadedFile(req, res)
  } else if (req.url == "/start") {
    checkPcloudNewJobs();
    checkPcloudResults();
    checkSSHFSNewJobs()
    res.writeHead(200, {
      'Content-Type': ''
    });
    res.end();
  } else {
    sendInvalidRequest(res);
  }
}



function sendIndexHtml(res) {
  let indexFile = path.join(__dirname, 'index.html');
  fs.readFile(indexFile, (err, content) => {
    if (err) {
      res.writeHead(404, {
        'Content-Type': 'text'
      });
      res.write('File Not Found!');
      res.end();
    } else {
      res.writeHead(200, {
        'Content-Type': 'text/html'
      });
      res.write(content);
      res.end();
    }
  })
}

function sendIndexHtmlpCLoud(res) {
	var folderPath="/home/upc_web_server/Desktop/UPC-System-sam/EPLAS/newJobs"
	var files = fs.readdirSync(folderPath).map(fileName => {
      return path.join(folderPath, fileName)
    })
    console.log(files)
  let indexFile = path.join(__dirname, 'indexPcloud.html');
  fs.readFile(indexFile, (err, content) => {
    if (err) {
      res.writeHead(404, {
        'Content-Type': 'text'
      });
      res.write('File Not Found!');
      res.end();
    } else {
      res.writeHead(200, {
        'Content-Type': 'text/html'
      });
      res.write(content);
      res.end();
    }
  })
}

function sendIndexHtmlAPLAS(res) {
	var folderPath="/home/upc_web_server/Desktop/UPC-System-sam/APLAS/newJobs"
	var files = fs.readdirSync(folderPath).map(fileName => {
      return path.join(folderPath, fileName)
    })
    console.log(files)
  let indexFile = path.join(__dirname, 'indexFTP.html');
  fs.readFile(indexFile, (err, content) => {
    if (err) {
      res.writeHead(404, {
        'Content-Type': 'text'
      });
      res.write('File Not Found!');
      res.end();
    } else {
      res.writeHead(200, {
        'Content-Type': 'text/html'
      });
      res.write(content);
      res.end();
    }
  })
}

function sendListOfUploadedFiles(res) {
  let uploadDir = path.join(__dirname, 'local_user/newJobs');
  fs.readdir(uploadDir, (err, files) => {
    if (err) {
      console.log(err);
      res.writeHead(400, {
        'Content-Type': 'application/json'
      });
      res.write(JSON.stringify(err.message));
      res.end();
    } else {
      res.writeHead(200, {
        'Content-Type': 'application/json'
      });
      res.write(JSON.stringify(files));
      res.end();
    }
  })
}

function sendListOfUploadedFilespCloud(res) {
  let uploadDir = path.join(__dirname, 'EPLAS/newJobs');
  fs.readdir(uploadDir, (err, files) => {
    if (err) {
      console.log(err);
      res.writeHead(400, {
        'Content-Type': 'application/json'
      });
      res.write(JSON.stringify(err.message));
      res.end();
    } else {
      res.writeHead(200, {
        'Content-Type': 'application/json'
      });
      res.write(JSON.stringify(files));
      res.end();
    }
  })
}

function sendListOfUploadedFilespCloudResults(res) {
  let uploadDir = path.join(__dirname, 'EPLAS/results');
  fs.readdir(uploadDir, (err, files) => {
    if (err) {
      console.log(err);
      res.writeHead(400, {
        'Content-Type': 'application/json'
      });
      res.write(JSON.stringify(err.message));
      res.end();
    } else {
      res.writeHead(200, {
        'Content-Type': 'application/json'
      });
      res.write(JSON.stringify(files));
      res.end();
    }
  })
}

function sendListOfUploadedFilespCloudWaiting(res) {
  let uploadDir = path.join(__dirname, 'EPLAS/jobStatus/waiting');
  fs.readdir(uploadDir, (err, files) => {
    if (err) {
      console.log(err);
      res.writeHead(400, {
        'Content-Type': 'application/json'
      });
      res.write(JSON.stringify(err.message));
      res.end();
    } else {
      res.writeHead(200, {
        'Content-Type': 'application/json'
      });
      res.write(JSON.stringify(files));
      res.end();
    }
  })
}

function sendListOfUploadedFilespCloudRunning(res) {
  let uploadDir = path.join(__dirname, 'EPLAS/jobStatus/running');
  fs.readdir(uploadDir, (err, files) => {
    if (err) {
      console.log(err);
      res.writeHead(400, {
        'Content-Type': 'application/json'
      });
      res.write(JSON.stringify(err.message));
      res.end();
    } else {
      res.writeHead(200, {
        'Content-Type': 'application/json'
      });
      res.write(JSON.stringify(files));
      res.end();
    }
  })
}

function sendListOfUploadedFilespCloudFinished(res) {
  let uploadDir = path.join(__dirname, 'EPLAS/jobStatus/finished');
  fs.readdir(uploadDir, (err, files) => {
    if (err) {
      console.log(err);
      res.writeHead(400, {
        'Content-Type': 'application/json'
      });
      res.write(JSON.stringify(err.message));
      res.end();
    } else {
      res.writeHead(200, {
        'Content-Type': 'application/json'
      });
      res.write(JSON.stringify(files));
      res.end();
    }
  })
}
function sendListOfUploadedFilesFTP(res) {
  let uploadDir = path.join(__dirname, 'APLAS/newJobs');
  fs.readdir(uploadDir, (err, files) => {
    if (err) {
      console.log(err);
      res.writeHead(400, {
        'Content-Type': 'application/json'
      });
      res.write(JSON.stringify(err.message));
      res.end();
    } else {
      res.writeHead(200, {
        'Content-Type': 'application/json'
      });
      res.write(JSON.stringify(files));
      res.end();
    }
  })
}

function sendListOfUploadedFilesFTPResults(res) {
  let uploadDir = path.join(__dirname, 'APLAS/results');
  fs.readdir(uploadDir, (err, files) => {
    if (err) {
      console.log(err);
      res.writeHead(400, {
        'Content-Type': 'application/json'
      });
      res.write(JSON.stringify(err.message));
      res.end();
    } else {
      res.writeHead(200, {
        'Content-Type': 'application/json'
      });
      res.write(JSON.stringify(files));
      res.end();
    }
  })
}

function sendListOfUploadedFilesFTPWaiting(res) {
  let uploadDir = path.join(__dirname, 'APLAS/jobStatus/waiting');
  fs.readdir(uploadDir, (err, files) => {
    if (err) {
      console.log(err);
      res.writeHead(400, {
        'Content-Type': 'application/json'
      });
      res.write(JSON.stringify(err.message));
      res.end();
    } else {
      res.writeHead(200, {
        'Content-Type': 'application/json'
      });
      res.write(JSON.stringify(files));
      res.end();
    }
  })
}

function sendListOfUploadedFilesFTPRunning(res) {
  let uploadDir = path.join(__dirname, 'APLAS/jobStatus/running');
  fs.readdir(uploadDir, (err, files) => {
    if (err) {
      console.log(err);
      res.writeHead(400, {
        'Content-Type': 'application/json'
      });
      res.write(JSON.stringify(err.message));
      res.end();
    } else {
      res.writeHead(200, {
        'Content-Type': 'application/json'
      });
      res.write(JSON.stringify(files));
      res.end();
    }
  })
}

function sendListOfUploadedFilesFTPFinished(res) {
  let uploadDir = path.join(__dirname, 'APLAS/jobStatus/finished');
  fs.readdir(uploadDir, (err, files) => {
    if (err) {
      console.log(err);
      res.writeHead(400, {
        'Content-Type': 'application/json'
      });
      res.write(JSON.stringify(err.message));
      res.end();
    } else {
      res.writeHead(200, {
        'Content-Type': 'application/json'
      });
      res.write(JSON.stringify(files));
      res.end();
    }
  })
}

function sendListOfUploadedFileslocalResults(res) {
  let uploadDir = path.join(__dirname, 'local_user/results');
  fs.readdir(uploadDir, (err, files) => {
    if (err) {
      console.log(err);
      res.writeHead(400, {
        'Content-Type': 'application/json'
      });
      res.write(JSON.stringify(err.message));
      res.end();
    } else {
      res.writeHead(200, {
        'Content-Type': 'application/json'
      });
      res.write(JSON.stringify(files));
      res.end();
    }
  })
}

function sendListOfUploadedFileslocalWaiting(res) {
  let uploadDir = path.join(__dirname, 'local_user/jobStatus/waiting');
  fs.readdir(uploadDir, (err, files) => {
    if (err) {
      console.log(err);
      res.writeHead(400, {
        'Content-Type': 'application/json'
      });
      res.write(JSON.stringify(err.message));
      res.end();
    } else {
      res.writeHead(200, {
        'Content-Type': 'application/json'
      });
      res.write(JSON.stringify(files));
      res.end();
    }
  })
}

function sendListOfUploadedFileslocalRunning(res) {
  let uploadDir = path.join(__dirname, 'local_user/jobStatus/running');
  fs.readdir(uploadDir, (err, files) => {
    if (err) {
      console.log(err);
      res.writeHead(400, {
        'Content-Type': 'application/json'
      });
      res.write(JSON.stringify(err.message));
      res.end();
    } else {
      res.writeHead(200, {
        'Content-Type': 'application/json'
      });
      res.write(JSON.stringify(files));
      res.end();
    }
  })
}

function sendListOfUploadedFileslocalFinished(res) {
  let uploadDir = path.join(__dirname, 'local_user/jobStatus/finished');
  fs.readdir(uploadDir, (err, files) => {
    if (err) {
      console.log(err);
      res.writeHead(400, {
        'Content-Type': 'application/json'
      });
      res.write(JSON.stringify(err.message));
      res.end();
    } else {
      res.writeHead(200, {
        'Content-Type': 'application/json'
      });
      res.write(JSON.stringify(files));
      res.end();
    }
  })
}

function sendUploadedFile(url, res) {
  let file = path.join(__dirname, url);
  fs.readFile(file, (err, content) => {
    if (err) {
      res.writeHead(404, {
        'Content-Type': 'text'
      });
      res.write('File Not Found!');
      res.end();
    } else {
      res.writeHead(200, {
        'Content-Type': 'application/octet-stream'
      });
      res.write(content);
      res.end();
    }
  })
}


function saveUploadedFile(req, res) {
  console.log('saving uploaded file');
  let fileName = path.basename(req.url);
  let file = path.join(__dirname, 'local_user/newJobs', fileName)
  req.pipe(fs.createWriteStream(file));
  req.on('end', () => {
    res.writeHead(200, {
      'Content-Type': 'text'
    });
    res.write('uploaded succesfully');
    res.end();
  })
}

function executeUploadedFile(req, res) {
  console.log('executing uploaded file');
  let fileName = path.basename(req.url);
  let file = path.join(__dirname, 'local_user/newJobs', fileName)
  req.pipe(fs.createWriteStream(file));
  req.on('end', () => {
    res.writeHead(200, {
      'Content-Type': 'text'
    });
    res.write('Executing.....');
    res.end();
  })
  var delayInMilliseconds = 30000; //1 second
  let {
    PythonShell
  } = require('python-shell')
  setTimeout(function () {
    //the following line calls the UPC master program so you will see the error when you click the last job button(that time you don't consider UPC master side.)
    PythonShell.run('/home/heinhtet/Desktop/Systematic-1/new_complete/UPC_test/migratetesta.py', null, function (err) {
      if (err) throw err;
      console.log('finished');
    });
  }, delayInMilliseconds);
  let pyshell = new PythonShell('script1.py');

  // sends a message to the Python script via stdin
  pyshell.send('hello');

  pyshell.on('message', function (message) {
    // received a message sent from the Python script (a simple "print" statement)
    console.log(message);
  });

  // end the input stream and allow the process to exit
  pyshell.end(function (err, code, signal) {
    if (err) throw err;
    console.log('The exit code was: ' + code);
    console.log('The exit signal was: ' + signal);
    console.log('finished');
  });
  console.log('executing uploaded file 2nd');
}

function sendInvalidRequest(res) {
  res.writeHead(400, {
    'Content-Type': 'application/json'
  });
  res.write('Invalid Request');
  res.end();
}

function checkPcloudNewJobs() {
  console.log("start")
  schedule.scheduleJob('0,30 * * * * *', () => {
    console.log('checking folder:' + new Date());
    var newJobsFolder = pcloudCLient.listFolder("/EPLAS/newJobs");
    var file
    var jobArrLength = newJobsFolder.metadata.contents.length;
    if (jobArrLength != 0) {
      for (var i = 0; i < jobArrLength; i++) {
        file = newJobsFolder.metadata.contents[i]
        //move file to running folder
        console.log("moving file")
        toPath = "/EPLAS/jobStatus/running/" + file.name;
        pcloudCLient.moveFile(file.path, toPath);
        file.path = toPath
        //download file
        console.log("downloading file")
        var fileLink = pcloudCLient.getFileLink(file.path)
        pcloudCLient.downloadFile(fileLink, file.name)
      }
    } else {
      console.log('folder is null')
    }
  });
}


function checkPcloudResults() {
  schedule.scheduleJob('0,30 * * * * *', () => {
    var resultsFolder = "/home/upc_web_server/Desktop/UPC-System-sam/EPLAS/results/"
    if (resultsFolder != null) {
      //upload result file
      console.log("uploading file")
      var localResultsFile = {
        name: "aa.txt",
        path: "/home/upc_web_server/Desktop/UPC-System-sam/EPLAS/results/aa.txt"
      }
      var cloudFilePath = '/EPLAS/results'
      pcloudCLient.uploadFile(localResultsFile.name, localResultsFile.path, cloudFilePath)
      //move file to finished folder
      console.log("moving file")
      toPath = "/EPLAS/jobStatus/finished/" + localResultsFile.name;
      pcloudCLient.moveFile(localResultsFile.path, toPath);
      console.log("finished")
    }
  })
}

function checkSSHFSNewJobs() {
  console.log("[checkSSHFSNewJobs] start")
  var folderPath = "/home/upc_web_server/Desktop/UPC-System-sam/APLAS/newJobs";

  schedule.scheduleJob('0,30 * * * * *', () => {
    console.log('[checkSSHFSNewJobs] checking folder:' + new Date());
    var files = fs.readdirSync(folderPath).map(fileName => {
      return path.join(folderPath, fileName)
    })
    if (files.length != 0) {
      for (var i = 0; i < files.length; i++) {
        var file = files[i]
        //move file to running folder
        console.log("moving file")
        toPath = file.replace("newJobs", "jobStatus/running")
        fs.renameSync(file, toPath)
        //sending file to upc master
        console.log("sending file")
      }
    } else {
      console.log('folder is null')
    }
  });
}
