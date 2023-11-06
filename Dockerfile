FROM python:3.11

WORKDIR /code

COPY requirements.txt /code

RUN pip3 install --upgrade pip

RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

COPY . /code

RUN chmod +x /code/run.sh

# ENTRYPOINT [""]

CMD ["/code/run.sh"]
