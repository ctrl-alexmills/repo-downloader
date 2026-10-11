"""
Repo Downloader
---------------
Paste a GitHub (or any Git) repo URL, choose a folder, click Download.

- First time: the repo is cloned into  <your folder>/<repo name>
- Next time (same URL + folder): it pulls the latest changes instead
- Remembers the last folder you used

Requirements: Python 3 and Git installed (nothing else to install).
Run with:  python repo_downloader.py
"""

import json
import os
import shutil
import subprocess
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, scrolledtext

SETTINGS_FILE = Path.home() / ".repo_downloader.json"

# Stop a black console window flashing up on Windows when git runs
NO_WINDOW = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0


# ---------------------------------------------------------------- settings
def load_settings():
    try:
        return json.loads(SETTINGS_FILE.read_text())
    except Exception:
        return {}


def save_settings(data):
    try:
        SETTINGS_FILE.write_text(json.dumps(data))
    except Exception:
        pass


# ---------------------------------------------------------------- git logic
def repo_name_from_url(url):
    """https://github.com/owner/my-repo.git  ->  my-repo"""
    name = url.strip().rstrip("/").split("/")[-1].split(":")[-1]
    if name.endswith(".git"):
        name = name[:-4]
    return name


def run_git(args, cwd=None, log=print):
    """Run a git command and stream its output to the log. Returns True on success."""
    process = subprocess.Popen(
        ["git", *args],
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        creationflags=NO_WINDOW,
    )
    for line in process.stdout:
        line = line.strip()
        if line:
            log(line)
    return process.wait() == 0


def download_repo(url, folder, log):
    """Clone the repo into folder/<name>, or pull if it's already there."""
    if not shutil.which("git"):
        log("ERROR: Git isn't installed (or isn't on PATH).")
        log("Install it from https://git-scm.com and try again.")
        return False

    name = repo_name_from_url(url)
    if not name:
        log("ERROR: That doesn't look like a repo URL.")
        return False

    target = Path(folder) / name

    if (target / ".git").exists():
        log(f"'{name}' already exists here - pulling latest changes...")
        ok = run_git(["pull"], cwd=target, log=log)
    elif target.exists() and any(target.iterdir()):
        log(f"ERROR: '{target}' already exists and isn't a Git repo.")
        log("Choose a different folder, or rename/move that one.")
        return False
    else:
        log(f"Downloading '{name}' into {folder} ...")
        ok = run_git(["clone", url.strip(), str(target)], log=log)

    if ok:
        log(f"Done. Files are in: {target}")
    else:
        log("Something went wrong - see the messages above.")
        log("(Private repo? Make sure you're signed in to GitHub with Git.)")
    return ok


# ---------------------------------------------------------------- interface
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Repo Downloader")
        self.geometry("620x380")
        self.minsize(480, 300)
        self.settings = load_settings()

        pad = {"padx": 10, "pady": 5}

        # Repo URL
        tk.Label(self, text="Repo URL:").grid(row=0, column=0, sticky="w", **pad)
        self.url_var = tk.StringVar()
        url_entry = tk.Entry(self, textvariable=self.url_var)
        url_entry.grid(row=0, column=1, columnspan=2, sticky="ew", **pad)
        url_entry.focus()

        # Destination folder
        tk.Label(self, text="Save to:").grid(row=1, column=0, sticky="w", **pad)
        self.folder_var = tk.StringVar(value=self.settings.get("last_folder", ""))
        tk.Entry(self, textvariable=self.folder_var).grid(
            row=1, column=1, sticky="ew", **pad
        )
        tk.Button(self, text="Browse...", command=self.choose_folder).grid(
            row=1, column=2, sticky="ew", **pad
        )

        # Buttons
        buttons = tk.Frame(self)
        buttons.grid(row=2, column=0, columnspan=3, sticky="ew", **pad)
        self.go_button = tk.Button(
            buttons, text="Download", width=14, command=self.start_download
        )
        self.go_button.pack(side="left")
        tk.Button(
            buttons, text="Open folder", width=14, command=self.open_folder
        ).pack(side="left", padx=8)

        # Log output
        self.log_box = scrolledtext.ScrolledText(self, height=10, state="disabled")
        self.log_box.grid(row=3, column=0, columnspan=3, sticky="nsew", **pad)

        self.columnconfigure(1, weight=1)
        self.rowconfigure(3, weight=1)
        self.bind("<Return>", lambda e: self.start_download())

    def choose_folder(self):
        folder = filedialog.askdirectory(
            initialdir=self.folder_var.get() or str(Path.home())
        )
        if folder:
            self.folder_var.set(folder)

    def open_folder(self):
        folder = self.folder_var.get()
        if not folder or not os.path.isdir(folder):
            messagebox.showinfo("Repo Downloader", "Choose a folder first.")
            return
        if sys.platform == "win32":
            os.startfile(folder)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", folder])
        else:
            subprocess.Popen(["xdg-open", folder])

    def log(self, message):
        # Safe to call from the worker thread
        def append():
            self.log_box.configure(state="normal")
            self.log_box.insert("end", message + "\n")
            self.log_box.see("end")
            self.log_box.configure(state="disabled")

        self.after(0, append)

    def start_download(self):
        url = self.url_var.get().strip()
        folder = self.folder_var.get().strip()

        if not url:
            messagebox.showwarning("Repo Downloader", "Paste a repo URL first.")
            return
        if not folder or not os.path.isdir(folder):
            messagebox.showwarning("Repo Downloader", "Choose a folder that exists.")
            return

        self.settings["last_folder"] = folder
        save_settings(self.settings)

        self.go_button.configure(state="disabled", text="Working...")
        threading.Thread(
            target=self.worker, args=(url, folder), daemon=True
        ).start()

    def worker(self, url, folder):
        try:
            download_repo(url, folder, self.log)
        except Exception as error:
            self.log(f"ERROR: {error}")
        finally:
            self.after(
                0, lambda: self.go_button.configure(state="normal", text="Download")
            )


if __name__ == "__main__":
    App().mainloop()
