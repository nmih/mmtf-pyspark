#!/user/bin/env python
'''
groupInteractionExtractor.py:

Creates a dataset of interactions of a specified group within
a cutoff distance. Groups are specified by there
Chemical Component identifier (residue name), e.g., "ZN", "ATP".

Authorship information:
    __author__ = "Mars (Shih-Cheng) Huang"
    __maintainer__ = "Mars (Shih-Cheng) Huang"
    __email__ = "marshuang80@gmail.com:
    __status__ = "Done"
'''

from mmtfPyspark.ml import pythonRDDToDataset
from mmtfPyspark.utils.structureToAllInteractions import *

class groupInteractionExtractor(object):
    '''
    Attributes:
        groupName (String): name of the group to be analyzed
        distance (float): cutoff distance
    '''

    def __init__(self, groupName, distance):
        self.groupName = groupName
        self.distance = distance


    def getDataset(self, structures):
        '''Returns a dataset of residues that interact with specified group within
        a specified cutoff distance

        Attricutes:
            structure (pythonRdd): a set of PDB structures
        Returns:
            dataset with interacting residue and atom information
        '''
        # create a list of all residues with a threshold distance
        rows = structures.flatMap(structureToAllInteractions(self.groupName, self.distance))

        # convert to a dataset
        colNames = ["structureId", "residue1", "atom1", "element1", "index1",
                    "residue2", "atom2", "element2", "index2", "distance"]
        return pythonRDDToDataset.getDataset(rows, colNames)
