#!/user/bin/env python
'''
blastCluster.py

This filter passes through representative structures from the RCSB PDB
BlastCLust cluster. A sequence identity thresholds needs to be specified.
The representative for each cluster is the first chain in a cluster.

<p>See <a href="http://www.rcsb.org/pdb/statistics/clusterStatistics.do"> BlastClust cluster.
field names.</a>

<p>Example: find representative PDB entries at 90% sequence identity.

<pre><code>
     int sequenceIdentity = 90;
          pdb = pdb.filter(new BlastCluster(90));
</code></pre>

Authorship information:
    __author__ = "Mars (Shih-Cheng) Huang"
    __maintainer__ = "Mars (Shih-Cheng) Huang"
    __email__ = "marshuang80@gmail.com:
    __status__ = "Done"
'''

import urllib.request

class blastCluster(object):
    '''
    Filters blast clusters

    Attributes:
        sequenceIdentity (Int): sequence indentity for blast
    '''
    def __init__(self, sequenceIdentity):

        clusters = self.getBlastCluster(sequenceIdentity)

        self.pdbIds = set()

        for protein in clusters:
            self.pdbIds.add(protein)
            self.pdbIds.add(protein[:4])


    def __call__(self, t):
        return t[0] in self.pdbIds


    def getBlastCluster(self, sequenceIdentity):

        if sequenceIdentity not in [30,40,50,70,90,95,100]:
            raise Exception(f"Error: representative chains are not availible for \
                            sequence Identity {sequenceIdentity}.\n Must be in \
                            range [30,40,50,70,90,95,100]")
            return

        coreUrl = "ftp://resources.rcsb.org/sequence/clusters/"
        clusters = []
        inputStream = urllib.request.urlopen(f"{coreUrl}bc-{sequenceIdentity}.out")

        for line in inputStream:
            line = str(line)[2:-3].replace("_",".").strip("\\n")
            clusters += line.split(" ")

        return clusters
