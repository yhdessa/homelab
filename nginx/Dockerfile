FROM nginx:1.29-alpine

RUN apk update --no-cache && \
    apk upgrade --no-cache libpng && \
    rm -rf /var/cache/apk/*

CMD ["nginx", "-g", "daemon off;"]
