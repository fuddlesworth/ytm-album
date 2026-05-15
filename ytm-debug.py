#!/usr/bin/env python3
"""Debug ytmusicapi discography lookup for a given artist."""
import sys
from ytmusicapi import YTMusic

if len(sys.argv) < 2:
    print("Usage: ytm-debug.py <artist name>")
    sys.exit(1)

artist = sys.argv[1]
yt = YTMusic()

ar = yt.search(artist, filter="artists", limit=1)
if not ar:
    print("No artist found")
    sys.exit(0)
ar = ar[0]
ch = ar["browseId"]
print(f"Channel: {ch}  Name: {ar['artist']}")

data = yt.get_artist(ch)
print(f"\nArtist page sections: {list(data.keys())}")

for key in ("albums", "singles"):
    section = data.get(key) or {}
    inline = section.get("results", [])
    params = section.get("params")
    print(f"\n[{key}] inline={len(inline)}  params={'YES' if params else 'NO'}")
    if params:
        try:
            full = yt.get_artist_albums(ch, params)
            print(f"  get_artist_albums: {len(full)} items")
            for r in full[:3]:
                print(f"    - {r.get('title')!r}  ({r.get('year')})  type={r.get('type')}")
        except Exception as e:
            print(f"  get_artist_albums FAILED: {type(e).__name__}: {e}")

s = yt.search(artist, filter="albums", limit=200)
print(f"\nsearch(albums, limit=200): {len(s)} raw results")
exact = [r for r in s if any(a.get('name','').lower() == artist.lower() for a in r.get('artists', []))]
contains = [r for r in s if any(artist.lower() in a.get('name','').lower() for a in r.get('artists', []))]
print(f"  exact-name match: {len(exact)}")
print(f"  contains match: {len(contains)}")
print(f"\nFirst 5 search results' artist fields:")
for r in s[:5]:
    names = [a.get('name') for a in r.get('artists', [])]
    print(f"  {r.get('title')!r} -> {names}")
