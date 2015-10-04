build:
	docker build --force-rm -t stanislavb/$(shell basename $(CURDIR)) .
rmi:
	docker rmi stanislavb/$(shell basename $(CURDIR))
compose:
	docker-compose up -d
test-syntax:
	flake8 --verbose --max-line-length=120 --exclude=".git,env" --show-source .
