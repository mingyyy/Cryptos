from pyspark.sql import SparkSession
import pyspark.sql.functions as F

spark = SparkSession.builder.appName("StructuredNetworkWordCount").getOrCreate()
spark.sparkContext.setLogLevel("ERROR")
df_lines = spark.readStream.format("socket").option("host", "localhost")\
        .option("port", 9999).load()
df_words = df_lines.select(
            F.explode(
                F.split(df_lines.value, " ")
                ).alias("word")
            )
df_wc = df_words.groupBy("word").count()
query = df_wc.writeStream.outputMode("complete").format("console").start()
query.awaitTermination()

# To run:
# terminal 1: nc -lk 9999
# terminal 2: bin/spark-submit ../../src/temp/structured_stream_quick_start.py localhost 9999

