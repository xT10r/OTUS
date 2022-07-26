FROM ket9/otus-devsecops-owasp-rest:latest

RUN apk update \
    && addgroup -S otus_group \
    && adduser -S otus_user -G otus_group \
    && rm -rf /var/cache/apk/*

USER otus_user

EXPOSE 8080