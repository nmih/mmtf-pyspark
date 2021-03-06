#!/user/bin/env python
'''
MMTFWriter.py

Encodes and write MMTF encoded structure data to a Hadoop Sequence File

Authorship information:
    __author__ = "Mars (Shih-Cheng) Huang"
    __maintainer__ = "Mars (Shih-Cheng) Huang"
    __email__ = "marshuang80@gmail.com:
    __status__ = "Done"
'''

from mmtf.api.mmtf_writer import MMTFEncoder
from mmtfPyspark.io import mmtfStructure
import gzip
import msgpack
import os

def writeSequenceFile(path, sc, structure, compressed = True):
    '''
    Encodes and writes MMTF encoded structure data to a Hadoop Sequnce File

    Attributes:
        path (str): Path to Hadoop file directory)
        sc (Spark context)
        structure (tuple): structure data to be written
        compress (bool): if true, apply gzip compression
    '''
    if structure.first()[1] == mmtfStructure:
        structure.map(lambda s: (s[0],s[1].set_alt_loc_list()) \
                                 if not s[1].alt_loc_set \
                                 else s) \

    structure.map(lambda t: (t[0], toByteArray(t[1], compressed))).saveAsHadoopFile(path,
                       "org.apache.hadoop.mapred.SequenceFileOutputFormat",
                       "org.apache.hadoop.io.Text",
                       "org.apache.hadoop.io.BytesWritable")


def writeMmtfFiles(path, sc, structure):
    '''
    Encodes and writes MMTF encoded and gzipped structure data to individual .mmtf.gz files.

    Attributes:
    path (str): Path to Hadoop file directory)
    sc (Spark context)
    structure (tuple): structure data to be written
    '''

    if path[-1] != "/":
        path = path + "/"

    if not os.path.exists(path):
        os.makedirs(path)

    structure = structure.map(lambda s: (s[0],s[1].set_alt_loc_list()) \
                                  if not s[1].alt_loc_set \
                                  else s) \
                .map(lambda t: (t[0], toByteArray(t[1], False))) \
                .foreach(lambda t: gzip.open(path + t[0] + '.mmtf.gz', mode = 'wb').write(t[1]))


def toByteArray(structure, compressed):
    '''
    Returns an MMTF-encoded byte array with optional gzip compression

    Returns:
        MMTF encoded and optionally gzipped structure data
    '''

    byte_array = bytearray(msgpack.packb(MMTFEncoder.encode_data(structure)))

    if compressed:
        return gzip.compress(byte_array)
    else:
        return byte_array
