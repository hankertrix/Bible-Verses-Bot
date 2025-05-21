FROM python:3.12-bookworm
COPY . /app
WORKDIR /app
RUN pip install pdm && \
	python -m pdm install && \
	python setup.py build_ext --inplace

ENTRYPOINT ["python"]
CMD ["main.py"]

EXPOSE 8080
