ANACONDADATADIR = /usr/share/anaconda
ANACONDABOOTDIR = $(ANACONDADATADIR)/boot

all: 
	@echo "Nothing to do."

splash.lss: syslinux-splash.png
	./splashtolss.sh syslinux-splash.png splash.lss

install: splash.lss
	@if [ "$(DESTDIR)" = "" ]; then \
		echo " "; \
		echo "ERROR: A destdir is required"; \
		exit 1; \
	fi

	mkdir -p $(DESTDIR)/$(ANACONDADATADIR)
	mkdir -p $(DESTDIR)/$(ANACONDABOOTDIR)
	mkdir -p $(DESTDIR)/$(ANACONDADATADIR)/pixmaps
	install -m 644 anaconda_header.png $(DESTDIR)/$(ANACONDADATADIR)/pixmaps
	install -m 644 progress_first.png $(DESTDIR)/$(ANACONDADATADIR)/pixmaps
	install -m 644 splash.png $(DESTDIR)/$(ANACONDADATADIR)/pixmaps

	install -m 644 splash.lss $(DESTDIR)/$(ANACONDABOOTDIR)
	install -m 644 syslinux-splash.png $(DESTDIR)/$(ANACONDABOOTDIR)/syslinux-splash.png
	# install -m 755 splashtolss.sh $(DESTDIR)/$(ANACONDADATADIR)
	install -m 644 syslinux-vesa-splash.jpg $(DESTDIR)/$(ANACONDABOOTDIR)

clean:
	rm -f splash.lss
