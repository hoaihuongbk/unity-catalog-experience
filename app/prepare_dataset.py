from pyspark.sql.functions import *
from pyspark.sql import SparkSession
from lakeops import LakeOps
from lakeops.core.engines import SparkEngine


def get_table_storage_path(schema_name, table_name):
    return f"/app/data/{schema_name}/{table_name}"


def write_table(spark, df, schema_name, table_name, table_format="parquet"):
    """
    Write a DataFrame to a table in the specified table format.

    Args:
        spark: SparkSession instance
        df: DataFrame to write
        schema_name: Name of the schema/database
        table_name: Name of the table to create
        table_format: Format to save table as ('parquet', 'delta', or 'iceberg'). Default is 'parquet'.

    The function writes the DataFrame to an external location and creates a table in the catalog
    using the specified format. For Delta and Iceberg formats, additional options are set to ensure
    compatibility and proper functionality.
    """

    # Write data into a external location
    table_path = get_table_storage_path(schema_name, table_name)

    engine = SparkEngine(spark)
    ops = LakeOps(engine)

    # writer = df.write.mode("overwrite").option("mergeSchema", "true")

    table_options = {"mergeSchema": "true"}
    # if table_format == "delta":
    #     table_options = {
    #         "delta.minReaderVersion": "2",
    #         "delta.minWriterVersion": "7",
    #         "delta.columnMapping.mode": "name",
    #     }

    ops.write(df, table_path, format=table_format, options=table_options)

    # Write the data to the table
    # writer.format(table_format).save(table_path)

    # Create table in Unity Catalog
    spark.sql(f"""
        CREATE OR REPLACE TABLE {schema_name}.{table_name}
        USING {table_format}
        LOCATION '{table_path}'
    """)

    # List the files in the Delta table
    # List all tables in the demo_delta schema
    # First verify the table format
    # spark.sql("SHOW CREATE TABLE unity.demo_delta.transactions").show(truncate=False)

    # spark.sql(f"""
    #     OPTIMIZE {schema_name}.{table_name}
    # """).show(truncate=False)
    #
    spark.sql(f"""
        DESC EXTENDED {schema_name}.{table_name}
    """).show(truncate=False)


def prepare_dataset(table_format="parquet"):
    """
    Prepare the dataset with specified table format.
    Args:
        table_format (str): Format to save tables. Can be 'parquet', 'delta', or 'iceberg'. Default is 'parquet'.
    """
    spark = SparkSession.builder.appName("Prepare Dataset").getOrCreate()

    # Create new schema
    # catalog_name = "unity"
    schema_name = f"demo_{table_format}"
    spark.sql(f"CREATE SCHEMA IF NOT EXISTS {schema_name}")

    # Should now show two schemas: default and demo
    spark.sql("SHOW SCHEMAS").show()

    ## Create the transactions table
    transaction_size = 150000000
    transactions_df = spark.range(0, transaction_size).select(
        "id",
        round(rand() * 10000, 2).alias("amount"),
        (col("id") % 10).alias("country_id"),
        (col("id") % 100).alias("store_id"),
    )

    write_table(spark, transactions_df, schema_name, "transactions", table_format)

    ## Create the stores table
    stores_df = spark.range(0, 99).select(
        "id",
        round(rand() * 100, 0).alias("employees"),
        (col("id") % 10).alias("country_id"),
        expr("uuid()").alias("name"),
    )

    write_table(spark, stores_df, schema_name, "stores", table_format)

    ## Create the countries table
    countries = [
        (0, "Italy"),
        (1, "Canada"),
        (2, "Mexico"),
        (3, "China"),
        (4, "Germany"),
        (5, "UK"),
        (6, "Japan"),
        (7, "Korea"),
        (8, "Australia"),
        (9, "France"),
        (10, "Spain"),
        (11, "USA"),
    ]

    columns = ["id", "name"]
    countries_df = spark.createDataFrame(data=countries, schema=columns)

    write_table(spark, countries_df, schema_name, "countries", table_format)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--table-format",
        type=str,
        default="parquet",
        choices=["parquet", "delta", "iceberg"],
        help="Table format to use",
    )
    args = parser.parse_args()

    if args.table_format == "iceberg":
        print("WARNING: iceberg is not supported natively yet")
        exit(1)

    print("Preparing dataset...")
    prepare_dataset(table_format=args.table_format)
