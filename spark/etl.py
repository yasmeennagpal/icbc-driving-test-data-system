# spark/etl.py

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, when, avg, count

spark = (
    SparkSession.builder
    .appName("ETL")
    .config("spark.hadoop.io.native.lib.available", "false")
    .getOrCreate()
)



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

print("✓ Data extracted")
df.show(5)


df_clean = (
    df
    .withColumn("Location", trim(col("Location")))
    .withColumn("Result", trim(col("Result")))
    .withColumn(
        "PassFlag",
        when(col("Result") == "PASS", 1).otherwise(0)
    )
)

print("✓ Data cleaned and enriched")
df_clean.show(5)

# Pass rate by location
pass_rate_by_location = (
    df_clean
    .groupBy("Location")
    .agg(
        avg("PassFlag").alias("PassRate"),
        count("*").alias("TotalTests")
    )
)

print("✓ Pass rate by location")
pass_rate_by_location.show()

# Average errors by examiner
avg_errors_by_examiner = (
    df_clean
    .groupBy("ExaminerID")
    .agg(avg("Errors").alias("AvgErrors"))
)

print("✓ Average errors by examiner")
avg_errors_by_examiner.show()

from pyspark.sql.functions import asc

lowest_pass_rate_city = pass_rate_by_location.orderBy(asc("PassRate")).limit(1)

print("City with lowest pass rate")
lowest_pass_rate_city.show()

from pyspark.sql.functions import desc

highest_pass_rate_city = pass_rate_by_location.orderBy(desc("PassRate")).limit(1)

print("City with highest pass rate")
highest_pass_rate_city.show()

# Create data directory
import os
os.makedirs("data", exist_ok=True)

# ALL ETL TRANSFORMATIONS DONE IN SPARK 
# Only the final file write uses Pandas to avoid Windows Hadoop issues
df_clean_pd = df_clean.toPandas()
df_clean_pd.to_csv("data/driving_tests_clean.csv", index=False)

print("✓ Spark ETL complete - Data saved successfully")

spark.stop()
