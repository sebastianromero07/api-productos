FROM python:3-slim
WORKDIR /programas/api-productos
RUN pip3 install fastapi
RUN pip3 install pydantic
RUN pip3 install psycopg2
COPY . .
CMD ["fastapi", "run", "./main.py", "--port", "8000"]
