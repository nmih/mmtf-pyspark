#!/user/bin/env python
'''
secondaryStructureSegmentExtractor.py:

This class creates a dataset of sequence segments of specified length
and associate secondary structure information. Sequence and secondary
structure strings are split into segments using a sliding window of the specified
segment length. The dataset contains the sequence segment and the DSP Q8 and
DSSP Q3 secondary structure annotation of the cneter residue. Therefore, the segment
length must be an odd number

Authorship information:
    __author__ = "Mars (Shih-Cheng) Huang"
    __maintainer__ = "Mars (Shih-Cheng) Huang"
    __email__ = "marshuang80@gmail.com:
    __status__ = "Done"
'''

from mmtfPyspark.datasets import secondaryStructureExtractor
from mmtfPyspark.mappers import structureToSecondaryStructureSegments
from mmtfPyspark.ml import pythonRDDToDataset

def getDataset(structureRDD, length):
    '''
    Returns a dataset of sequence segments of the specified length and
    the DSSP Q8 and Q3 code of the center residue in a segment.

    Attributes:
        structureRDD: structure
        length (int): segment length, must be an odd number

    Returns:
        dataset of segments
    '''

    if length % 2 == 0:
        raise Exception("Segment length must be an odd number %i" % length)

    rows = secondaryStructureExtractor.getPythonRdd(structureRDD) \
            .flatMap(structureToSecondaryStructureSegments(length))

    colNames = ["structureChainId", "sequence", "labelQ8", "labelQ3"]
    return pythonRDDToDataset.getDataset(rows, colNames)
