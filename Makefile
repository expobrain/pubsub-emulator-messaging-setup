.SILENT: fmt check lint bandit

fmt:
	find . -type d -name ".venv" -prune -o -print -type f -name "*.py" \
		-exec pyupgrade \
			--exit-zero-even-if-changed \
			--keep-runtime-typing \
			--py38-plus \
			{} \+ 1> /dev/null
	autoflake \
		--in-place \
		--remove-all-unused-imports \
		--ignore-init-module-imports \
		-r \
		pubsub_emulator_messaging_setup tests
	isort --profile black .
	black .

bandit:
	bandit -q -r pubsub_emulator_messaging_setup
	bandit -q -lll -r tests

check: bandit
	find . -type d -name ".venv" -prune -o -print -type f -name "*.py" \
		-exec pyupgrade \
			--keep-runtime-typing \
			--py38-plus \
			{} \+ 1> /dev/null
	autoflake \
		--in-place \
		--remove-all-unused-imports \
		--ignore-init-module-imports \
		-r \
		-c \
		pubsub_emulator_messaging_setup tests
	isort --profile black -c .
	black --check .

lint: bandit
	mypy pubsub_emulator_messaging_setup
	flake8 .

test:
	pytest -x --cov=core --cov=pubsub_emulator_messaging_setup --cov-fail-under=89

compose:
	docker-compose up --build

compose_up:
	docker-compose up -d --build

compose_down:
	docker-compose down

install:
	poetry install --sync
