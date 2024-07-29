default: print
	tar cvf dist/docker-challenge.tar -C src app Dockerfile
	cd src && zip -r - . --exclude='*flag*' > ../dist/web-search-4.zip
	@echo Challenge compiled.

print:
	@echo Current Flag: $$(cat src/app/flag.txt)

change: print changeflag clean default print

changeflag:
	$(shell bash -c 'read -p "New Flag: " flag; echo $$flag > src/app/flag.txt')
	@echo Flag changed.

clean:
	rm -f dist/docker-challenge.tar
	rm -f dist/web-search-4.zip
	@echo Challenge cleaned.
