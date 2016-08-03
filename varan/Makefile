SH     = $(shell which sh)
PWD    = $(shell pwd)

# Varan
VX     = # Path to vx executable

# Compilers
GCC    = $(shell which gcc)
CLANG  = $(shell which clang)

# Default CFLAGS
CFLAGS = -g -O2 -Wall

# For debugging
#STRIP="--disable-strip"
#CFLAGS = -g -O0 -Wall

SSL_PREFIX = # Prefix of SSL instalation

# Comment to use system SSL
SSL = --with-ssl-dir=$(SSL_PREFIX)       \
	  --includedir=$(SSL_PREFIX)/include \
	  --with-ssl-engine                  \
	  --without-openssl-header-check

# Where each version expects to be installed
INSTALL_DIR       = $(PWD)/install
INSTALL_BUILD_DIR = $(INSTALL_DIR)/openssh

# Where different versions are installed
INSTALL_GCC        = $(PWD)/install/gcc
INSTALL_CLANG      = $(PWD)/install/clang
INSTALL_CLANG_ASAN = $(PWD)/install/clang-asan

# Binaries inside each build directory
OPENSSH_GCC        = $(INSTALL_GCC)/bin/ssh
OPENSSH_GCC_ASAN   = $(INSTALL_GCC_ASAN)/bin/ssh
OPENSSH_CLANG      = $(INSTALL_CLANG)/bin/ssh
OPENSSH_CLANG_ASAN = $(INSTALL_CLANG_ASAN)/bin/ssh
OPENSSH_CLANG_MSAN = $(INSTALL_CLANG_MSAN)/bin/ssh

# Script to run CLANG with Varan
OPENSSH_DIR = $(PWD)/bin
OPENSSH = $(OPENSSH)/redis

# Main target
all: $(OPENSSH_CLANG) $(OPENSSH_CLANG_ASAN) $(OPENSSH_GCC)

# ==============================================================================
# CLANG targets
# ==============================================================================
#
# Build using gcc and no sanitization
$(OPENSSH_GCC):
	rm -rf $(INSTALL_BUILD_DIR) || true
	make -C .. clean || true
	cd .. ; autoconf
	cd .. ; autoheader
	cd .. ; CC=$(GCC)             \
  	CFLAGS="$(CFLAGS)"            \
  	./configure                   \
  	--prefix=$(INSTALL_BUILD_DIR) \
	$(STRIP)                      \
	$(SSL)                        \
	--without-pie                 \
	--without-hardening
	make -C .. V=1
	make -C .. install
	rm -rf $(INSTALL_GCC) || true
	mv $(INSTALL_BUILD_DIR) $(INSTALL_GCC)

# Build using gcc and no sanitization
$(OPENSSH_CLANG):
	rm -rf $(INSTALL_BUILD_DIR) || true
	make -C .. clean || true
	cd .. ; autoconf
	cd .. ; autoheader
	cd .. ; CC=$(CLANG)           \
  	CFLAGS="$(CFLAGS)"            \
  	./configure                   \
  	--prefix=$(INSTALL_BUILD_DIR) \
	$(STRIP)                      \
	$(SSL)                        \
	--without-pie                 \
	--without-hardening
	make -C .. V=1
	make -C .. install
	rm -rf $(INSTALL_CLANG) || true
	mv $(INSTALL_BUILD_DIR) $(INSTALL_CLANG)

# Build using gcc and no sanitization
$(OPENSSH_CLANG_ASAN):
	rm -rf $(INSTALL_BUILD_DIR) || true
	make -C .. clean || true
	cd .. ; autoconf
	cd .. ; autoheader
	cd .. ; CC=$(CLANG)                   \
  	CFLAGS="-fsanitize=address $(CFLAGS)" \
  	LDFLAGS="-fsanitize=address"          \
  	./configure                           \
  	--prefix=$(INSTALL_BUILD_DIR)         \
	$(STRIP)                              \
	$(SSL)                                \
	--without-pie                         \
	--without-hardening
	make -C .. V=1
	make -C .. install
	rm -rf $(INSTALL_CLANG_ASAN) || true
	mv $(INSTALL_BUILD_DIR) $(INSTALL_CLANG_ASAN)

# ==============================================================================
# misc targets
# ==============================================================================

clean:
	make -C .. distclean || true
	rm -rf $(INSTALL_DIR) || true
	rm -rf $(CLANG_DIR) || true
