FROM public.ecr.aws/lambda/python:3.11

ARG SPIDER_BANK_INDONESIA_URL

ENV SPIDER_BANK_INDONESIA_URL=$SPIDER_BANK_INDONESIA_URL

RUN yum install -y gcc libxml2-devel libxslt-devel

COPY . ${LAMBDA_TASK_ROOT}

RUN pip install -r requirements.txt

CMD [ "main.handler" ]