export HOST=0.0.0.0
export ENV_PORT=8000
echo "Starting server on port $ENV_PORT... Host: $HOST"
docker run -e HOST=$HOST -e ENV_PORT=$ENV_PORT -ti -p 8000:8000 url-shortner