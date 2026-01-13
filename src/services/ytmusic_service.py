import time
from ytmusicapi import YTMusic
import logging
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import random

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_AUTH_FILE = str(BASE_DIR / "browser.json")
YT_PLAYLIST_BASE_URL = "https://music.youtube.com/playlist?list="

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class YTMusicService:

    def __init__(self, max_workers: int = 3):
        self.yt = YTMusic(DEFAULT_AUTH_FILE)
        self.MIN_DELAY = 0.3
        self.MAX_WORKERS = max_workers

    def sync_live_setlist(
        self, artist_name: str, live_title: str, song_names: list[str]
    ) -> str | None:
        logger.info(f"开始同步{artist_name}的演出歌单: {live_title}")

        with ThreadPoolExecutor(max_workers=self.MAX_WORKERS) as executor:
            results = list(
                executor.map(
                    lambda song_name: self._search_song(artist_name, song_name),
                    song_names,
                )
            )
        song_ids = [song_id for song_id in results if song_id]

        if not song_ids:
            logger.info(f"未找到任何匹配的歌曲，创建歌单失败")
            return None

        playlist_name = f"{artist_name} - {live_title}"
        description = (
            f"Auto-generated setlist for {live_title} via live-setlist-creater"
        )

        try:
            playlist_id = self._upsert_playlist(playlist_name, description, song_ids)
            return f"{YT_PLAYLIST_BASE_URL}{playlist_id}"
        except Exception as e:
            logger.error(f"同步歌单失败: {e}")
            return None

    def _search_song(self, artist: str, song: str) -> str | None:
        time.sleep(self.MIN_DELAY + random.random())
        query_word = f"{artist} {song}"
        results = self.yt.search(query_word, filter="songs", limit=1)
        if results:
            return results[0]["videoId"]
        logger.info(f"未找到歌曲:{song}")
        return None

    def _upsert_playlist(
        self, playlist_name: str, description: str, song_ids: list[str]
    ) -> str:
        exist_playlists = self.yt.get_library_playlists()
        target_playlist_id = next(
            (
                pl["playlistId"]
                for pl in exist_playlists
                if pl["title"] == playlist_name
            ),
            None,
        )
        if target_playlist_id:
            logger.info(f"已存在歌单{playlist_name}")
            current_tracks = self.yt.get_playlist(target_playlist_id)["tracks"]
            if current_tracks:
                self.yt.remove_playlist_items(target_playlist_id, current_tracks)
            self.yt.add_playlist_items(target_playlist_id, song_ids)
            final_playlist_id = target_playlist_id
        else:
            logger.info(f"正在生成歌单{playlist_name}")
            final_playlist_id = self.yt.create_playlist(
                title=playlist_name, description=description, video_ids=song_ids
            )

        return final_playlist_id
