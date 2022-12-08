kill -9 $(sudo lsof -t -i:5000)
timeout 10s echo "foo bar"
gunicorn --certfile nginx-selfsigned.pem --keyfile nginx-selfsignedkey.pem -b 192.168.2.251:5000 --threads=4 --worker-connections=1000 --preload wsgi:app