default: print
	-rm -f src/ch4ll3ng_flag.png
	-rm -f *.sus
	-rm -rf files
	cd src && python3 -m pip install -r dev-requirements.txt
	cd src && python3 ./generate-flag.py
	cd src && gcc -g -o free_0days free_0days.c
	cd src && ./free_0days
	mkdir -p src/files
	mv src/*.sus src/files
	cd src && zip -r - free_0days ./files > ../dist/rev-ransomware-v2.zip
	-rm -f src/ch4ll3ng_flag.png
	-rm -f src/*.sus
	@echo Challenge compiled.

print:
	@echo Current Flag: $$(cat src/flag.txt)

change: print changeflag clean default print

changeflag:
	$(shell bash -c 'read -p "New Flag: " flag; echo $$flag > src/flag.txt')
	@echo Flag changed.

clean:
	-rm -f dist/rev-ransomware-v2.zip
	-rm -f src/ch4ll3ng_flag.png
	-rm -f src/*.sus
	-rm -rf src/files
	-rm -f src/free_0days
	@echo Challenge cleaned.
