IMAGE := supermarket-sales-api
CONTAINER := supermarket-sales-api

.PHONY: build run stop logs test clean

build:
	docker build -t $(IMAGE) .

run:
	docker run -d --name $(CONTAINER) -p 8000:8000 $(IMAGE)
	@echo "API running at http://localhost:8000/docs"

stop:
	-docker stop $(CONTAINER)
	-docker rm $(CONTAINER)

logs:
	docker logs -f $(CONTAINER)

test:
	pip install -r requirements-dev.txt
	python -m pytest -q

clean: stop
	-docker rmi $(IMAGE)
