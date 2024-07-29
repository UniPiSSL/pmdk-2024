default: print
	cd src && python3 -m pip install -r requirements.txt
	cd src && python3 ./TAlgebra.py
	cd src && zip -r - output.txt TAlgebra.py requirements.txt > ../dist/crypto-twisted-algebra.zip
	-rm -f src/output.txt
	@echo Challenge compiled.

print:
	@echo Current Flag: $$(cat src/flag.txt)

change: print changeflag clean default print

changeflag:
	$(shell bash -c 'read -p "New Flag: " flag; echo $$flag > src/flag.txt')
	@echo Flag changed.

clean:
	-rm -f dist/crypto-twisted-algebra.zip
	-rm -f src/output.txt
	@echo Challenge cleaned.
