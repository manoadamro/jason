
LANG=en_GB.UTF-8
LC_ALL=en_GB.UTF-8


install:
	pip3 install --upgrade pip ;
	pip3 install --upgrade --force-reinstall . ;

cloc:
	cloc ./jason ;

format:
	isort -rc ./tests ./jason ;
	black ./tests ./jason ;

test:
	isort -rc --check-only ./tests ./jason ;
	black --check ./tests ./jason;
	coverage run -m pytest --doctest-modules;
	coverage report --show-missing --skip-covered ;

pre-commit:
	python3 --version ;
	make format ;
	make test ;
