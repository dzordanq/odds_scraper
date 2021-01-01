FROM python:3.7
COPY . .
RUN pip install --requirement requirements.txt
CMD [ "python3", "main.py" ]