from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from models import db, Artist, Album, Cover
import api_client
from datetime import datetime

music_bp = Blueprint("music", __name__)


# Home page route
@music_bp.route("/")
def home():
    return render_template("home.html")


# Search results route
@music_bp.route("/search")
@login_required
def search():
    artist = request.args.get("artist")
    album = request.args.get("album")

    if not artist or not album:
        flash("Artist and Album are required for search.", "error")
        return redirect(url_for("music.home"))

    parsed_data = api_client.search_musicbrainz(artist, album)

    if parsed_data is None:
        flash("The album could not be found.", "error")
        return redirect(url_for("music.home"))

    # Grabbing cover art
    cover_art_url = api_client.search_cover_art_archive(parsed_data["mbid"])
    parsed_data["cover_art"] = (
        cover_art_url or "path/to/default/image.png"
    )  # Fallback image

    return render_template("album_search.html", album=parsed_data)


# Add to list route
@music_bp.route("/add_to_list/<mbid>", methods=["POST"])
@login_required
def add_to_list(mbid):
    # Check for duplicate
    existing_album = db.session.scalar(db.select(Album).where(Album.mbid == mbid))
    if existing_album:
        flash("This album is already in your list.", "error")
        return redirect(url_for("music.home"))

    # Get data from the form
    artist_name = request.form.get("artist")
    album_name = request.form.get("album")
    release_date_str = request.form.get("release_date")
    genres = request.form.get("genres")
    cover_art = request.form.get("cover_art")

    # Find or create the artist
    artist = db.session.scalar(db.select(Artist).where(Artist.name == artist_name))
    if not artist:
        artist = Artist(name=artist_name)
        db.session.add(artist)

    # Clean up the date
    try:
        # Handle full YYYY-MM-DD
        release_date = datetime.strptime(release_date_str, "%Y-%m-%d").date()
    except ValueError:
        try:
            # Handle YYYY-MM
            release_date = datetime.strptime(release_date_str, "%Y-%m").date()
        except ValueError:
            try:
                # Handle YYYY
                release_date = datetime.strptime(release_date_str, "%Y").date()
            except ValueError:
                # Fallback
                release_date = datetime.strptime("1900-01-01", "%Y-%m-%d").date()

    # Create the new album and cover
    new_album = Album(
        name=album_name,
        mbid=mbid,
        release_date=release_date,
        genres=genres,
        artist=artist,
    )

    new_cover = Cover(
        cover_art_url=cover_art,
        album=new_album,
    )

    db.session.add_all([new_album, new_cover])
    db.session.commit()

    flash("Album added to your list!", "success")
    return redirect(url_for("music.home"))


# View all albums route
@music_bp.route("/all_albums")
@music_bp.route("/all_albums/<int:page>")
@login_required
def all_albums(page=1):
    albums_pagination = (
        db.session.query(Album)
        .join(Artist)
        .order_by(Artist.name, Album.name)
        .paginate(page=page, per_page=5, error_out=False)
    )

    if not albums_pagination.items and page > 1:
        flash("Invalid page number.", "error")
        return redirect(url_for("music.all_albums"))

    return render_template("lists.html", albums_pagination=albums_pagination)


# Delete album route
@music_bp.route("/delete/<mbid>", methods=["POST"])
@login_required
def delete_album(mbid):
    # Find the album
    album_to_delete = db.session.scalar(db.select(Album).where(Album.mbid == mbid))

    if album_to_delete:
        db.session.delete(album_to_delete)
        db.session.commit()
        flash("Album removed from your list.", "success")
    else:
        flash("Album not found.", "error")

    return redirect(url_for("music.all_albums"))
