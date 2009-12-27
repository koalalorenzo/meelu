clean:
	rm -rf build
	
install:
	python setup.py install --record /usr/share/meelu/installed.list
	chmod +x /usr/bin/meelu

uninstall:
	cat /usr/share/meelu/installed.list | xargs rm -rf
	rm -rf /usr/share/meelu
