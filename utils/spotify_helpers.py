def is_explicit(track):
    """Checks if a song is explicit."""
    return track.get("explicit", False)
