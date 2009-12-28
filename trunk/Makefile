clean:
	rm -rf ./build
	rm -rf ./dist
	rm -rf ./Meelu
	rm -rf ./root
	rm -f ./Meelu.deb
build: clean
	python setup.py build
	
tarball: build
	python setup.py bdist

deb: build
	python setup.py install --prefix=/usr --root=./Meelu/
	mkdir ./Meelu/DEBIAN
	touch ./Meelu/DEBIAN/control
	echo "Package: meelu" >> ./Meelu/DEBIAN/control
	echo "Version: 0.2b" >> ./Meelu/DEBIAN/control 
	echo "Architecture: all" >> ./Meelu/DEBIAN/control
	echo "Depends: python (>= 2.5), python-notify, python-glade2, python-gtk2, python-webkit" >> ./Meelu/DEBIAN/control
	echo "Maintainer: Lorenzo Setale <koalalorenzo@gmail.com>" >> ./Meelu/DEBIAN/control
	echo "Description: Meelu: The Meemi Client" >> ./Meelu/DEBIAN/control
	echo " Questo pacchetto contiene Meelu, un Client che permette" >> ./Meelu/DEBIAN/control
	echo " di accedere al social network Meemi senza aprire un" >> ./Meelu/DEBIAN/control
	echo " web browser." >> ./Meelu/DEBIAN/control
	dpkg-deb -b Meelu

install:
	python setup.py install --prefix=/usr --root=${PREFIX}/
	mv ${PREFIX}/usr/lib/python2.6/site-packages/libmeelu.py ${PREFIX}/usr/lib/python2.6/libmeelu.py
	rm ${PREFIX}/usr/lib/python2.6/site-packages/libmeelu.pyc
	rm ${PREFIX}/usr/lib/python2.6/site-packages/Meelu*
	chmod +x ${PREFIX}/usr/bin/meelu

uninstall:
	rm -rf ${PREFIX}/usr/bin/meelu
	rm ${PREFIX}/usr/lib/python2.6/libmeelu.py
	rm -rf ${PREFIX}/usr/share/meelu
