const fs = require('fs');
const axios = require('axios');

function cat(path) {
    fs.readFile(path, 'utf8', (err, data) => {
      if (err) {
        console.error(`Error reading ${path}: ${err}`);
      } 
      console.log(data);
    });
}


async function webCat(url) {
    try {
        let read_file = await axios.get(url);
        console.log(read_file.data);
    } catch (err) {
        console.error(`Error reading ${url}: ${err}`);
    }   
}

if (process.argv.length !== 3) {
    console.log('Usage: node step[X].js <file_path>');
  } else if (process.argv[2].startsWith('http://') || process.argv[2].startsWith('https://')) {
        webCat(process.argv[2]);
  } else {
        cat(process.argv[2]);
  }


