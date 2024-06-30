import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import uvicorn

app = FastAPI()

# Get the markdown directory from environment variable, with a fallback
MARKDOWN_DIR = os.getenv("MARKDOWN_DIR", "./mock documents")

@app.get("/markdown/{filename}")
async def stream_markdown(filename: str):
    file_path = os.path.join(MARKDOWN_DIR, filename)
    print(file_path)
    
    if not file_path.endswith('.md'):
        raise HTTPException(status_code=400, detail="File must have .md extension")
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    def file_iterator():
        with open(file_path, mode="rb") as file:
            yield from file
    
    return StreamingResponse(file_iterator(), media_type="text/markdown")

@app.get("/")
async def root():
    return {"message": "Welcome to the Markdown Streamer API"}

def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()