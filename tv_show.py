import logging
import os
import re
import sys

import video_const
from episode import Episode


DEV_LOGGER = logging.getLogger("Tv_show")


class Tv_show(object):
    """
    Object representation for a Tv_show
    """
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.episodes = []
        self.se_regex = r'(Season|Series|Volume) (\d*)'
        print "Show: %s has been created at path: %s" % (self.name, self.path)

    def get_episodes(self):
        """
        gets all the episodes relating to that show
        """
        print "Gathering Episodes for TVShow %s at path %s" % (self.name, self.path)
        abs_path = os.path.abspath(self.path)
        for _dirname, dirnames, _filenames in os.walk(abs_path):
            for season in dirnames:
                season_match = re.search(self.se_regex, season)
                if season_match:
                    season_number = season_match.group(2)
                    print "%s has been found" % season
                    season_path = abs_path + '/' + season
                    for _sdirname, _sdirnames, episodes in os.walk(season_path):
                        for episode_name in episodes:
                            if episode_name.endswith((video_const.VIDEO_FILES)):
                                print "Video %s has been found" % (episode_name)
                                episode_path = season_path + '/' + episode_name
                                self.episodes += [Episode(episode_name,
                                                        episode_path,
                                                        self.name,
                                                        season_number)]
            break

    def rename_episodes(self):
        """
        Go through each episode and rename them
        """
        for episode in self.episodes:
            success = episode.rename()
            if not success:
                DEV_LOGGER.info("Problem renaming %s" % episode)
