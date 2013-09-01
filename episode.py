class Episode(object):
    """
    Object representing an episode of a given TV Show
    """
    def __init__(self, current_name, path, tv_show, season):
        self.Tv_show = tv_show
        self.season = season
        self._path = path
        self._current_name = current_name
        self._new_name = None

        self._fixed = False

    def __str__(self):
        """ String representation of episode """
        ret_string = ''.join([self.Tv_show, self.season, self.episode])

    def rename(self):
        """ Rename the episode to the desired regex convention """
        # Not Implemented
        return True


