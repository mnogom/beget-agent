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
### How to use with GitHub Actions:
```yaml
name: python-ci-cd

on:
  push:
    branches:
      - '**'
    tags:
      - '**'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2

      - name: Deploy
        env:
          SFTP_HOST: ${{ secrets.SFTP_HOST }}
          SFTP_PORT: ${{ secrets.SFTP_PORT }}
          SFTP_USERNAME: ${{ secrets.SFTP_USERNAME }}
          SFTP_PASSWORD: ${{ secrets.SFTP_PASSWORD }}
          SFTP_REMOTE_HOME: ${{ secrets.SFTP_REMOTE_HOME }}
        run: |
          pip3 install --upgrade git+https://github.com/mnogom/beget-agent.git
          beag put -rai
          beag restart
```

---
### Features
1. Upload folders using **-r** flag
2. Upload all files using **-a** flag
3. Upload files from git index (intersection your files with index) using **-i** flag