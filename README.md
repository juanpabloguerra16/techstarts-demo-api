# Markdown Streamer!

Uses FastAPI in Python to deliver a streaming response of text from a text file (with Markdown extension).

## Usage

Initialize Docker container:

`docker build -t markdown-streamer`

`docker run -it -p 8000:8000 markdown-streamer`

Send requests on port 8000:

`GET http://localhost:8000/markdown/ai-skunkworks.md`
