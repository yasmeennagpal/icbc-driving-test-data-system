# spark/etl.py

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, when, avg, count


spark = (
    SparkSession.builder
    .appName(" Driving Test ETL")
    .config("spark.hadoop.io.native.lib.available", "false")
    .config("spark.sql.warehouse.dir", "file:///C:/temp/spark-warehouse") 
    .config(
        "spark.sql.sources.commitProtocolClass",
        "org.apache.spark.sql.execution.datasources.SQLHadoopMapReduceCommitProtocol"
    )
    .config("spark.hadoop.mapreduce.fileoutputcommitter.algorithm.version", "2")
    .getOrCreate()
)

# -------------------------
# 2. Extract (CSV without header)
# -------------------------
input_path = "C:/Users/yasme/Downloads/drivingtests.csv"

df = spark.read.csv(
    input_path,
    header=False,
    inferSchema=True
)

# Assign column names explicitly
df = df.toDF(
    "TestID",
    "LicenseNumber",
    "TestDate",
    "Location",
    "ExaminerID",
    "Result",
    "Errors",
    "Timestamp"
)

print("Data extracted")
df.show(5)

# -------------------------
# 3. Transform (clean + enrich)
# -------------------------
df_clean = (
    df
    .withColumn("Location", trim(col("Location")))
    .withColumn("Result", trim(col("Result")))
    .withColumn(
        "PassFlag",
        when(col("Result") == "PASS", 1).otherwise(0)
    )
)

print("Data cleaned and enriched")
df_clean.show(5)

# -------------------------
# 4. Analytics
# -------------------------

# Pass rate by location
pass_rate_by_location = (
    df_clean
    .groupBy("Location")
    .agg(
        avg("PassFlag").alias("PassRate"),
        count("*").alias("TotalTests")
    )
)

print("Pass rate by location")
pass_rate_by_location.show()

# Average errors by examiner
avg_errors_by_examiner = (
    df_clean
    .groupBy("ExaminerID")
    .agg(avg("Errors").alias("AvgErrors"))
)

print("Average errors by examiner")
avg_errors_by_examiner.show()

from pyspark.sql.functions import asc

lowest_pass_rate_city = pass_rate_by_location.orderBy(asc("PassRate")).limit(1)

print("City with lowest pass rate")
lowest_pass_rate_city.show()

from pyspark.sql.functions import desc

highest_pass_rate_city = pass_rate_by_location.orderBy(desc("PassRate")).limit(1)

print("City with highest pass rate")
highest_pass_rate_city.show()

# -------------------------
# 5. Load (write outputs)
# -------------------------
base_output = "file:///C:/temp/tests_outputs"

df_clean.coalesce(1).write.mode("overwrite").parquet(
    f"{base_output}/cleaned_driving_tests"
)

pass_rate_by_location.write.mode("overwrite").parquet(
    f"{base_output}/pass_rate_by_location"
)

avg_errors_by_examiner.write.mode("overwrite").parquet(
    f"{base_output}/avg_errors_by_examiner"
)

print("All outputs written")

spark.stop()
