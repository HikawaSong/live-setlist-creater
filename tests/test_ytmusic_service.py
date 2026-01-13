import pytest
from src.services.ytmusic_service import YTMusicService

from collections import Counter


def test_search_create_playlist():
    artist = "Roselia"
    live_title = "「Stille Nacht, Rosen Nacht」＠武蔵野の森総合スポーツプラザ (東京都)"
    songs = [
        "Symbol I : △",
        "Symbol II : Air",
        "Symbol III : ▽",
        "Symbol IV : Earth",
        "Ave mujica Ether",
        "Sage der Rosen",
        "Song I am.",
        "THE HISTORIC...",
        "Determination Symphony",
        "FIRE BIRD",
        "約束",
        "礎の花冠",
        "Neo-Aspect",
        "Re:birth day",
        "Floral Heaven",
        "PASSIONATE ANTHEM",
        "R",
        "-HEROIC ADVENT-",
        "Our Carol",
    ]

    service = YTMusicService()
    url = service.sync_live_setlist(
        artist_name=artist, live_title=live_title, song_names=songs
    )

    assert url is not None
    print(f"\n 测试成功，生成的歌单: {url}")
