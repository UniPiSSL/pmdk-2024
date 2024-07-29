default:
	cd src/ && pip install -r requirements.txt && python3 source.py && zip -r ../dist/crypto-rout.zip source.py output.txt
	@echo Challenge compiled.

clean:
	rm -f src/output.txt
	rm -f dist/crypto-rout.zip
	rm -r src/__pycache__
	@echo Challenge cleaned.
