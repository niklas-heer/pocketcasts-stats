# Variables
NAME = "pocketcasts-stats"

all: build run

build:
	docker build -t $(NAME) .

run:
	docker run --env-file=.env $(NAME)

test: build
	docker run -ti --env-file=.env $(NAME) sh -c 'pytest'

.PHONY: all build run test
