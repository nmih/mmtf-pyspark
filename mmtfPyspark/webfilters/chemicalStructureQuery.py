#!/user/bin/env python
'''
chemicalStructureQuery.py

This filter returns entries that contain groups with specified chemical structures (SMILES string).
This chemical structure query supports for query: exact, similar, substructure, and superstructure.
For details see:

<a href="http://www.rcsb.org/pdb/staticHelp.do?p=help/advancedsearch/chemSmiles.html">Chemical Structure Search</a>.

Authorship information:
    __author__ = "Mars (Shih-Cheng) Huang"
    __maintainer__ = "Mars (Shih-Cheng) Huang"
    __email__ = "marshuang80@gmail.com:
    __status__ = "Done"
'''

from mmtfPyspark.webfilters import advancedQuery

class chemicalStructureQuery(object):

    EXACT = "Exact"
    SIMILAR = "Similar"
    SUBSTRUCTURE = "Substructure"
    SUPERSTRUCTURE = "Superstructure"

    def __init__(self, smiles, queryType = "Substructure", percentSimilarity = 0):
        '''
        Constructor to setup filter that matches any entry with at least one chemical component
        that matches the specified SMILES string using the specified query type.
        For details see:
            <a href="http://www.rcsb.org/pdb/staticHelp.do?p=help/advancedsearch/chemSmiles.html">Chemical Structure Search</a>.

        Attribute:
            smiles (String): SMILES string representing chemical structure
            queryType: One of the 4 supported types
            percentSimilarity: percent similarity for similarity search. This parameter is
                               ignored for all other query types
        '''

        if not (queryType == self.EXACT \
                or queryType == self.SIMILAR \
                or queryType == self.SUBSTRUCTURE \
                or queryType == self.SUPERSTRUCTURE):

                raise Exception("Invalid search type: %s" %queryType)

        query = "<orgPdbQuery>" + \
                   "<queryType>org.pdb.query.simple.ChemSmilesQuery</queryType>" + \
        	       "<smiles>" + smiles + "</smiles>" + \
        	       "<searchType>" + queryType + "</searchType>" + \
        	       "<similarity>" + str(percentSimilarity) + "</similarity>" + \
        	       "<polymericType>Any</polymericType>" + \
               "</orgPdbQuery>"

        self.filter = advancedQuery(query)


    def __call__(self, t):
        return self.filter(t)
