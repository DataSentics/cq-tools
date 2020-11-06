import sys

exec("df_{}_{} = spark.table('{}')".format('fsfan' , 'profile_attribute_simple', table_name))


if __name__ == "__main__":
    pass

