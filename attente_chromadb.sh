#!/bin/sh

set -e

host="$CHROMADB_HOST"
port="$CHROMADB_PORT"

echo "Attente de ChromaDB sur $host:$port"

until curl -s "http://$host:$port/api/v1/tenants/default_tenant"; do
  >&2 echo "ChromaDB n'est pas prêt - attente"
  sleep 2
done

>&2 echo "ChromaDB est prêt - lancement de l'initialisation"
exec "$@"
