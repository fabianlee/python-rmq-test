OWNER := fabianlee
PROJECT := python-rmq-test
VERSION := 1.0.0
OPV := $(OWNER)/$(PROJECT):$(VERSION)

# runs rabbitmq server
run-rabbitmq-background:
	$(eval ISRUNNING=$(shell sudo docker ps -a -f name=my-rabbit --format='{{.Names}}' | wc -l ))
	@echo ISRUNNING = $(ISRUNNING)
ifeq (1, 1)
	@echo RabbitMQ server is already running, no need to startup container
else
	sudo docker stop my-rabbit
	sudo docker run --rm -it -d --hostname my-rabbit --name my-rabbit -p 15672:15672 -p 5672:5672 rabbitmq:3-management
	@echo
	@echo RabbitMQ server starting...
	sleep 10
	sudo docker logs my-rabbit | grep startup
endif
	@echo
	$(eval RMQ=$(shell sudo docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' my-rabbit))
	@echo RabbitMQ server listening at $(RMQ):5672 and also host server:5672
	@echo RabbitMQ web admin gui listening at $(RMQ):15672 and also host server:15672

# builds docker image
docker-build:
	sudo docker build -f Dockerfile -t $(OPV) .

## cleans docker image
clean:
	sudo docker image rm $(OPV) | true

## runs container in foreground, using default args
docker-test:
	sudo docker run -it --rm $(OPV)

## runs container in foreground, override entrypoint to use use shell
docker-test-cli:
	sudo docker run -it --rm --entrypoint "/bin/bash" $(OPV)

## runs bssl with parameters passed from command line "
## example:
## make docker-run CMD="./producer.py --host=192.168.1.100"
## make docker-run CMD="./consumer.py --host=192.168.1.100"
## make docker-run CMD="./get_ip.py"
docker-run: 
	sudo docker run -it --rm $(OPV) $(CMD)

## pushes to docker hub
docker-push:
	sudo docker push $(OPV)
