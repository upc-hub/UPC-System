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
    var dest = path.join("/Users/SamZHOU/workspace/UPC-System", fileName);
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
  } else if (/\/submit_download\/[^\/]+$/.test(req.url)) {
    sendUploadedFile(req.url, res);
  } else if (/\/upload\/[^\/]+$/.test(req.url)) {
    saveUploadedFile(req, res)
  } else if (/\/execute\/[^\/]+$/.test(req.url)) {
    executeUploadedFile(req, res)
  } else if (req.url == "/start") {
    // checkPcloudNewJobs();
    // checkPcloudResult();
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

function sendListOfUploadedFiles(res) {
  let uploadDir = path.join(__dirname, 'submit_download');
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
  let file = path.join(__dirname, 'submit_download', fileName)
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
  let file = path.join(__dirname, 'submit_download', fileName)
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
    var newJobsFolder = pcloudCLient.listFolder("/APLAS/newJobs");
    var file
    var jobArrLength = newJobsFolder.metadata.contents.length;
    if (jobArrLength != 0) {
      for (var i = 0; i++; i < jobArrLength) {
        file = newJobsFolder.metadata.contents[0]
        //move file to running folder
        console.log("moving file")
        toPath = "/APLAS/jobStatus/running/" + file.name;
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


function checkPcloudResult() {
  schedule.scheduleJob('0,30 * * * * *', () => {
    var resultFolder
    if (resultFolder != null) {
      //upload result file
      console.log("uploading file")
      var localResultFile = {
        name: "resultFile.txt",
        path: "/Users/SamZHOU/workspace/UPC-System/UPC-System-main/resultFile.txt"
      }
      var cloudFilePath = '/APLAS/result'
      pcloudCLient.uploadFile(localResultFile.name, localResultFile.path, cloudFilePath)
      //move file to finished folder
      console.log("moving file")
      toPath = "/APLAS/jobStatus/finished/" + file.name;
      pcloudCLient.moveFile(file.path, toPath);
      console.log("finished")
    }
  })
}

function checkSSHFSNewJobs() {
  console.log("[checkSSHFSNewJobs] start")
  var folderPath = "/Users/SamZHOU/workspace/UPC-System/UPC-Remote/newJobs";

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