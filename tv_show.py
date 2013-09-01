import logging
import os
import re
import sys

from pprint import pprint

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
        # print "\tShow: %s has been created at path: %s" % (self.name, self.path)

    def get_episodes(self):
        """
        gets all the episodes relating to that show
        """
        abs_path = os.path.abspath(self.path)
        for _dirname, dirnames, _filenames in os.walk(abs_path):
            for season in dirnames:
                season_match = re.search(self.se_regex, season)
                if season_match:
                    season_number = season_match.group(2)
                    if len(season_number) == 1:
                        season_number = '0' + season_number
                    season_path = abs_path + '/' + season
                    for _sdirname, _sdirnames, episodes in os.walk(season_path):
                        for episode_name in episodes:
                            if episode_name.endswith((video_const.VIDEO_FILES)):
                                self.episodes += [Episode(episode_name,
                                                        season_path,
                                                        self.name,
                                                        season_number)]
            break

    def rename_episodes(self):
        """
        Go through each episode and rename them
        """
        for episode in self.episodes:
            success = episode.find_new_name()
            if not success:
                DEV_LOGGER.info("Problem scraping %s into desired format" % episode)

        naming_structures = {"No Action Needed": [],
                             "Episodes To Be Renamed": [],
                             "Episodes That Cannot Be Renamed": []}

        print self.name
        for episode in self.episodes:
            if episode._already_fixed:
                naming_structures["No Action Needed"] += [episode._current_name]
            elif episode._fixed:
                naming_structures["Episodes To Be Renamed"] += [(episode._current_name,
                                                                 episode._new_name)]
            else:
                naming_structures["Episodes That Cannot Be Renamed"] += [episode._current_name]

        
        if len(naming_structures["Episodes To Be Renamed"]) == 0:
            print "No action could be worked out, either all shows correctly named or in an incorrect folder format"
        else:
            pprint(naming_structures)
            user_input = raw_input("Is This Okay? (y|n): ")
            if user_input == 'y':
                for episode in self.episodes:
                    if episode._fixed:
                        episode.rename()
            else:
                print "NO FURTHER ACTION"


