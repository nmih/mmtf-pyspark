'''
sequenceNgrammer.py

This class contians methods for creating overlapping and non-overlapping
n-grams of one-letter code sequence
(e.g., protein sequences)

Authorship information:
    __author__ = "Mars (Shih-Cheng) Huang"
    __maintainer__ = "Mars (Shih-Cheng) Huang"
    __email__ = "marshuang80@gmail.com:
    __status__ = "Done"
'''

from pyspark.sql import SparkSession, types


def ngram(data, n, outputCol):
    '''
    Splits a one-letter sequence column (e.g., protein sequence)
    into array of overlapping n-grams.

    <p> Example 2-gram: IDCGH ... => [ID, DC, CG, GH, ...]

    Attribute:
        data (dataset): input dataset with column "sequence"
        n (int): size of the n-gram
        outputCol (String): name of the output column

    Return:
        output dataset with appended ngram column
    '''

    session = SparkSession.builder.getOrCreate()

    #Encoder function to be passed as User Defined Function (UDF)
    def _ngrammer(s):
        ngram = []
        i = 0

        if len(s) < 1:
            return []

        while i < len(s) - n + 1:
            ngram.append(s[i: i + n])
            i += 1

        return ngram

    session.udf.register("ngrammer", _ngrammer, types.ArrayType(types.StringType()))

    data.createOrReplaceTempView("table")
    sql = f"SELECT *, ngrammer(sequence) AS {outputCol} from table"

    data = session.sql(sql)

    return data


def shiftedNgram(data, n, shift, outputCol):
    '''
    Splits a one-letter sequence column (e.g., protein sequence)
	into array of non-overlapping n-grams. To generate all possible n-grams,
	this method needs to be called n times with shift parameters {0, ..., n-1}.

	<p> Example 3-gram(shift=0) : IDCGHTVEDQR ... => [IDC, GHT, VED, ...]
	<p> Example 3-gram(shift=1) : IDCGHTVEDQR ... => [DCG, HTV, EDQ, ...]
	<p> Example 3-gram(shift=2) : IDCGHTVEDQR ... => [CGH, TVE, DQR, ...]

	<p>For an application of shifted n-grams see:
	E Asgari, MRK Mofrad, PLoS One. 2015; 10(11): e0141287, doi:
	<a href="https://dx.doi.org/10.1371/journal.pone.0141287">10.1371/journal.pone.0141287</a>

    Attribute:
        data (dataset): input dataset with column "sequence"
        n (int): size of the n-gram
        shift(int): start index for the n-gram
        outputCol (String): name of the output column

    Return:
        output dataset with appended ngram column
    '''

    session = SparkSession.builder.getOrCreate()

    #Encoder function to be passed as User Defined Function (UDF)
    def _ngrammer(s):
        ngram = []
        i,j = 0,0
        t = int(len(s)/n)

        if len(s) < shift:
            return []

        s = s[shift:]

        while j < t:
            ngram.append(s[i: i + n])
            j += 1
            i += n

        return ngram

    session.udf.register("ngrammer", _ngrammer, types.ArrayType(types.StringType()))

    data.createOrReplaceTempView("table")
    sql = f"SELECT *, ngrammer(sequence) AS {outputCol} from table"

    data = session.sql(sql)

    return data
