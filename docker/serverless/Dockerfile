FROM public.ecr.aws/lambda/python:3.11

COPY . ${LAMBDA_TASK_ROOT}
RUN pip install -r requirements.txt
RUN pip install -e .

COPY docker/serverless/lambda_function.py ${LAMBDA_TASK_ROOT}

CMD [ "lambda_function.handler" ]
