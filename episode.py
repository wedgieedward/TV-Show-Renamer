import logging
import os
import re

DEV_LOGGER = logging.getLogger("Tv_show")

DESIRED_REGEX = r'.*((s|S)\d\d((e|E)\d\d)(-(e|E)\d\d)?)+\..*'
KNOWN_REGEX = r'(\d\d - \d\d|\d\d\.\d|\d\d)(( ?- | )(.*))?'
EPISODE_REGEX = r'Episode (\d+)'

class Episode(object):
    """
    Object representing an episode of a given TV Show
    """

    def __init__(self, current_name, season_path, tv_show, season):
        self.tv_show = tv_show.lower().replace(' ', '.')
        self.season = season

        self._season_path = season_path
        self._current_name, self._extension = os.path.splitext(current_name)
        self._new_name = None
        self._fixed = False
        self._already_fixed = False

        # An array of episode numbers ['01'] or ['01', '02']
        # useful for two parters
        self._episode_number = None

    def find_new_name(self):
        """
        Rename the episode to the desired regex convention
        name.s01e02.ext
        """
        name_is_desired = re.search(DESIRED_REGEX, self._current_name)
        if name_is_desired:
            DEV_LOGGER.info("Episode %s is already in desired format" % self._current_name)
            self._already_fixed = True
            return True

        name_known = re.search(KNOWN_REGEX, self._current_name)
        if name_known:
            self._new_name = '%s.' % self.tv_show
            self._episode_number = name_known.group(1).replace(' ', '').split('-')
            for episode_number in self._episode_number:
                self._new_name += 's%se%s.' % (self.season, episode_number)

            safe_title = False
            try:
                title = name_known.group(4)
                if title is not None:
                    safe_title = True
            except IndexError, TypeError:
                pass

            if safe_title:
                self._new_name += title.lower().replace(' ', '.')
            else:
                self._new_name = self._new_name[:-1]
            self._new_name += self._extension
            self._fixed = True
            return True

        episode_known = re.search(EPISODE_REGEX, self._current_name)
        if episode_known:
            self._new_name = '%s.' % self.tv_show
            self._episode_number = episode_known.group(1).split('-')
            for episode_number in self._episode_number:
                self._new_name += 's%se%s' % (self.season, episode_number)
            self._fixed = True
            return True

        else:
            return False

    def rename(self):
        """
        Does the actual renaming of the files
        """
        original = self._season_path + '/' + self._current_name + self._extension
        new_name = self._season_path + '/' + self._new_name
        print original + ' \tbecomes \t' + new_name
        try:
            os.rename(original, new_name)
        except OSError:
            print "FATAL ERROR TRYING TO RENAME %s" % original






