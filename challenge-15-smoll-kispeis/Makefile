default:
	cd src/ && pip install -r requirements.txt
	cd src/ && python3 source.py
	cd src/ && zip -r ../dist/crypto-smoll-kispeis.zip source.py output.txt
	@echo Challenge compiled.

clean:
	rm -f src/output.txt
	rm -f dist/crypto-smoll-kispeis.zip
	rm -r src/__pycache__
	@echo Challenge cleaned.
