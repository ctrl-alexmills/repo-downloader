# Repo Downloader

A small Windows app for downloading GitHub repos without using the command line.
Paste a repo URL, pick a folder and click **Download**.

- **First time:** the repo is downloaded into `<your folder>\<repo name>`.
- **After that:** the same URL and folder fetch the latest changes instead of downloading everything again.
- It remembers the last folder you used.

Works with any Git URL (GitHub, GitLab, Bitbucket and others), including private repos you have access to.

## Install

1. **Install [Git](https://git-scm.com/downloads)** if you don't already have it. Repo Downloader uses it behind the scenes, and the default options in Git's installer are fine.
2. Go to the **[latest release](https://github.com/ctrl-alexmills/repo-downloader/releases/latest)** and download **`RepoDownloader-Setup-<version>.exe`**.
3. Run it. It installs just for your Windows account, so it doesn't need admin rights, and it adds Repo Downloader to your Start Menu.

Prefer not to install anything? Download `RepoDownloader-<version>-portable.exe` instead and run it from anywhere.

### "Windows protected your PC"

The app isn't code-signed, which costs money, so Windows SmartScreen shows a warning the first time you run it.
Click **More info → Run anyway**. Every release is built from the source code in this repo by
[GitHub Actions](https://github.com/ctrl-alexmills/repo-downloader/actions), so you can check exactly what went into it.

## Private repos

The first time you download a private repo, Git opens a GitHub sign-in window. Sign in once, and Git remembers you after that.

## Uninstall

Go to **Settings → Apps → Installed apps → Repo Downloader → Uninstall**.
Your downloaded repos are left alone. The app's one settings file is `%USERPROFILE%\.repo_downloader.json`, and you can delete it if you like.

## Running from source

You need Python 3.10 or newer, with tkinter (included in the python.org installer), and Git.

```
python repo_downloader.py
```

To build the `.exe` yourself, double-click `build_exe.bat`. The result goes in `dist\`.

## Making a release (maintainers)

1. Bump `__version__` in `repo_downloader.py` and commit.
2. Tag and push:
   ```
   git tag v1.0.1
   git push origin v1.0.1
   ```
3. GitHub Actions builds the installer and portable exe, then publishes them as a release.
   The build fails if the tag doesn't match `__version__`.

## License

[MIT](LICENSE)
