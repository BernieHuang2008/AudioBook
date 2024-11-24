#!/bin/bash

# copy & chmod
cp service/xread.service /etc/systemd/system/xread
chmod 644 /etc/systemd/system/xread.service

# reload systemd
systemctl daemon-reload

# enable auto-start
systemctl enable xread

# run
systemctl start your_service
systemctl stop your_service
systemctl status your_service