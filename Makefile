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
	python3 -m isort -rc ./tests ./jason ;
	python3 -m black ./tests ./jason ;

lint:
	python3 -m isort -rc --check-only ./tests ./jason ;
	python3 -m black --check ./tests ./jason ;

test:
	python3 -m coverage run --source=./jason -m pytest --doctest-modules ;
	python3 -m coverage report ;
	python3 -m behave ./tests/features

pre-commit:
	python3 --version ;
	make format ;
	make lint ;
	make test ;
