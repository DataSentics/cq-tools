current_env = os.environ.get("READ_ENV")
current_env = os.environ.get("CURRENT_ENV") 

target_table = get_table(table_name='{}_{}'.format(output_layer, output_name), database_name=database_name, env=current_env)
write_df(df=df, table_name=target_table, spark=spark, path=target_path)
