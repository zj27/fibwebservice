#!/bin/sh
echo "Building..."
tar -cjvf fibwebservice.tar.bz2 fibservice.py install.sh conf/fibserver.cfg
if [ `echo $?` == 0 ]; then
    echo "Succeed"
else
    echo "Failed"
fi
