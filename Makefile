# make run | test | evals | docker | docker-run | config      (PORT=7870 make run to change the port)
PORT ?= 7860
IMAGE ?= zlayt-demo

.PHONY: run test evals docker docker-run config

run:            ## demo mode, no key: http://127.0.0.1:$(PORT)
	PORT=$(PORT) ./run.sh

test:           ## unit tests (several minutes)
	./run.sh test

evals:          ## golden-set eval on the fixture backend; report in data/evals/ (git-ignored). a failure here is EXPECTED, see README
	./run.sh setup
	@.venv/bin/python -m evals.run --out data/evals; rc=$$?; \
	if [ $$rc -ne 0 ]; then echo; echo "make evals: the failure (runner exit $$rc) is EXPECTED on the fixture backend. The ship bar needs live-model runs (determinism, judge controls), so a fixture run reports ship_bar_met=False by design. The report is in data/evals/. See README, 'Tests and evals'."; fi; \
	exit $$rc

config:         ## print the resolved mode (never prints a key)
	./run.sh setup
	.venv/bin/python -m app.config

docker:         ## build the demo image
	docker build -t $(IMAGE) .

docker-run:     ## run the demo image on host port $(PORT)
	docker run --rm -p $(PORT):7860 $(IMAGE)
