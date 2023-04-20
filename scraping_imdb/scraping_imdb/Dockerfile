FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

EXPOSE 8000

CMD ["streamlit", "run", "streamlit_app.py", "--server.address", "0.0.0.0", "--server.port", "80"]