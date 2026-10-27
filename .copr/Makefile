# COPR-Build-Methode "Make SRPM":
#   make -f .copr/Makefile srpm outdir=<dir> spec=<spec>
top := $(abspath $(dir $(lastword $(MAKEFILE_LIST)))/..)

.PHONY: srpm
srpm:
	dnf -y install rpm-build rpmdevtools
	cd $(top) && spectool -g -C $(top) $(spec)
	cd $(top) && rpmbuild -bs $(spec) \
	    --define "_sourcedir $(top)" \
	    --define "_srcrpmdir $(outdir)"
