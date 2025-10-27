import requests


# Searches MusicBrainz for album
def search_musicbrainz(artist, album):
    artist_query = requests.utils.quote(artist)
    album_query = requests.utils.quote(album)

    url = f"https://musicbrainz.org/ws/2/release?query={artist_query} AND release:{album_query}&fmt=json"
    headers = {"User-Agent": "PythonMusicTracker/0.1 ( your-email@example.com )"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an error for bad responses (4xx, 5xx)
        data = response.json()

        if data.get("count", 0) == 0:
            return None  # No releases found

        # Parse and return the first release
        release = data["releases"][0]
        parsed_data = {
            "artist": release["artist-credit"][0]["name"],
            "album": release["title"],
            "mbid": release["id"],
            "release_date": release.get(
                "date", "1900-01-01"
            ),  # Default date if missing
            "genres": ", ".join(tag.get("name") for tag in release.get("tags", [])),
        }
        return parsed_data

    except requests.RequestException as e:
        print(f"API Error: {e}")  # Log this error
        return None
    except (KeyError, IndexError):
        print("Error parsing API response")
        return None


# Searches CoverArtArchive for album art
def search_cover_art_archive(mbid):
    url = f"https://coverartarchive.org/release/{mbid}/front-250"
    headers = {"User-Agent": "PythonMusicTracker/0.1 ( your-email@example.com )"}

    try:
        # Set allow_redirects=False because the API returns a 307 Redirect
        # to the actual image URL. We just want that URL.
        response = requests.head(url, headers=headers, allow_redirects=False)

        if response.status_code == 307:
            return response.headers.get("Location")  # This is the image URL
        else:
            return None  # No cover art found

    except requests.RequestException:
        return None
