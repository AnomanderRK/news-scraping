# Basic example: https://www.youtube.com/watch?v=bi0cKgmRuiA
FROM python:3.7

COPY ["requirements.txt", "/usr/src"]

WORKDIR /usr/src

RUN pip install -r requirements.txt

COPY [".", "/usr/src"]

RUN pip install -e .

ENTRYPOINT ["python", "run_pipeline.py", "--config_file"]

CMD ["config.yaml"]