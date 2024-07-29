default: print
	#-cd src/app && rm pwnb0t && rm -r glibc
	#cd src/app && cp binary0 . #&& cp -r ../build/glibc .
	tar cvf dist/docker-challenge.tar -C src app Dockerfile
	cd src/app && zip -r - array-app --exclude='*flag*' > ../../dist/pwn-array-app.zip
	@echo Challenge compiled.
print:
	@echo Current Flag: $$(cat src/app/flag.txt)
change: print changeflag clean default print
changeflag:
	$(shell bash -c 'read -p "New Flag: " flag; echo $$flag > src/app/flag.txt')
	@echo Flag changed.
clean:
	-rm -f dist/docker-challenge.tar
	-rm -f dist/pwn-array-app.zip
	@echo Challenge cleaned.
