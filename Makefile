# SPDX-License-Identifier: GPL-3.0-or-later
#
# GNU make. packaging/apex-desktop.spec installs the files; this file checks them and
# builds the RPM from git HEAD.

RPMBUILD ?= rpmbuild
# rpms.sh reads the RPMs from target/rpm.
BUILD_DIR ?= target

DESKTOP_XML := desktop/schemas/io.github.apex_linux.Apex.Desktop.gschema.xml \
	desktop/keybindings/60-apex.xml desktop/wallpapers/apex-facets.xml \
	desktop/fontconfig/60-apex-adwaita-sans-ss03.conf
CHECK_DIR := $(abspath $(BUILD_DIR))/check-data

# The = variables expand lazily, so git and sed run only when a target needs them.
SPEC        := packaging/apex-desktop.spec
RPM_TOPDIR  := $(abspath $(BUILD_DIR))/rpm
VERSION      = $(shell sed -n 's/^Version:[[:space:]]*//p' $(SPEC))
COMMITDATE   = $(shell TZ=UTC git log -1 --format=%cd --date=format-local:%Y%m%d HEAD 2>/dev/null)
SHORTCOMMIT  = $(shell git rev-parse --short=12 HEAD 2>/dev/null)
RPMBUILD_FLAGS ?=

.PHONY: all check-data rpm clean help
.DELETE_ON_ERROR:

all: help

help:
	@echo 'make check-data   xmllint, glib-compile-schemas --strict and dconf compile on desktop/'
	@echo '                  (validators that are not installed are skipped)'
	@echo 'make rpm          the apex-desktop SRPM and RPM from git HEAD, into $(RPM_TOPDIR)'
	@echo 'make clean        remove $(RPM_TOPDIR) and $(CHECK_DIR)'

check-data:
	@if command -v xmllint >/dev/null 2>&1; then \
		echo "xmllint --noout --nonet $(DESKTOP_XML)"; \
		xmllint --noout --nonet $(DESKTOP_XML); \
	else \
		echo "skip: xmllint not found (Fedora: libxml2)"; \
	fi
	@if command -v glib-compile-schemas >/dev/null 2>&1; then \
		echo "glib-compile-schemas --strict --dry-run desktop/schemas"; \
		glib-compile-schemas --strict --dry-run desktop/schemas; \
	else \
		echo "skip: glib-compile-schemas not found (Fedora: glib2)"; \
	fi
	@if command -v dconf >/dev/null 2>&1; then \
		mkdir -p '$(CHECK_DIR)'; \
		echo "dconf compile $(CHECK_DIR)/distro desktop/dconf/distro.d"; \
		dconf compile '$(CHECK_DIR)/distro' desktop/dconf/distro.d; \
	else \
		echo "skip: dconf not found (Fedora: dconf)"; \
	fi

rpm:
	@if [ -z '$(SHORTCOMMIT)' ]; then \
		echo "error: 'make rpm' packages git HEAD, and this checkout has no commit" >&2; \
		exit 1; \
	fi
	@git diff --quiet HEAD -- desktop $(SPEC) LICENSE 2>/dev/null || \
		echo "warning: the RPM is built from HEAD; uncommitted changes are not included" >&2
	mkdir -p '$(RPM_TOPDIR)/SOURCES'
	git archive --format=tar.gz --prefix='apex-desktop-$(VERSION)/' \
		-o '$(RPM_TOPDIR)/SOURCES/apex-desktop-$(VERSION).tar.gz' HEAD -- desktop LICENSE
	$(RPMBUILD) -ba $(SPEC) \
		--define '_topdir $(RPM_TOPDIR)' \
		--define 'commitdate $(COMMITDATE)' \
		--define 'shortcommit $(SHORTCOMMIT)' \
		$(RPMBUILD_FLAGS)

clean:
	rm -rf '$(RPM_TOPDIR)' '$(CHECK_DIR)'
