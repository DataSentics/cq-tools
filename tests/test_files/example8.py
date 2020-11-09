read_env = os.environ.get("READ_ENV")

for table in input_tables:
  try:
    table_name = get_table(table_name='{}_{}'.format(input_layer,table), database_name = database_name, env=read_env)
    spark.sql('refresh table ' + table_name)
    exec("df_{} = spark.table('{}')".format(table, table_name))
  except:
    print('{} does not exist'.format(table))
