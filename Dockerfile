FROM python:3.10-slim

WORKDIR /src

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN export FLASK_APP=run.py

COPY . .

EXPOSE 5000

# ENTRYPOINT ["/bin/bash", "-c"]

CMD ["python3", "run.py"]
