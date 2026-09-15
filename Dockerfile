FROM python:3.13-slim

WORKDIR /marketplace_app

COPY . /marketplace_app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN chmod a+x /marketplace_app/newdjango/entrypoint.sh

EXPOSE 8000

CMD ["sh", "newdjango/entrypoint.sh"]