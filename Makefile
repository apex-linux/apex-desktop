# SPDX-License-Identifier: GPL-3.0-or-later
#
# GNU make. packaging/apex-desktop.spec installs the files; this file checks them and
# builds the RPM from git HEAD.

RPMBUILD ?= rpmbuild
# rpms.sh reads the RPMs from target/rpm.
BUILD_DIR ?= target

DESKTOP_XML := desktop/schemas/io.github.apex_linux.Apex.Desktop.gschema.xml \
	desktop/keybindings/60-apex.xml desktop/wallpapers/apex-facets.xml \
	desktop/fontconfig/60-apex-adwaita-sans-ss03.conf $(wildcard desktop/plymouth/art/*.svg)
CHECK_DIR := $(abspath $(BUILD_DIR))/check-data
PLACES_INPUTS := desktop/icons/places/folder.svg desktop/icons/places/emblems desktop/icons/accents
MIMETYPES_INPUTS := desktop/icons/mimetypes/file.svg desktop/icons/mimetypes/kinds \
	desktop/icons/mimetypes/types
COLLOID_GIT := $(abspath $(BUILD_DIR))/colloid.git
COLLOID_URL := https://github.com/vinceliuice/Colloid-icon-theme.git
# Only the full-colour app icons and the licence; the spec's colloid_sha256 covers this list.
COLLOID_PATHS := LICENSE src/apps/scalable links/apps/scalable

# The = variables expand lazily, so git and sed run only when a target needs them.
SPEC        := packaging/apex-desktop.spec
RPM_TOPDIR  := $(abspath $(BUILD_DIR))/rpm
VERSION      = $(shell sed -n 's/^Version:[[:space:]]*//p' $(SPEC))
COMMITDATE   = $(shell TZ=UTC git log -1 --format=%cd --date=format-local:%Y%m%d HEAD 2>/dev/null)
SHORTCOMMIT  = $(shell git rev-parse --short=12 HEAD 2>/dev/null)
COLLOID_COMMIT = $(shell sed -n 's/^%global colloid_commit[[:space:]]*//p' $(SPEC))
RPMBUILD_FLAGS ?=

.PHONY: all check-data rpm clean help
.DELETE_ON_ERROR:

all: help

help:
	@echo 'make check-data   xmllint, glib-compile-schemas --strict, dconf compile and the icon theme'
	@echo '                  check on desktop/, the tmpfiles entry, and the Plymouth themes: built, checked and,'
	@echo '                  as root in a container, rendered headless into $(CHECK_DIR)/plymouth-frames'
	@echo '                  (validators that are not installed are skipped)'
	@echo 'make rpm          the apex-desktop SRPM and RPM from git HEAD, into $(RPM_TOPDIR)'
	@echo 'make clean        remove $(RPM_TOPDIR), $(CHECK_DIR) and $(COLLOID_GIT)'

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
	@if command -v glib-compile-schemas >/dev/null 2>&1 && command -v gsettings >/dev/null 2>&1 && \
		command -v xmllint >/dev/null 2>&1; then \
		echo ".github/scripts/disabled-features-check.sh"; \
		.github/scripts/disabled-features-check.sh; \
	else \
		echo "skip: glib-compile-schemas, gsettings or xmllint not found, so no disabled-features check (Fedora: glib2 libxml2)"; \
	fi
	@if command -v dconf >/dev/null 2>&1; then \
		mkdir -p '$(CHECK_DIR)'; \
		echo "dconf compile $(CHECK_DIR)/distro desktop/dconf/distro.d"; \
		dconf compile '$(CHECK_DIR)/distro' desktop/dconf/distro.d; \
	else \
		echo "skip: dconf not found (Fedora: dconf)"; \
	fi
	@if command -v xmllint >/dev/null 2>&1; then \
		rm -rf '$(CHECK_DIR)/Apex' '$(CHECK_DIR)'/Apex-* && mkdir -p '$(CHECK_DIR)/Apex/symbolic'; \
		cp desktop/icons/index.theme '$(CHECK_DIR)/Apex/'; \
		echo "xmllint --noout --nonet desktop/icons/symbolic/*.svg"; \
		xmllint --noout --nonet desktop/icons/symbolic/*.svg; \
		src=; \
		if command -v inkscape >/dev/null 2>&1; then \
			src=desktop/icons/symbolic; \
			for f in desktop/icons/symbolic/*.svg; do \
				n=$${f##*/}; \
				bash desktop/icons/fill-strokes.sh "$$f" "$(CHECK_DIR)/Apex/symbolic/$${n%.svg}-symbolic.svg" || exit 1; \
			done; \
		else \
			echo "skip: inkscape not found (Fedora: inkscape); the theme has no symbolic icons"; \
		fi; \
		echo "bash desktop/icons/build-places.sh $(CHECK_DIR) $(PLACES_INPUTS)"; \
		bash desktop/icons/build-places.sh '$(CHECK_DIR)' $(PLACES_INPUTS) || exit 1; \
		mime=; \
		if command -v inkscape >/dev/null 2>&1 && fc-list 'Adwaita Sans' family 2>/dev/null | grep -q .; then \
			mime=1; \
			echo "bash desktop/icons/build-mimetypes.sh $(CHECK_DIR) $(MIMETYPES_INPUTS)"; \
			bash desktop/icons/build-mimetypes.sh '$(CHECK_DIR)' $(MIMETYPES_INPUTS) || exit 1; \
		else \
			echo "skip: inkscape or Adwaita Sans not found, so no file icons (Fedora: inkscape adwaita-sans-fonts)"; \
		fi; \
		echo "bash desktop/icons/check-theme.sh $(CHECK_DIR)/Apex $$src"; \
		bash desktop/icons/check-theme.sh '$(CHECK_DIR)/Apex' $$src || exit 1; \
		for t in '$(CHECK_DIR)'/Apex-*; do \
			bash desktop/icons/check-theme.sh "$$t" >/dev/null || exit 1; \
		done; \
		echo "check-theme: the nine Apex-<accent> themes pass"; \
		if python3 -c 'import gi; gi.require_version("Gtk", "4.0"); from gi.repository import Gtk' 2>/dev/null; then \
			echo ".github/scripts/places-check.py $(CHECK_DIR)"; \
			python3 .github/scripts/places-check.py '$(CHECK_DIR)' || exit 1; \
			if [ -n "$$mime" ]; then \
				echo ".github/scripts/mimetypes-check.py $(CHECK_DIR)"; \
				python3 .github/scripts/mimetypes-check.py '$(CHECK_DIR)' || exit 1; \
			fi; \
		else \
			echo "skip: no GTK 4 for Python, so no folder lookup check (Fedora: python3-gobject gtk4)"; \
		fi; \
	else \
		echo "skip: xmllint not found, so no icon theme check (Fedora: libxml2)"; \
	fi
	@if command -v rsvg-convert >/dev/null 2>&1; then \
		mkdir -p '$(CHECK_DIR)/greeter'; \
		for v in light dark; do \
			echo "rsvg-convert -w 2880 -h 1800 desktop/wallpapers/apex-greeter-$$v.svg"; \
			rsvg-convert -w 2880 -h 1800 -o "$(CHECK_DIR)/greeter/apex-greeter-$$v.png" \
				"desktop/wallpapers/apex-greeter-$$v.svg" || exit 1; \
		done; \
		bash desktop/wallpapers/check-greeter.sh '$(CHECK_DIR)/greeter' || exit 1; \
	else \
		echo "skip: rsvg-convert not found, so no greeter backgrounds (Fedora: librsvg2-tools)"; \
	fi
	@fedora=$$(rpm -E %fedora 2>/dev/null); \
	if command -v inkscape >/dev/null 2>&1 && fc-list 'Adwaita Sans' family 2>/dev/null | grep -q . && \
		[ "$$fedora" -eq "$$fedora" ] 2>/dev/null; then \
		echo "bash desktop/gdm/build-logo.sh $(CHECK_DIR)/apex-gdm-logo.svg desktop/gdm/logo.svg $$fedora"; \
		bash desktop/gdm/build-logo.sh '$(CHECK_DIR)/apex-gdm-logo.svg' desktop/gdm/logo.svg "$$fedora" || exit 1; \
		xmllint --noout --nonet '$(CHECK_DIR)/apex-gdm-logo.svg' || exit 1; \
	else \
		echo "skip: inkscape, Adwaita Sans or rpm's %fedora missing, so no gdm logo (Fedora: inkscape adwaita-sans-fonts)"; \
	fi
	@if command -v glib-compile-schemas >/dev/null 2>&1 && command -v gsettings >/dev/null 2>&1; then \
		echo ".github/scripts/gdm-logo-check.sh"; \
		.github/scripts/gdm-logo-check.sh; \
	else \
		echo "skip: glib-compile-schemas or gsettings not found, so no gdm logo key check (Fedora: glib2)"; \
	fi
	@if ! command -v systemd-tmpfiles >/dev/null 2>&1; then \
		echo "skip: systemd-tmpfiles not found (Fedora: systemd)"; \
	elif [ "$$(id -u)" != 0 ]; then \
		echo "skip: the tmpfiles check runs as root only (it applies root-owned entries)"; \
	else \
		echo ".github/scripts/tmpfiles-check.sh"; \
		.github/scripts/tmpfiles-check.sh; \
	fi
	@if command -v rsvg-convert >/dev/null 2>&1 && command -v fc-list >/dev/null 2>&1 && \
		fc-list 'Adwaita Sans' family | grep -q .; then \
		rm -rf '$(CHECK_DIR)/plymouth' && \
		echo "bash desktop/plymouth/build.sh $(CHECK_DIR)/plymouth desktop/plymouth/art/*.svg" && \
		bash desktop/plymouth/build.sh '$(CHECK_DIR)/plymouth' desktop/plymouth/art/*.svg && \
		echo "bash desktop/plymouth/check-theme.sh $(CHECK_DIR)/plymouth" && \
		bash desktop/plymouth/check-theme.sh '$(CHECK_DIR)/plymouth' || exit 1; \
		if [ "$$(id -u)" != 0 ] || { [ ! -e /.dockerenv ] && [ ! -e /run/.containerenv ]; }; then \
			echo "skip: the Plymouth preview runs as root in a container only"; \
		elif ! command -v plymouthd >/dev/null 2>&1 || ! ls /usr/lib*/plymouth/renderers/x11.so >/dev/null 2>&1 || \
			! command -v Xvfb >/dev/null 2>&1 || \
			! command -v xdotool >/dev/null 2>&1 || ! command -v xwdtopnm >/dev/null 2>&1; then \
			echo "skip: no Plymouth preview (Fedora: plymouth-plugin-script plymouth-plugin-two-step plymouth-devel xorg-x11-server-Xvfb xwd xdotool netpbm-progs)"; \
		else \
			rm -rf '$(CHECK_DIR)/plymouth-frames'; \
			echo ".github/scripts/plymouth-preview.sh $(CHECK_DIR)/plymouth $(CHECK_DIR)/plymouth-frames"; \
			.github/scripts/plymouth-preview.sh '$(CHECK_DIR)/plymouth' '$(CHECK_DIR)/plymouth-frames'; \
		fi; \
	else \
		echo "skip: rsvg-convert or Adwaita Sans not found, so no Plymouth check (Fedora: librsvg2-tools adwaita-sans-fonts)"; \
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
	git init -q --bare '$(COLLOID_GIT)'
	git -C '$(COLLOID_GIT)' fetch -q --depth 1 '$(COLLOID_URL)' '$(COLLOID_COMMIT)'
	git -C '$(COLLOID_GIT)' archive --format=tar --prefix='Colloid-icon-theme-$(COLLOID_COMMIT)/' \
		-o '$(RPM_TOPDIR)/SOURCES/Colloid-icon-theme-$(COLLOID_COMMIT).tar' '$(COLLOID_COMMIT)' -- $(COLLOID_PATHS)
	$(RPMBUILD) -ba $(SPEC) \
		--define '_topdir $(RPM_TOPDIR)' \
		--define 'commitdate $(COMMITDATE)' \
		--define 'shortcommit $(SHORTCOMMIT)' \
		$(RPMBUILD_FLAGS)

clean:
	rm -rf '$(RPM_TOPDIR)' '$(CHECK_DIR)' '$(COLLOID_GIT)'
