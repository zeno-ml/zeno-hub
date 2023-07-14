.PHONY: lint
lint:
	@echo "==> 👕 Linting"
	@poetry check
	@poetry run black --check .
	@poetry run ruff check .

.PHONY: typecheck
typecheck:
	@echo "==> ✅ Type checks"
	@poetry run pyright . 
