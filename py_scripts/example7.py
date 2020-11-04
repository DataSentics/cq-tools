# Databricks notebook source
# MAGIC %sh 
# MAGIC 
# MAGIC # SecretClient
# MAGIC 
# MAGIC find /dbfs/ -name "src"

# COMMAND ----------

# MAGIC %run 

# COMMAND ----------

# %run

# COMMAND ----------

spark.conf.get("spark.sql.files.maxPartitionBytes")

# COMMAND ----------

# MAGIC %sh 
# MAGIC 
# MAGIC ls -la /dbfs/mnt/prod_solutions/sdm/out/nonpersonal

# COMMAND ----------

# MAGIC %sh 
# MAGIC 
# MAGIC du -h --max-depth=1 /dbfs/mnt/prod_solutions/sdm/out/ticketing_transactiontable
