FROM nginx:1.29-alpine

RUN apk add --no-cache openssl && \
    mkdir -p /etc/nginx/certs && \
    openssl req -x509 -nodes -days 3650 \
      -newkey rsa:2048 \
      -keyout /etc/nginx/certs/selfsigned.key \
      -out /etc/nginx/certs/selfsigned.crt \
      -subj "/C=RU/ST=YourState/L=YourCity/O=YourOrg/CN=localhost" && \
    apk del openssl && \
    rm -rf /var/cache/apk/*

CMD ["nginx", "-g", "daemon off;"]
