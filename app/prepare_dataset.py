from pyspark.sql.functions import *
from pyspark.sql import SparkSession


def write_table(spark, df, schema_name, table_name, table_format="parquet"):
    """
    Write a DataFrame to a table in the specified table format.
    :param spark:
    :param df:
    :param schema_name:
    :param table_name:
    :param table_format:
    :return:
    """

    final_table_format = table_format
    if table_format == "iceberg":
        # Need to use uniform, write table as delta and allow to read from iceberg client
        final_table_format = "delta"

    # Write data into a external location
    table_path = f"/app/data/{schema_name}/{table_name}"
    df.write.format(final_table_format).mode("overwrite").option(
        "mergeSchema", "true"
    ).save(table_path)

    # Create table in Unity Catalog
    spark.sql(f"""
        CREATE OR REPLACE TABLE {schema_name}.{table_name}
        USING {final_table_format}
        LOCATION '{table_path}'
    """)

    # TODO: this alter doesn't work for iceberg at this moment
    # if table_format == "iceberg":
    #     # Enable uniform format for iceberg
    #     spark.sql(f"""
    #         ALTER TABLE {schema_name}.{table_name}
    #         SET TBLPROPERTIES (
    #             'delta.enableIcebergCompatV2' = 'true',
    #             'delta.universalFormat.enabledFormats' = 'iceberg'
    #         )
    #    """)


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

    print("Preparing dataset...")
    prepare_dataset(table_format=args.table_format)
