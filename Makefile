.SILENT: fmt check lint bandit

fmt:
	find . -type d -name ".venv" -prune -o -print -type f -name "*.py" \
		-exec pyupgrade \
			--exit-zero-even-if-changed \
			--keep-runtime-typing \
			--py310-plus \
			{} \+ 1> /dev/null
	autoflake \
		--in-place \
		--remove-all-unused-imports \
		--ignore-init-module-imports \
		-r \
		<project-name> tests
	isort --profile black .
	black .

bandit:
	bandit -q -r <project-name>
	bandit -q -lll -r tests

check: bandit
	find . -type d -name ".venv" -prune -o -print -type f -name "*.py" \
		-exec pyupgrade \
			--keep-runtime-typing \
			--py310-plus \
			{} \+ 1> /dev/null
	autoflake \
		--in-place \
		--remove-all-unused-imports \
		--ignore-init-module-imports \
		-r \
		-c \
		<project-name> tests
	isort --profile black -c .
	black --check .

lint: bandit
	mypy <project-name>
	flake8 .

test:
	pytest -x --cov=core --cov=<project-name> --cov-fail-under=90
