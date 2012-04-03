ANACONDADATADIR = /usr/share/anaconda
ANACONDABOOTDIR = $(ANACONDADATADIR)/boot

all: 
	@echo "Nothing to do."

splash.lss: syslinux-splash.png
	./splashtolss.sh syslinux-splash.png splash.lss

install: 
	@if [ "$(DESTDIR)" = "" ]; then \
		echo " "; \
		echo "ERROR: A destdir is required"; \
		exit 1; \
	fi

	mkdir -p $(DESTDIR)/$(ANACONDADATADIR)
	mkdir -p $(DESTDIR)/$(ANACONDABOOTDIR)
	mkdir -p $(DESTDIR)/$(ANACONDADATADIR)/pixmaps
	install -m 644 *.png $(DESTDIR)/$(ANACONDADATADIR)/pixmaps
	install -m 644 splash.png $(DESTDIR)/$(ANACONDADATADIR)/pixmaps/progress_first.png
	install -m 644 splash.png $(DESTDIR)/$(ANACONDADATADIR)/pixmaps/progress_first-lowres.png

	install -m 644 syslinux-vesa-splash.jpg $(DESTDIR)/$(ANACONDABOOTDIR)

clean:
	rm -f splash.lss
