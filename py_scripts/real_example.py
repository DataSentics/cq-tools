# Databricks notebook source
# MAGIC %md
# MAGIC ### Setup

# COMMAND ----------

import os
import pyspark.sql.types as T
import pyspark.sql.functions as f
from adap_spark.utils import write_df, get_path, get_table

# COMMAND ----------

# MAGIC %md
# MAGIC ### Variables

# COMMAND ----------

# retrieving environment variable from pipeline parameters
read_env = os.environ.get("READ_ENV")
current_env = os.environ.get("CURRENT_ENV")

# name of the output table and parquet
output_name = 'mosaic'

input_layer = 'raw'
output_layer = 'parsed'

data_type = 'dataoneoff'
data_source = 'experian'

database_name = '{}_{}'.format(data_type, data_source)

# COMMAND ----------

target_path = get_path(path=[data_type, data_source, output_layer], file_name=output_name, env=current_env)
target_table = get_table(table_name='{}_{}'.format(output_layer, output_name), database_name=database_name, env=current_env)

# COMMAND ----------

input_file_name = 'Experian_Mosaic.csv'
input_path = get_path(path=[data_type, data_source, input_layer], file_name=input_file_name, env=current_env)

# COMMAND ----------

file_type = "csv"
infer_schema = "true"

# COMMAND ----------

# MAGIC %md
# MAGIC ### Input

# COMMAND ----------

df = (spark.read.format(file_type)
      .option("inferSchema", infer_schema)
      .option("header", True)
      .option("sep", ',')
      .load(input_path)
     )

# COMMAND ----------

# MAGIC %md
# MAGIC ### Transformations

# COMMAND ----------



# COMMAND ----------

# MAGIC %md
# MAGIC ### Save

# COMMAND ----------

write_df(df=df, table_name=target_table, spark=spark, path=target_path)