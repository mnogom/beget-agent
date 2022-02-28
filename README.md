# Beget (SFTP) agent

---
### Installation
```commandline
pip3 install --upgrade git+https://github.com/mnogom/beget-agent.git
```

---
### Usage
Command line
```commandline
usage: beag [-h] {restart,put} ...

Beget SFTP agent

positional arguments:
  {restart,put}
    restart      Restart server. Store "./tmp/restart.txt"
    put          Put files to server

optional arguments:
  -h, --help     show this help message and exit
```

---
### Features
1. Upload folders using **-r** flag
2. Upload all files using **-a** flag
3. Upload files from git index (intersection your files with index) using **-i** flag