# Quick Start

## Docker
This is the recommended way for Linux deployment machines.

1. Make sure host `/data` exists, is mounted on the permanent disk, and contains `/data/audio-book/`.
```bash
findmnt /data
ls -ld /data/audio-book
```
2. Build the image from GitHub, so each build pulls the latest `main` code.
```bash
docker build -t audiobook:latest https://github.com/BernieHuang2008/AudioBook.git#main
```
3. Start the container.
```bash
docker run -d \
  --name audiobook \
  --restart unless-stopped \
  -p 5001:5001 \
  -v /data:/data \
  audiobook:latest
```
4. Make sure Docker itself starts on boot.
```bash
sudo systemctl enable --now docker
```

The app keeps using `data_dir = /data/audio-book/`, so data stays under host `/data/audio-book/`.

## Install as Service
If you still want the legacy systemd setup on a Linux server:
1. edit `service/start.sh` and `service/xread.service`, replace the path with the absolute path to `server.py` and `start.sh`
2. run `service/install.sh`
```bash
bash ./service/install.sh
```

