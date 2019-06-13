LANG=en_GB.UTF-8
LC_ALL=en_GB.UTF-8


install:
	pip3 install --user --upgrade pip ;
	pip3 install --user --upgrade --force-reinstall . ;

install-dev:
	pip3 install --user --upgrade pip ;
	pip3 install --user --upgrade --force-reinstall .[dev] ;

cloc:
	cloc --exclude-list-file=.gitignore . ;

format:
	python3 -m isort -rc ./tests ./jason ./examples ;
	python3 -m black ./tests ./jason ./examples ;

lint:
	python3 -m isort -rc --check-only ./tests ./jason ./examples ;
	python3 -m black --check ./tests ./jason ./examples ;

unit-test:
	python3 -m coverage run --source=./jason -m pytest --doctest-modules ;
	python3 -m coverage report ;

feature-test:
	python3 -m behave ./tests/features ;

pre-commit:
	python3 --version ;
	make format ;
	make lint ;
	make unit-test ;
	make feature-test ;
