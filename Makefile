# Variables
NAME = "pocketcasts-stats"

all: build run

build:
	docker build -t $(NAME) .

run:
	docker run --env-file=.env $(NAME)

test: build
	docker run -ti --env-file=.env $(NAME) sh -c 'pytest'

coverage: build
	docker run -ti --env-file=.env $(NAME) sh -c 'pytest --cov=./'

report:
	pytest --cov-report=xml:cov.xml --cov=./

.PHONY: all build run test coverage report
