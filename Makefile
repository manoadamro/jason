
LANG=en_GB.UTF-8
LC_ALL=en_GB.UTF-8


format:
	isort -rc ./tests ./jason ;
	black ./tests ./jason ;

test:
	isort -rc --check-only ./tests ./jason ;
	black --check ./tests ./jason;
	coverage run -m pytest ;
	coverage report --show-missing --skip-covered ;

pre-commit:
	python --version
	make format
	make test
