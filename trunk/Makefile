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

ubuntu: build
	python setup.py install --prefix=/usr --root=./Meelu/
	mv ./Meelu/usr/lib/python2.6/site-packages/libmeelu.py ./Meelu/usr/lib/python2.6/libmeelu.py
	rm ./Meelu/usr/lib/python2.6/site-packages/libmeelu.pyc
	rm ./Meelu/usr/lib/python2.6/site-packages/Meelu*
	chmod +x ./Meelu/usr/bin/meelu
	mkdir ./Meelu/DEBIAN
	touch ./Meelu/DEBIAN/control
	echo "Package: meelu" >> ./Meelu/DEBIAN/control
	echo "Version: 0.6" >> ./Meelu/DEBIAN/control 
	echo "Architecture: all" >> ./Meelu/DEBIAN/control
	echo "Depends: python (>= 2.6), python-sqlite, python-notify, python-glade2, python-gtk2, python-webkit" >> ./Meelu/DEBIAN/control
	echo "Maintainer: Lorenzo Setale <koalalorenzo@gmail.com>" >> ./Meelu/DEBIAN/control
	echo "Description: Meelu: The Meemi Client" >> ./Meelu/DEBIAN/control
	echo " Questo pacchetto contiene Meelu, un Client che permette" >> ./Meelu/DEBIAN/control
	echo " di accedere al social network Meemi senza aprire un" >> ./Meelu/DEBIAN/control
	echo " web browser." >> ./Meelu/DEBIAN/control
	dpkg-deb -b Meelu

debian: build
	python setup.py install --prefix=/usr --root=./Meelu/
	mv ./Meelu/usr/lib/python2.5/site-packages/libmeelu.py ./Meelu/usr/lib/python2.5/libmeelu.py
	rm ./Meelu/usr/lib/python2.5/site-packages/libmeelu.pyc
	rm ./Meelu/usr/lib/python2.5/site-packages/Meelu*
	chmod +x ./Meelu/usr/bin/meelu
	mkdir ./Meelu/DEBIAN
	touch ./Meelu/DEBIAN/control
	echo "Package: meelu" >> ./Meelu/DEBIAN/control
	echo "Version: 0.6" >> ./Meelu/DEBIAN/control 
	echo "Architecture: all" >> ./Meelu/DEBIAN/control
	echo "Depends: python (>= 2.5), python-sqlite, python-notify, python-glade2, python-gtk2, python-webkit" >> ./Meelu/DEBIAN/control
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
