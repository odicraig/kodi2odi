"""
    SALTS XBMC Addon
    Copyright (C) 2014 tknorris

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import re
import urllib
import urlparse
import kodi
import log_utils  # @UnusedImport
import dom_parser
from salts_lib import scraper_utils
from salts_lib.constants import FORCE_NO_MATCH
from salts_lib.constants import VIDEO_TYPES
from salts_lib.constants import XHR
import scraper

BASE_URL = 'http://movytvy.com'

class Scraper(scraper.Scraper):
    base_url = BASE_URL
    
    def __init__(self, timeout=scraper.DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.base_url = kodi.get_setting('%s-base_url' % (self.get_name()))

    @classmethod
    def provides(cls):
        return frozenset([VIDEO_TYPES.MOVIE, VIDEO_TYPES.TVSHOW, VIDEO_TYPES.EPISODE])

    @classmethod
    def get_name(cls):
        return 'MovyTvy'

    def get_sources(self, video):
        source_url = self.get_url(video)
        hosters = []
        if source_url and source_url != FORCE_NO_MATCH:
            page_url = urlparse.urljoin(self.base_url, source_url)
            html = self._http_get(page_url, require_debrid=True, cache_limit=.5)
            fragment = dom_parser.parse_dom(html, 'table', {'class': '[^"]*links-table[^"]*'})
            if fragment:
                for row in dom_parser.parse_dom(fragment[0], 'tr'):
                    match = re.search("playVideo\.bind\(.*?'([^']+)(?:[^>]*>){2}(.*?)</td>", row, re.DOTALL)
                    if match:
                        stream_url, release = match.groups()
                        if self._get_direct_hostname(stream_url) == 'gvideo':
                            sources = self._parse_google(stream_url)
                        else:
                            sources = [stream_url]
                        
                        for source in sources:
                            host = self._get_direct_hostname(source)
                            if host == 'gvideo':
                                quality = scraper_utils.gv_get_quality(source)
                                direct = True
                            else:
                                host = urlparse.urlparse(source).hostname
                                if video.video_type == VIDEO_TYPES.MOVIE:
                                    meta = scraper_utils.parse_movie_link(release)
                                else:
                                    meta = scraper_utils.parse_episode_link(release)
                                base_quality = scraper_utils.height_get_quality(meta['height'])
                                quality = scraper_utils.get_quality(video, host, base_quality)
                                direct = False
                            hoster = {'multi-part': False, 'host': host, 'class': self, 'quality': quality, 'views': None, 'rating': None, 'url': source, 'direct': direct}
                            hosters.append(hoster)
            
        return hosters

    def _get_episode_url(self, show_url, video):
        show_url = urlparse.urljoin(self.base_url, show_url)
        html = self._http_get(show_url, require_debrid=True, cache_limit=8)
        fragment = dom_parser.parse_dom(html, 'div', {'class': '[^"]*seasons[^"]*'})
        if fragment:
            match = re.search('href="([^"]+)[^>]*>%s<' % (video.season), html)
            if match:
                season_url = scraper_utils.pathify_url(match.group(1))
                episode_pattern = 'href="([^"]*/seasons/%s/episodes/%s(?!\d)[^"]*)' % (video.season, video.episode)
                title_pattern = 'href="(?P<url>[^"]+)[^>]*>Episode\s+\d+\s+-\s+(<?P<title>[^<]+)'
                return self._default_get_episode_url(season_url, video, episode_pattern, title_pattern)

    def search(self, video_type, title, year, season=''):  # @UnusedVariable
        results = []
        media_type = 'series' if video_type == VIDEO_TYPES.TVSHOW else 'movie'
        search_url = urlparse.urljoin(self.base_url, '/typeahead/%s' % (urllib.quote(title)))
        headers = {'Referer': self.base_url}
        headers.update(XHR)
        html = self._http_get(search_url, headers=headers, require_debrid=True, cache_limit=.5)
        for item in scraper_utils.parse_json(html, search_url):
            match_title = item.get('title')
            match_url = item.get('link')
            match_year = ''
            if item.get('type') == media_type and match_title and match_url:
                if not year or not match_year or year == match_year:
                    result = {'title': scraper_utils.cleanse_title(match_title), 'year': match_year, 'url': scraper_utils.pathify_url(match_url)}
                    results.append(result)
            
        return results
