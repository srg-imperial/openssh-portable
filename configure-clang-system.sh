#!/bin/sh

autoconf
autoheader
CC=`which clang` CFLAGS="-O0 -g" STRIP_SYM="no" ./configure --prefix=/home/lganchin/repos/varan/openssh-portable/install/clang-system --without-pie --without-hardening
