FROM python:3.11

WORKDIR /chatbot_api

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install transformers==4.49.0

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]