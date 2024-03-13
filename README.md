# Spin up the container:
$docker-compose up -d --build

# Reducing URL [post]
http://127.0.0.1:5001/shorten

example: curl -X POST http://127.0.0.1:5001/shorten -H "Content-Type: application/json" -d '{"url": "http://ya.ru"}' 

# Retrieving original URL by shorten [get]
http://127.0.0.1:5001/<shorten_url>

example: curl http://127.0.0.1:5001/1b556b

# Retrieving top N most requsted URLs [get]
http://127.0.0.1:5001/top_urls

example: curl http://127.0.0.1:5001/top_urls
