#!/bin/sh
echo "Building..."
tar -cjvf fibwebservice.tar.bz2 fibservice.py install.sh conf/fibserver.cfg
if [ `echo $?` == 0 ]; then
    md5sum fibwebservice.tar.bz2 > fibwebservice.tar.bz2.md5
    mv -f fibwebservice.tar.bz2 fibwebservice.tar.bz2.md5 ../package
    echo "Succeed"
else
    echo "Failed"
fi
