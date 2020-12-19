build:
	@echo "===================================================================="
	@echo "Build docker image"
	@echo "===================================================================="
	@docker-compose build

bash: build
	@echo "===================================================================="
	@echo "Start bash in docker container"
	@echo "===================================================================="
	@docker-compose run -v $(pwd):/home/python earth bash

up:
	@echo "===================================================================="
	@echo "Start docker-compose file"
	@echo "===================================================================="
	@docker-compose up --build

.PHONY: build bash up
