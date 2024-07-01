#!/bin/sh

if [ -z "${PORT}" ]; then
    echo "PORT is not set"
    exit 1
fi

if [ -z "${SECURE}" ]; then
  SECURE=no
fi

SSL=""
if [ "${SECURE}" = "yes" ]; then
  SSL="--ssl-keyfile=dev-key.pem --ssl-certfile=dev-cert.pem"
  echo "Setting SSL parameters to $SSL"
fi

python -m uvicorn main:app --reload --host 0.0.0.0 --port ${PORT} ${SSL}
