# ytm-album

Download YouTube Music albums (and full artist discographies) at the highest quality available with your Premium account — 256kbps AAC, properly tagged, with embedded high-resolution cover art.

## Features

- Looks up albums by `artist` + `album` name via YouTube Music's metadata API
- Downloads tracks in parallel (configurable concurrency)
- Writes proper iTunes-style MP4 tags (title, artist, album, track number, year)
- Embeds high-resolution album cover into each `.m4a`
- Saves a separate `cover.jpg` in the album folder for music players that prefer folder art
- Full-discography mode: pass just an artist name to download every album
- Optional `--singles` flag to include EPs and singles
- Skips already-downloaded tracks on resume by default
- Live progress bar with per-track status

## Requirements

- `python3` (3.10+)
- [`yt-dlp`](https://github.com/yt-dlp/yt-dlp) — handles the actual audio download
- A YouTube Music **Premium** account (for 256kbps AAC; free accounts are capped at 128kbps)
- A browser logged into music.youtube.com (cookies are pulled from it)

### Python dependencies

```bash
pip3 install --user ytmusicapi mutagen rich
```

## Install

Clone and symlink (so the command is available in your `$PATH`):

```bash
git clone https://github.com/fuddlesworth/ytm-album.git ~/Documents/ytm-album
mkdir -p ~/bin
ln -s ~/Documents/ytm-album/ytm-album ~/bin/ytm-album
```

Make sure `~/bin` is on your `PATH`. For fish:

```fish
set -gx PATH $HOME/bin $PATH
```

## Usage

### Single album

```bash
ytm-album "Radiohead" "OK Computer"
```

Output: `./Radiohead/OK Computer/01 - Airbag.m4a` ... + `cover.jpg`

### Full discography

```bash
ytm-album "Aphex Twin"                # all albums (default)
ytm-album "Aphex Twin" --singles      # albums + singles/EPs
ytm-album "Aphex Twin" --no-albums --singles  # singles only
```

### Common flags

| Flag | Default | Description |
|------|---------|-------------|
| `--browser` | `firefox` | Browser to pull cookies from (`firefox`, `chrome`, `brave`, `safari`, `edge`) |
| `--output-dir` | `.` | Base directory; artist subfolder is created inside |
| `-j N`, `--jobs N` | `4` | Parallel track downloads |
| `-y`, `--yes` | off | Skip confirmation prompt |
| `--no-skip` | off | Re-download tracks even if file already exists |
| `--albums` / `--no-albums` | albums on | Toggle albums in discography mode |
| `--singles` / `--no-singles` | singles off | Toggle singles/EPs in discography mode |

### Examples

```bash
# Album with specific output dir
ytm-album "Boards of Canada" "Music Has the Right to Children" --output-dir ~/Music

# Full discography, no prompt, more parallelism
ytm-album "Tycho" -y -j 8

# Use Chrome's cookies instead of Firefox
ytm-album "Phoebe Bridgers" "Punisher" --browser chrome
```

## How it works

1. **`ytmusicapi`** searches YouTube Music for the album/artist and returns canonical metadata (title, track list, video IDs, cover art URLs).
2. For each track, **`yt-dlp`** downloads the audio stream (`bestaudio[ext=m4a]`) using cookies from your browser to unlock the Premium 256kbps AAC stream.
3. **`mutagen`** writes proper MP4 tags from the ytmusicapi metadata directly — no reliance on yt-dlp's flaky YouTube Music metadata extraction.
4. **High-res cover** is fetched directly from YouTube Music's image proxy (with the `=w1200-h1200-l90-rj` size hint).

## Troubleshooting

**Getting 128kbps instead of 256kbps?** The cookies aren't being read. Make sure:
- You're logged into music.youtube.com in the specified browser
- The browser is closed (or use `--browser firefox:default` for a specific profile)
- Your Premium subscription is active

**Verify a single track**:
```bash
yt-dlp --cookies-from-browser firefox -F "https://music.youtube.com/watch?v=<video-id>"
```
You should see a format with ~256k AAC.

**Discography missing albums?** YouTube Music's API returns inconsistent data for some artists. The script tries three fallback strategies (artist page → all-albums browse endpoint → search). For artists with very large discographies, some might still be missed — open an issue with the artist name and I'll dig in.

## License

MIT — see `LICENSE`.
