default: print
	-rm -f src/flag.pdf
	cd src && python3 -m pip install -r requirements.txt
	cd src && python3 -m pip install -r dev-requirements.txt
	cd src && python3 ./generate-pdf.py
	cd src && python3 ./Lobotomy_Kaisen.py
	cd src && zip -r - output.txt flag.pdf.enc Lobotomy_Kaisen.py requirements.txt > ../dist/crypto-lobotomy-kaisen.zip
	-rm -f src/flag.pdf
	-rm -f src/output.txt
	-rm -f src/flag.pdf.enc
	@echo Challenge compiled.

print:
	@echo Current Flag: $$(cat src/flag.txt)

change: print changeflag clean default print

changeflag:
	$(shell bash -c 'read -p "New Flag: " flag; echo $$flag > src/flag.txt')
	@echo Flag changed.

clean:
	-rm -f dist/crypto-lobotomy-kaisen.zip
	-rm -f src/flag.pdf
	-rm -f src/output.txt
	-rm -f src/flag.pdf.enc
	@echo Challenge cleaned.
