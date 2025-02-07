from pyspark.sql import SparkSession
from deltalake import DeltaTable
from prepare_dataset import get_table_storage_path

# def enable_uniform_table(uniform_schema_name, schema_name, table_name):
#     print("Before enabling uniform table")
#     spark.sql(f"""
#         DESC EXTENDED {schema_name}.{table_name}
#     """).show(truncate=False)
#
#     # TODO: atm, we can not alter table from UC, the update function has not implemented yet
#     # spark.sql(f"""
#     #     ALTER TABLE {schema_name}.{table_name}
#     #     SET TBLPROPERTIES (
#     #         'delta.enableIcebergCompatV2' = 'true',
#     #         'delta.universalFormat.enabledFormats' = 'iceberg'
#     #     )
#     # """)
#
#     df = spark.table(f"{schema_name}.{table_name}")
#     table_path = get_table_storage_path(uniform_schema_name, table_name)
#     df.write.mode("overwrite").option("delta.enableIcebergCompatV2", "true").option(
#         "delta.universalFormat.enabledFormats", "iceberg"
#     ).save(table_path)
#
#     print("After enabling uniform table")
#     spark.sql(f"""
#         DESC EXTENDED {uniform_schema_name}.{table_name};
#     """).show(truncate=False)


def enable_uniform(schema_name, table_name):
    """
    Enable Uniform the test dataset
    """
    # spark = SparkSession.builder.appName("Enable Uniform").getOrCreate()

    # Load the table
    table_path = get_table_storage_path(schema_name, table_name)
    if not DeltaTable.is_deltatable(table_path):
        raise ValueError(f"Table {table_path} is not a Delta table")

    dt = DeltaTable(table_path)
    # dt.alter.set_table_properties({
    #     "delta.enableIcebergCompatV2": "true",
    #     "delta.universalFormat.enabledFormats": "iceberg"
    # })

    dt.alter.set_table_properties({"delta.enableChangeDataFeed": "true"})
    dt.alter.set_table_properties({"delta.enableIcebergCompatV2": "true"})


    # uniform_schema_name = "demo_uniform"
    # spark.sql(f"CREATE SCHEMA IF NOT EXISTS {uniform_schema_name}")
    # # Should now show two schemas: default and demo
    # spark.sql("SHOW SCHEMAS").show()
    #
    # # Should now show two schemas: default and demo
    # spark.sql(f"SHOW TABLES FROM {schema_name}").show()
    #
    # enable_uniform_table(spark, uniform_schema_name, schema_name, "transactions")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--schema-name",
        type=str,
        help="Schema name to enable uniform",
    )
    parser.add_argument(
        "--table-name",
        type=str,
        help="Table name to enable uniform",
    )
    args = parser.parse_args()


    print("Enable uniform ...")
    schema_name = "demo_delta"
    enable_uniform(schema_name=args.schema_name, table_name=args.table_name)
