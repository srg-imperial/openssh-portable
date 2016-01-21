#!/bin/sh

autoconf
autoheader
CC=`which gcc` CFLAGS="-O0 -g" STRIP_SYM="no" ./configure --prefix=/home/lganchin/repos/varan/openssh-portable/install/gcc-system --without-pie --without-hardening
