#!/user/bin/env python
'''
containsAlternativeLocations.py

This filter return true if this structure contains an alternative location

Authorship information:
    __author__ = "Mars (Shih-Cheng) Huang"
    __maintainer__ = "Mars (Shih-Cheng) Huang"
    __email__ = "marshuang80@gmail.com:
    __status__ = "Done"
'''

class containsAlternativeLocations(object):

    def __call__(self,t):
        structure = t[1]

        for c in structure.alt_loc_list:
            if c != '\0': return True

        return False
