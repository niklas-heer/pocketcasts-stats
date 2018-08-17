# Variables
NAME = "pocketcasts-stats"

all: build run

build:
	docker build -t $(NAME) .

run:
	docker run --env-file=env.txt $(NAME)


.PHONY: all build run
