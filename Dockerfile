FROM python:3.12-bookworm
COPY . /app
WORKDIR /app
RUN pip install uv && \
	python -m uv sync && \
	python -m uv run setup.py build_ext --inplace

ENTRYPOINT ["python", "-m", "uv", "run", "main.py"]

EXPOSE 8080
