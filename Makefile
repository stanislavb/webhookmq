.PHONY: test-syntax test-integration build rmi compose rabbitmq-test docker-test-integration test clean
test-syntax:
	flake8 --verbose --max-line-length=120 --exclude=".git,env" --show-source .
test-integration:
	python -m webhookmq.queue test
build:
	docker build --force-rm -t stanislavb/$(shell basename $(CURDIR)) .
rmi:
	docker rmi stanislavb/$(shell basename $(CURDIR))
compose:
	docker-compose build
	docker-compose up -d
rabbitmq-test:
	docker run -d --hostname $(shell basename $(CURDIR))_rabbitmq \
		--name $(shell basename $(CURDIR))_rabbitmq_test rabbitmq
	sleep 3
docker-test-integration:
	docker run -it --name $(shell basename $(CURDIR))_integration_test \
		-e "SECRET_KEY=test" -e "PATH_PREFIX=test" -e "DEBUG=True" \
		--link $(shell basename $(CURDIR))_rabbitmq_test:rabbitmq \
		stanislavb/$(shell basename $(CURDIR)) \
		make test-integration
test: build rabbitmq-test docker-test-integration
clean:
	docker rm -f $(shell basename $(CURDIR))_rabbitmq_test
	docker rm -f $(shell basename $(CURDIR))_integration_test
