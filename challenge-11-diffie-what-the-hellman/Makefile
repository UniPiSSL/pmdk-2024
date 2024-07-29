default:
	tar cvf dist/docker-challenge.tar -C src app Dockerfile
	cd src/app && zip -r - . --exclude='*flag*' > ../../dist/crypto-diffie-what-the-hellman.zip
	@echo Challenge compiled.

clean:
	rm -f dist/crypto-diffie-what-the-hellman.zip
	rm -f dist/docker-challenge.tar
	@echo Challenge cleaned.
