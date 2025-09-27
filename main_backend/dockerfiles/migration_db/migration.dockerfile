FROM alpine:3.18

RUN apk add --no-cache postgresql-client bash dos2unix

WORKDIR /migration/scripts

COPY database/ ../database/
COPY scripts/*.sh ./
COPY .env ../.env

RUN dos2unix ../.env ./*.sh && \
    chmod +x ./*.sh

CMD ["bash"]