const fs = require('fs');
const axios = require('axios');

function handleOutput(writeFrom, writeTo) {
    if (out) {
        fs.writeFile(writeTo, writeFrom, 'utf8', function(err) {
            if (err) {
                console.error(err);
                process.exit(1);
            }
        });
    } else {
        console.log(writeFrom);
    }
}

async function cat(path, out) {
    fs.readFile(path, 'utf8', (err, data) => {
      if (err) {
        console.error(`Error reading ${path}: ${err}`);
      } 
      handleOutput(data, out);
      
    });
}

async function webCat(url, out) {
    try {
        let read_file = await axios.get(url);
        handleOutput(resp.data, out)
    } catch (err) {
        console.error(`Error reading ${url}: ${err}`);
    }   
}

if (process.argv.length === 5 && process.argv[2] === '--out') {
    out = process.argv[3];
    path = process.argv[4];
  } else {
    path = process.argv[2];
  }
if (path.slice(0,4) === 'http') {
    webCat(path, out);
} else {
    cat(path, out);
}