import time
from ytmusicapi import YTMusic
from ytmusicapi.auth.oauth.credentials import OAuthCredentials
from ytmusicapi.auth.oauth.token import Token
from ytmusicapi.auth.types import AuthType
import logging
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_AUTH_FILE = str(BASE_DIR / "browser.json")
SEARCH_DELAY = 0.5
YT_PLAYLIST_BASE_URL = "https://music.youtube.com/playlist?list="

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class YTMusicService:

    def __init__(self):
        self.yt = YTMusic(DEFAULT_AUTH_FILE)

    def sync_live_setlist(
        self, artist_name: str, live_title: str, song_names: list
    ) -> str | None:
        logger.info(f"开始同步{artist_name}的演出歌单: {live_title}")

        song_ids = []

        for song in song_names:
            query = f"{artist_name} {song}"

            results = self.yt.search(query, filter="songs", limit=1)
            if results:
                song_id = results[0]["videoId"]
                song_ids.append(song_id)
                time.sleep(SEARCH_DELAY)
            else:
                logger.info(f"未找到歌曲:{song}")

        if not song_ids:
            logger.info(f"未找到任何匹配的歌曲，创建歌单失败")
            return None

        playlist_name = f"{artist_name} - {live_title}"

        exist_playlists = self.yt.get_library_playlists()
        target_playlist_id = next(
            (
                pl["playlistId"]
                for pl in exist_playlists
                if pl["title"] == playlist_name
            ),
            None,
        )

        description = (
            f"Auto-generated setlist for {live_title} via live-setlist-creater"
        )

        if target_playlist_id:
            logger.info(f"已存在歌单{playlist_name}")
            try:
                logger.info(f"尝试删除现存歌单{playlist_name}")
                self.yt.delete_playlist(target_playlist_id)
            except Exception as e:
                logger.error(f"删除已存在歌单失败: {e}")

        logger.info(f"正在生成歌单{playlist_name}")
        playlist_id = self.yt.create_playlist(
            title=playlist_name, description=description, video_ids=song_ids
        )

        url = f"{YT_PLAYLIST_BASE_URL}{playlist_id}"
        return url
