.PHONY: build clean upload increment_version

build:
	python3 -m build

clean:
	rm -rf dist/*

increment_version:
	python3 scripts/increment_version.py

upload:
	python3 -m twine upload dist/*

deploy: clean increment_version build upload
