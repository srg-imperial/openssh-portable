SH     = $(shell which sh)
PWD    = $(shell pwd)

# Varan
VX     = $(shell which vx)

# Compilers
GCC    = $(shell which gcc)
CLANG  = $(shell which clang)

# SSH config flags
SSH_CFG_FLAGS=--without-pie --without-hardening

# For debugging
SSH_CFG_FLAGS=--disable-strip
CFLAGS = -O0 -g

# Where each version expects to be installed
INSTALL_DIR       = $(PWD)/install
INSTALL_BUILD_DIR = $(INSTALL_DIR)/ssh

# Location of ssh_config file
SSH_CONFIG=$(INSTALL_BUILD_DIR)/etc/ssh_config

# Where different versions are installed
INSTALL_GCC        = $(INSTALL_DIR)/gcc-system
INSTALL_GCC_ASAN   = $(INSTALL_DIR)/gcc-asan-system
INSTALL_CLANG      = $(INSTALL_DIR)/clang-system
INSTALL_CLANG_ASAN = $(INSTALL_DIR)/clang-asan-system

# Binaries inside each build directory
SSH_GCC        = $(INSTALL_GCC)/bin/ssh
SSH_GCC_ASAN   = $(INSTALL_GCC_ASAN)/bin/ssh
SSH_CLANG      = $(INSTALL_CLANG)/bin/ssh
SSH_CLANG_ASAN = $(INSTALL_CLANG_ASAN)/bin/ssh

# Script to run SSH with Varan
SSH_DIR = $(PWD)/bin
SSH     = $(SSH_DIR)/ssh

# Command lines to run SSH with Varan inside script
RUN_GCC_GCC          =                              $(VX) $(SSH_GCC) $(SSH_GCC)          -- \$$@
RUN_GCC_GCC_ASAN     = ASAN_OPTIONS="handle_segv=0" $(VX) $(SSH_GCC) $(SSH_GCC_ASAN)     -- \$$@
RUN_CLANG_CLANG      =                              $(VX) $(SSH_CLANG) $(SSH_CLANG)      -- \$$@
RUN_CLANG_CLANG_ASAN = ASAN_OPTIONS="handle_segv=0" $(VX) $(SSH_CLANG) $(SSH_CLANG_ASAN) -- \$$@

# Main target
all: vx-gcc-gcc_asan

# ==============================================================================
# GCC targets
# ==============================================================================

# Set up script for native leader and native follower built with gcc
vx-gcc-gcc: $(SSH_GCC)
	rm -rf $(INSTALL_BUILD_DIR) || true
	cp -r $(INSTALL_GCC) $(INSTALL_BUILD_DIR)
	rm -rf $(SSH_DIR) || true
	mkdir -p $(SSH_DIR)
	echo "#!$(SH)"        >  $(SSH)
	echo "$(RUN_GCC_GCC)" >> $(SSH)
	chmod a+x $(SSH)

# Set up script for native leader and sanitized follower built with gcc
vx-gcc-gcc_asan: $(SSH_GCC) $(SSH_GCC_ASAN)
	rm -rf $(INSTALL_BUILD_DIR) || true
	cp -r $(INSTALL_GCC) $(INSTALL_BUILD_DIR)
	rm -rf $(SSH_DIR) || true
	mkdir -p $(SSH_DIR)
	echo "#!$(SH)"             >  $(SSH)
	echo "$(RUN_GCC_GCC_ASAN)" >> $(SSH)
	chmod a+x $(SSH)

# Build using gcc and no sanitization
$(SSH_GCC):
	rm -rf $(INSTALL_BUILD_DIR) || true
	make -C .. clean || true
	cd .. ; autoconf || true
	cd .. ; autoheader || true
	cd .. ; CC=$(GCC)             \
  	CFLAGS="$(CFLAGS)"            \
  	./configure                   \
  	$(SSH_CFG_FLAGS)              \
  	--prefix=$(INSTALL_BUILD_DIR) \
	--with-privsep-path=$(INSTALL_BUILD_DIR)/var/empty
	make -C ..
	make -C .. install
	echo "" > $(SSH_CONFIG)
	rm -rf $(INSTALL_GCC) || true
	mv $(INSTALL_BUILD_DIR) $(INSTALL_GCC)

# Build using gcc and sanitization
$(SSH_GCC_ASAN):
	rm -rf $(INSTALL_BUILD_DIR) || true
	make -C .. clean || true
	cd .. ; autoconf || true
	cd .. ; autoheader || true
	cd .. ; CC=$(GCC)                     \
  	CFLAGS="$(CFLAGS) -fsanitize=address" \
  	LDFLAGS="-fsanitize=address -ldl"     \
  	./configure                           \
  	$(SSH_CFG_FLAGS)                      \
  	--prefix=$(INSTALL_BUILD_DIR)         \
	--with-privsep-path=$(INSTALL_BUILD_DIR)/var/empty
	make -C ..
	make -C .. install
	echo "" > $(SSH_CONFIG)
	rm -rf $(INSTALL_GCC_ASAN) || true
	mv $(INSTALL_BUILD_DIR) $(INSTALL_GCC_ASAN)

# ==============================================================================
# CLANG targets
# ==============================================================================

# Set up script for native leader and native follower built with clang
vx-clang-clang: $(SSH_CLANG)
	rm -rf $(INSTALL_BUILD_DIR) || true
	cp -r $(INSTALL_CLANG) $(INSTALL_BUILD_DIR)
	rm -rf $(SSH_DIR) || true
	mkdir -p $(SSH_DIR)
	echo "#!$(SH)"            >  $(SSH)
	echo "$(RUN_CLANG_CLANG)" >> $(SSH)
	chmod a+x $(SSH)

# Set up script for native leader and sanitized follower built with clang
vx-clang-clang_asan: $(SSH_CLANG) $(SSH_CLANG_ASAN)
	rm -rf $(INSTALL_BUILD_DIR) || true
	cp -r $(INSTALL_CLANG) $(INSTALL_BUILD_DIR)
	rm -rf $(SSH_DIR) || true
	mkdir -p $(SSH_DIR)
	echo "#!$(SH)"                 >  $(SSH)
	echo "$(RUN_CLANG_CLANG_ASAN)" >> $(SSH)
	chmod a+x $(SSH)

# Build using clang and no sanitization
$(SSH_CLANG):
	rm -rf $(INSTALL_BUILD_DIR) || true
	make -C .. clean || true
	cd .. ; autoconf || true
	cd .. ; autoheader || true
	cd .. ; CC=$(CLANG)           \
  	CFLAGS="$(CFLAGS)"            \
  	./configure                   \
  	$(SSH_CFG_FLAGS)              \
  	--prefix=$(INSTALL_BUILD_DIR) \
	--with-privsep-path=$(INSTALL_BUILD_DIR)/var/empty
	make -C ..
	make -C .. install
	echo "" > $(SSH_CONFIG)
	rm -rf $(INSTALL_CLANG) || true
	mv $(INSTALL_BUILD_DIR) $(INSTALL_CLANG)

# Build using clang and sanitization
$(SSH_CLANG_ASAN):
	rm -rf $(INSTALL_BUILD_DIR) || true
	make -C .. clean || true
	cd .. ; autoconf || true
	cd .. ; autoheader || true
	cd .. ; CC=$(CLANG)                   \
  	CFLAGS="$(CFLAGS) -fsanitize=address" \
  	LDFLAGS="-fsanitize=address -ldl"     \
  	./configure                           \
  	$(SSH_CFG_FLAGS)                      \
  	--prefix=$(INSTALL_BUILD_DIR)         \
	--with-privsep-path=$(INSTALL_BUILD_DIR)/var/empty
	make -C ..
	make -C .. install
	echo "" > $(SSH_CONFIG)
	rm -rf $(INSTALL_CLANG_ASAN) || true
	mv $(INSTALL_BUILD_DIR) $(INSTALL_CLANG_ASAN)

# ==============================================================================
# misc targets
# ==============================================================================

clean:
	make -C .. clean || true
	rm -rf $(INSTALL_DIR) || true
	rm -rf $(SSH_DIR) || true
