const fs = require('fs');

function cat(path) {
  fs.readFile(path, 'utf8', (err, data) => {
    if (err) {
      console.error(`Error reading ${path}: ${err}`);
    } 
    console.log(data);
  });
}

if (process.argv.length !== 3) {
  console.log('Usage: node step1.js <file_path>');
} else {
  const filePath = process.argv[2];
  cat(filePath);
}
