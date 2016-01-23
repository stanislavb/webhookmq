.PHONY: test-syntax test-integration build rmi compose docker-test-integration

# Test code syntax and standards
test-syntax:
	flake8 --verbose --max-line-length=120 --exclude=".git,env" --show-source .

# Run Django tests. Sleep timer is to let RabbitMQ start being reachable.
test-integration:
	sleep 3 && python -m webhookmq.queue test webhookmq.test

# Build docker image
build:
	docker build --force-rm -t stanislavb/webhookmq .

# Remove docker image
rmi:
	docker rmi stanislavb/webhookmq

# Build and run WebhookMQ with RabbitMQ backend
compose:
	docker-compose build
	docker-compose up -d

# Run integration test in a docker container linked to rabbitmq backend
docker-test-integration:
	docker-compose build
	docker-compose run webhookmq make test-integration
