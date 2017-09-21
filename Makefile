all: venv
	git pull
	./venv/bin/python scripts/process.py
	./venv/bin/goodtables datapackage.json
	@git diff data

venv: scripts/requirements.txt
	[ -d ./venv ] || python3 -m venv venv
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install -Ur scripts/requirements.txt
	touch venv

clean:
	rm -r data/*.csv venv

.PHONY: clean
