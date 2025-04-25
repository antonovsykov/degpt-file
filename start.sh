PORT="${PORT:-8080}"
HOST="${HOST:-0.0.0.0}"
echo "PORT: $PORT"
echo "HOST: $HOST"

echo "Starting uvicorn..."
echo uvicorn main:app --host "$HOST" --port "$PORT" --forwarded-allow-ips '*'

# WEBUI_SECRET_KEY="$WEBUI_SECRET_KEY" exec uvicorn main:app  --host "$HOST" --port "$PORT" --forwarded-allow-ips '*'
exec uvicorn main:app \
    --workers 20 \
    --host "$HOST" \
    --port "$PORT" \
    --forwarded-allow-ips '*' \
    --timeout-keep-alive 65