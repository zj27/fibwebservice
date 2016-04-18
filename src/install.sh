#!/bin/sh
chmod +x fibservice.py
cp -f fibservice.py /usr/local/bin/
cp -f conf/fibserver.cfg /etc/
if [ -f /usr/local/bin/fibservice.py ] && [ -f /etc/fibserver.cfg ]; then
    echo "Installtion Complete"
fi
