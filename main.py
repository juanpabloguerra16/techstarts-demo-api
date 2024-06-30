import os
from time import sleep
import aiofiles
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
import uvicorn

app = FastAPI()

# Get the markdown directory from environment variable, with a fallback
MARKDOWN_DIR = os.getenv("MARKDOWN_DIR", "./mock documents")
HTML_DIR = os.getenv("HTML_DIR", "./html")


@app.get("/markdown/{filename}")
async def stream_markdown(filename: str):
    file_path = os.path.join(MARKDOWN_DIR, filename)
    print(file_path)

    if not file_path.endswith(".md"):
        raise HTTPException(status_code=400, detail="File must have .md extension")

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    async def file_iterator():
        async with aiofiles.open(file_path, mode="r", encoding="utf-8") as file:
            while True:
                char = await file.read(1)
                sleep(0.01)
                if not char:
                    break
                yield char.encode("utf-8")

    return StreamingResponse(file_iterator(), media_type="text/markdown")


@app.get("/html/{filename}")
async def stream_html(filename: str):
    file_path = os.path.join(HTML_DIR, filename)
    print(file_path)

    # if not file_path.endswith(".html"):
    #     raise HTTPException(status_code=400, detail="File must have .md extension")

    # if not os.path.exists(file_path):
    #     raise HTTPException(status_code=404, detail="File not found")

    def file_iterator():
        return open(file_path, mode="r").read()

        # async with aiofiles.open(file_path, mode="r", encoding="utf-8") as file:
        #     while True:
        #         char = await file.read(1)
        #         sleep(0.00)
        #         if not char:
        #             break
        #         yield char.encode("utf-8")

    return StreamingResponse(open(file_path, mode="r").read(), media_type="text/html")

@app.get("/image/{filename}")
async def stream_image(filename: str):
    file_path = os.path.join(HTML_DIR, filename)
    print(file_path)

    # if not file_path.endswith(".html"):
    #     raise HTTPException(status_code=400, detail="File must have .md extension")

    # if not os.path.exists(file_path):
    #     raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path) # (open(file_path, mode="rb").read(), media_type="image/png")


@app.get("/")
async def root():
    return {"message": "Welcome to the Markdown Streamer API"}


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
