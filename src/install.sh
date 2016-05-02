#!/bin/sh
chmod +x fibservice.py
cp -f fibservice.py /usr/local/bin/
cp -f conf/fibservice.cfg /etc/
if [ -f /usr/local/bin/fibservice.py ] && [ -f /etc/fibservice.cfg ]; then
    echo "Installtion Complete"
fi
