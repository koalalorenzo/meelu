clean:
	rm -rf build
	
install:
	python setup.py install --prefix=/usr --record /usr/share/meelu/installed.list
	ln -s /usr/lib/python2.6/site-packages/libmeelu.py /usr/lib/python2.6/libmeelu.py
	chmod +x /usr/bin/meelu

uninstall:
	cat /usr/share/meelu/installed.list | xargs rm -rf
	rm /usr/lib/python2.6/libmeelu.py
	rm -rf /usr/share/meelu
