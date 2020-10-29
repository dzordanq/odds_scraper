FROM python:3.8
COPY requirements.txt /
RUN pip install --requirement requirements.txt
COPY DEFINITIONS.py /
COPY functions.py /
COPY main.py /
COPY MarketsFilter.py /
COPY Parser.py /
COPY Unibet.py /
CMD [ "python3", "main.py" ]