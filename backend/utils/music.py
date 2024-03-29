from yandex_music import Client, Track
from datetime import datetime as dt
import random


class Music:
  def __init__(self) -> None:
    self.s = None
    self.client: Client = None
    # self.radio: Radio = None
    self.track: Track = None
    self.liked: list = []
    self.prev_track: Track = None
    self.idx: int = None

  @property
  def meta(self):
    return dict(title=self.track.title, author=self.artists, cover=self.track_cover, duration=self.track.duration_ms / 1000,
                url=self._extract_url(), isLiked=self.is_liked, id=self.track.id)
  
  @property
  def artists(self):
    total_artists = len(self.track.artists)
    concatenator = ',' if total_artists > 3 else '&'
    if total_artists < 2:
      return self.track.artists[0].name
    return concatenator.join([artist.name for artist in self.track.artists])
  
  @property
  def is_liked(self):
    return self.track.id in self.liked
  
  def _extract_url(self, track_id=None):
    track_id = track_id if track_id else self.track.id
    dl = self.client.tracks_download_info(track_id, get_direct_links=True)
    best_link = max([link.bitrate_in_kbps for link in dl if link.codec == self.s.AUDIO_CODEC])
    i = max([index for index, link in enumerate(dl) if link.bitrate_in_kbps == best_link])
    return dl[i].direct_link
  
  def like_track(self, trackId=None, **kwargs):
    track_id = trackId if trackId else self.track.id
    self.client.users_likes_tracks_add(track_id)
    self.liked.append(track_id)
    return 'like', None
  
  def unlike_track(self, trackId=None, **kwargs):
    track_id = trackId if trackId else self.track.id
    self.client.users_likes_tracks_remove(track_id)
    self.liked.remove(track_id)
    return 'unlike', None
  
  def dislike_track(self, trackId=None, **kwargs):
    track_id = trackId if trackId else None
    self.client.users_dislikes_tracks_add(track_id)
    return 'dislike', None
  
  def search(self, query, **kwargs):
    result = 
