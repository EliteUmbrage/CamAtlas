#!/usr/bin/env python3

import json
import webbrowser
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import pickle
from urllib.parse import urljoin
from rich.console import Console
from rich.table import Table
from rich.live import Live
from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import HSplit
from prompt_toolkit.widgets import Box, Frame, Label
from threading import Thread
import time

console = Console()
REFRESH_INTERVAL = 60  # seconds

# Load sources
with open("sources.json", "r") as f:
    sources = json.load(f)

# Metadata cache
CACHE_FILE = Path("metadata_cache.pkl")
if CACHE_FILE.exists():
    with open(CACHE_FILE, "rb") as f:
        metadata_cache = pickle.load(f)
else:
    metadata_cache = {}

# Favorites
FAV_FILE = Path("favorites.json")
if FAV_FILE.exists():
    with open(FAV_FILE, "r") as f:
        favorites = json.load(f)
else:
    favorites = []

# Save helpers
def save_cache():
    with open(CACHE_FILE, "wb") as f:
        pickle.dump(metadata_cache, f)

def save_favorites():
    with open(FAV_FILE, "w") as f:
        json.dump(favorites, f, indent=2)

# Fetch metadata
def fetch_metadata(cam):
    if cam["url"] in metadata_cache:
        return metadata_cache[cam["url"]]
    try:
        r = requests.get(cam["url"], timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")
        title = soup.title.string.strip() if soup.title else "No title"
        desc_tag = soup.find("meta", attrs={"name": "description"})
        description = desc_tag["content"].strip() if desc_tag else "No description"

        snapshot_url = None
        for img in soup.find_all("img"):
            src = img.get("src", "")
            alt = img.get("alt", "")
            if any(k in src.lower() or k in alt.lower() for k in ["snapshot","camera","live","feed"]):
                snapshot_url = src
                if snapshot_url.startswith("/"):
                    snapshot_url = urljoin(cam["url"], snapshot_url)
                break

        meta = {"title": title, "description": description, "snapshot": snapshot_url}
    except Exception as e:
        meta = {"title": "Failed", "description": str(e), "snapshot": None}

    metadata_cache[cam["url"]] = meta
    save_cache()
    return meta

# Refresh snapshots in background
def refresh_snapshots():
    while True:
        for cam in sources:
            fetch_metadata(cam)
        time.sleep(REFRESH_INTERVAL)

# Build the TUI table
def build_table(selected_idx=0):
    table = Table(title="CamAtlas Dashboard", expand=True)
    table.add_column("Index", style="cyan", no_wrap=True)
    table.add_column("Name", style="magenta")
    table.add_column("Type", style="green")
    table.add_column("Country", style="yellow")
    table.add_column("Snapshot", style="blue")
    table.add_column("Favorite", style="red")

    for idx, cam in enumerate(sources):
        meta = fetch_metadata(cam)
        snapshot_flag = "✅" if meta["snapshot"] else ""
        favorite_flag = "★" if cam["name"] in favorites else ""
        style = "reverse" if idx == selected_idx else ""
        table.add_row(str(idx), cam["name"], cam["type"], cam["country"], snapshot_flag, favorite_flag, style=style)
    return table

# TUI Application
class CamAtlasTUI:
    def __init__(self):
        self.selected_idx = 0
        self.running = True
        self.bindings = KeyBindings()

        @self.bindings.add("up")
        def move_up(event):
            self.selected_idx = max(0, self.selected_idx - 1)

        @self.bindings.add("down")
        def move_down(event):
            self.selected_idx = min(len(sources)-1, self.selected_idx + 1)

        @self.bindings.add("enter")
        def open_camera(event):
            cam = sources[self.selected_idx]
            meta = fetch_metadata(cam)
            url_to_open = meta["snapshot"] if meta["snapshot"] else cam["url"]
            webbrowser.get("firefox").open(url_to_open)

        @self.bindings.add("f")
        def toggle_favorite(event):
            cam = sources[self.selected_idx]
            if cam["name"] in favorites:
                favorites.remove(cam["name"])
            else:
                favorites.append(cam["name"])
            save_favorites()

        @self.bindings.add("q")
        def quit_app(event):
            self.running = False
            event.app.exit()

        self.layout = Layout(HSplit([Label(text="CamAtlas TUI - ↑/↓ select, Enter open, f toggle favorite, q quit")]))

        self.app = Application(layout=self.layout, key_bindings=self.bindings, full_screen=True, refresh_interval=1)

    def run(self):
        def updater():
            with Live(build_table(self.selected_idx), refresh_per_second=1) as live:
                while self.running:
                    live.update(build_table(self.selected_idx))
                    time.sleep(0.5)
        Thread(target=updater, daemon=True).start()
        self.app.run()

if __name__ == "__main__":
    Thread(target=refresh_snapshots, daemon=True).start()
    CamAtlasTUI().run()
