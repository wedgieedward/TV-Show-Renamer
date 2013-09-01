import os
import sys
from tv_show import Tv_show

class Renamer(object):
    """
    Renamer class
    """
    def __init__(self, paths):
        self._paths = paths
        self._shows = []

    def gather_tv_shows(self):
        """
        gather tv show information
        """
        for path in self._paths:
            abs_path = os.path.abspath(path)
            for _dirname, dirnames, _filenames in os.walk(abs_path):
                for tv_show_name in dirnames:
                    self._shows += [Tv_show(tv_show_name, abs_path + '/' + tv_show_name)]
                break

    def gather_episodes(self):
        """
        Will go through each tv_show and gather all known episodes
        """
        for show in self._shows:
            show.get_episodes()

    def rename_episodes(self):
        """
        rename all episodes belonging to each tv show
        """
        for show in self._shows:
            show.rename_episodes()


if __name__ == '__main__':
    paths = []
    if len(sys.argv) == 2:
        paths += [sys.argv[1]]

    elif len(sys.argv) >2:
        # multiple folders to check
        for path in sys.argv[1:]:
            paths += [path]
    else:
        print "Invalid number of arguments, please specify root path or paths of your TV Shows"

    renamer = Renamer(paths)
    renamer.gather_tv_shows()
    renamer.gather_episodes()
    renamer.rename_episodes()


