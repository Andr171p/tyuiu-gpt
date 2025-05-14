FROM python:3.11

WORKDIR /tyuiu_gpt

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

RUN python -c "from transformers import AutoModel; AutoModel.from_pretrained('intfloat/multilingual-e5-large')"

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]