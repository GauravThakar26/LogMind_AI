const http = require('http');
const fs = require('fs');
const path = require('path');
const port = 3002;

const server = http.createServer((req, res) => {
  if (req.url === '/' || req.url === '/index.html') {
    fs.readFile(path.join(__dirname, 'public', 'index.html'), (err, data) => {
      if (err) {
        res.writeHead(500);
        res.end('Error loading index.html');
        return;
      }
      res.writeHead(200, { 'Content-Type': 'text/html' });
      res.end(data);
    });
  } else {
    // Serve static files
    const filePath = path.join(__dirname, 'public', req.url);
    fs.readFile(filePath, (err, data) => {
      if (err) {
        res.writeHead(404);
        res.end('File not found');
        return;
      }
      res.writeHead(200);
      res.end(data);
    });
  }
});

server.listen(port, () => {
  console.log(`Frontend server running at http://localhost:${port}`);
});