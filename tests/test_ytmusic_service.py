import pytest
from src.services.ytmusic_service import YTMusicService


def test_search_create_playlist():
    artist = "Roselia"
    live_title = "Roselia ASIA TOUR「Neuweltfahrt」- 大阪"
    songs = [
        "FRONTIER FANTASIA",
        "Song I am.",
        "Determination Symphony",
        "紫炎",
        "R",
        "熱色スターマイン",
        "Ringing Bloom",
        "陽だまりロードナイト",
        "軌跡",
        "BLACK SHOUT",
        "Steadfast Spirits",
        "Neo-Aspect",
        "FIRE BIRD",
        "PASSIONATE ANTHEM",
    ]

    service = YTMusicService()
    url = service.sync_live_setlist(
        artist_name=artist, live_title=live_title, song_names=songs
    )

    assert url is not None
    print(f"\n✅ 测试成功，生成的歌单: {url}")
