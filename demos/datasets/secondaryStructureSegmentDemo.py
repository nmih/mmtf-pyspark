#!/usr/bin/env python
'''
secondaryStructureSegmentDemo.py:

Authorship information:
    __author__ = "Mars (Shih-Cheng) Huang"
    __maintainer__ = "Mars (Shih-Cheng) Huang"
    __email__ = "marshuang80@gmail.com:
    __status__ = "Done"
'''

from pyspark import SparkConf, SparkContext
from mmtfPyspark.io import MmtfReader
from mmtfPyspark.mappers import structureToPolymerChains
from mmtfPyspark.filters import containsLProteinChain
from mmtfPyspark.datasets import secondaryStructureSegmentExtractor, secondaryStructureExtractor
import time


def main():
    start = time.time()

    conf = SparkConf().setMaster("local[*]") \
                      .setAppName("secondaryStructureSegmentDemo")
    sc = SparkContext(conf = conf)

    pdb = MmtfReader.downloadMmtfFiles(["1STP"],sc)

    pdb = pdb.flatMap(structureToPolymerChains()) \
             .filter(containsLProteinChain())

    segmentLength = 25
    ds = secondaryStructureSegmentExtractor.getDataset(pdb,segmentLength)

    ds.show(50, False)

    end = time.time()

    print("Time: %f  sec." %(end-start))

    sc.stop()

if __name__ == "__main__":
    main()
