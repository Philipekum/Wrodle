FROM redis:8-alpine

COPY redis.conf /usr/local/etc/redis/redis.conf

ENV REDISCLI_AUTH=""

HEALTHCHECK --start-period=5s --start-interval=1s --interval=30s --timeout=3s --retries=3 \
  CMD redis-cli --no-auth-warning ping || exit 1

CMD ["sh", "-c", "exec redis-server /usr/local/etc/redis/redis.conf --requirepass \"$REDIS_PASSWORD\""]
