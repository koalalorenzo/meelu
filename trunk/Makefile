clean:
	rm -rf ./build
	rm -rf ./dist
	
build: clean
	python setup.py build
	
tarball: build
	python setup.py bdist
	
install:
	python setup.py install --prefix=/usr --root=${PREFIX} --record ${PREFIX}/usr/share/meelu/installed.list
	ln -s ${PREFIX}/usr/lib/python2.6/site-packages/libmeelu.py ${PREFIX}/usr/lib/python2.6/libmeelu.py
	chmod +x ${PREFIX}/usr/bin/meelu

uninstall:
	cat ${PREFIX}/usr/share/meelu/installed.list | xargs rm -rf
	rm ${PREFIX}/usr/lib/python2.6/libmeelu.py
	rm -rf ${PREFIX}/usr/share/meelu
