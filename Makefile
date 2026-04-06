.PHONY: help install test clean

help:
	@echo "ENTRO-CORE Makefile"
	@echo "  make install  - Install package"
	@echo "  make test     - Run tests"
	@echo "  make clean    - Clean build artifacts"

install:
	pip install -e .

test:
	pytest tests/ -v

clean:
	rm -rf build/ dist/ *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
