#!/bin/sh
cp fibservice.py /usr/local/bin/
cp conf/fibserver.cfg /etc/
if [ -f /usr/local/bin/fibservice.py ] && [ -f /etc/fibserver.cfg ]; then
    echo "Installtion Complete"
fi
