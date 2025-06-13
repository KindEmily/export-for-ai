import asyncio
import json
import logging
import os
import shutil
from typing import AsyncGenerator

import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel

import app_main

# --- FastAPI App Setup ---
app = FastAPI()
UI_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "ui_config.json")


# --- Pydantic Models ---
class Config(BaseModel):
    export_destination: str
    repositories: list[str]


# --- Helper Functions ---
def get_config_data() -> dict:
    if not os.path.exists(UI_CONFIG_PATH):
        return {"export_destination": "", "repositories": []}
    try:
        with open(UI_CONFIG_PATH, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {"export_destination": "", "repositories": []}


# --- API Endpoints ---
@app.get("/")
async def get_index() -> FileResponse:
    template_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    return FileResponse(template_path)


@app.get("/api/config")
async def get_config() -> dict:
    return get_config_data()


@app.post("/api/config")
async def save_config(config: Config) -> dict:
    try:
        with open(UI_CONFIG_PATH, "w") as f:
            json.dump(config.dict(), f, indent=2)
        return {"status": "success"}
    except IOError as e:
        return {"status": "error", "message": str(e)}


async def run_export_logic(config: Config) -> AsyncGenerator[str, None]:
    app_main.setup_logging()
    yield "data: Starting export process...\n\n"

    export_destination = config.export_destination
    repositories = config.repositories

    if not export_destination or not await asyncio.to_thread(
        os.path.isdir, export_destination
    ):
        yield f"data: [ERROR] Export destination '{export_destination}' is not a valid directory.\n\n"
        return

    if not repositories:
        yield "data: [WARN] No repositories listed in config file.\n\n"
        return

    yield f"data: Loaded {len(repositories)} repositories from config.\n\n"
    yield f"data: Aggregated export destination: {export_destination}\n\n"

    for repo_path in repositories:
        try:
            yield f"data: --- Processing repository: {repo_path} ---\n\n"

            md_file_path = await asyncio.to_thread(
                app_main.process_single_repository, repo_path
            )

            if md_file_path:
                yield f"data: Successfully generated export file: {os.path.basename(md_file_path)}\n\n"

                export_dir = os.path.dirname(md_file_path)
                await asyncio.to_thread(
                    shutil.copy, md_file_path, export_destination
                )
                yield f"data: Copied '{os.path.basename(md_file_path)}' to {export_destination}\n\n"

                await asyncio.to_thread(shutil.rmtree, export_dir)
                yield "data: Cleaned up temporary directory.\n\n"
            else:
                yield f"data: [ERROR] Failed to process repository: {repo_path}\n\n"
        except Exception as e:
            yield f"data: [ERROR] An unexpected error occurred while processing {repo_path}: {e}\n\n"
            logging.error(f"Error processing {repo_path}", exc_info=True)

    yield "data: All repositories processed.\n\n"


@app.post("/api/run-export")
async def run_export(config: Config) -> StreamingResponse:
    return StreamingResponse(run_export_logic(config), media_type="text/event-stream")


# --- Uvicorn runner ---
if __name__ == "__main__":
    print("Starting Export-for-AI web UI...")
    print("Open http://127.0.0.1:8000 in your browser.")
    uvicorn.run(app, host="127.0.0.1", port=8000)