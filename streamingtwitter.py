import sys

from pyspark import SparkContext
from pyspark.streaming import StreamingContext


if __name__ == "__main__":

    sc = SparkContext(appName="StreamingWordCount")
    ssc = StreamingContext(sc, 2)

    ssc.checkpoint("file:///tmp/spark")

    lines = ssc.socketTextStream("localhost", 7789)

    def countWords(newValues, lastSum):
      if lastSum is None:
        lastSum = 0
      return sum(newValues, lastSum)  

    word_counts = lines.flatMap(lambda line: line.split(" "))\
                  .filter(lambda w: w.startswith("#"))\
                  .map(lambda word: (word, 1))\
                  .updateStateByKey(countWords)

    word_counts.pprint()

    ssc.start()
    ssc.awaitTermination()
