build:
	@echo "===================================================================="
	@echo "Build docker image"
	@echo "===================================================================="
	@docker build --tag datasets-earth .

run: build
	@echo "===================================================================="
	@echo "Run docker image"
	@echo "===================================================================="
	@docker run datasets-earth

bash: build
	@echo "===================================================================="
	@echo "Start bash in docker container"
	@echo "===================================================================="
	@docker run -it datasets-earth bash

up:
	@echo "===================================================================="
	@echo "Start docker-compose file"
	@echo "===================================================================="
	@docker-compose up --build

.PHONY: build run bash up
