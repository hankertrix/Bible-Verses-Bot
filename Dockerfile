FROM python:3.12-bookworm
COPY . /app
WORKDIR /app
RUN pip install pdm && \
	python -m pdm export -o requirements.txt --without-hashes && \
	pip install -r requirements.txt && \
	python setup.py build_ext --inplace

ENTRYPOINT ["python"]
CMD ["main.py"]

EXPOSE 8080
