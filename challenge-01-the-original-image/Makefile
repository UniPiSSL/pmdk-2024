SHELL := /bin/bash

default: print
	cd src && zip --password `cat zip-password.txt` -r - flag.txt > locked.zip
	cd src && zip -r - locked.zip pmdk-2024-altered.jpg > ../dist/misc-the-original-image.zip
	@echo Challenge compiled.

print:
	@echo Current Flag: $$(cat src/flag.txt)

change: print changeflag clean default print

changeflag:
	$(shell bash -c 'read -p "New Flag: " flag; echo $$flag > src/flag.txt')
	@echo Flag changed.

clean:
	rm -f src/locked.zip
	rm -f dist/misc-the-original-image.zip
	@echo Challenge cleaned.
