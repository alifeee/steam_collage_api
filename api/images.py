
def getImageUrlForGameId(game_id: int):
    """Get image url for game id

    Args:
        game_id (int): Game id

    Returns:
        str: Image url
    """
    return f"https://cdn.cloudflare.steamstatic.com/steam/apps/{game_id}/header.jpg"

