
LANG=en_GB.UTF-8
LC_ALL=en_GB.UTF-8


install:
	pip3 install --upgrade pip ;
	pip3 install --upgrade --force-reinstall . ;

cloc:
	cloc --exclude-list-file=.gitignore . ;

format:
	isort -rc ./tests ./jason ;
	black ./tests ./jason ;

check:
	isort -rc --check-only ./tests ./jason ;
	black --check ./tests ./jason;

test:
	coverage run -m pytest --doctest-modules;
	coverage report ;

pre-commit:
	python3 --version ;
	make format ;
	make check ;
	make test ;
	make cloc ;
