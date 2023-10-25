.PHONY: lint
lint:
	@echo "==> 👕 Linting"
	@poetry check
	@poetry run ruff format ./zeno_backend
	@poetry run ruff check .

.PHONY: typecheck
typecheck:
	@echo "==> ✅ Type checks"
	@poetry run pyright . 
