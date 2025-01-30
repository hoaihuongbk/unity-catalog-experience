# Unity Catalog Experience

This repository documents the exploration and testing of Unity Catalog OSS version 0.2.1, focusing on various table formats and their compatibility with centralized catalog management.

## Overview

Testing and validating different data formats and operations using Unity Catalog:
- Delta tables
- Iceberg tables
- Parquet files
- Uniform format integration

## Current Testing Status

### Working Features
- Delta table read/write operations
- Schema management

### In Progress/Limited Support
- Native Iceberg table writes
- Uniform format integration
- REST API compatibility testing

## Usage Examples

```python
# Write data into a external location
table_path = f"/app/data/{schema_name}/{table_name}"
df.write.format(table_format).mode("overwrite").option(
    "mergeSchema", "true"
).save(table_path)

# Create table in Unity Catalog
spark.sql(f"""
    CREATE OR REPLACE TABLE {schema_name}.{table_name}
    USING {table_format}
    LOCATION '{table_path}'
""")
```

## Updates
This repository is actively maintained with latest findings and compatibility updates as Unity Catalog evolves. Check back regularly for:

- New feature support
- Workarounds for unsupported operations
- Best practices
- Integration patterns

## Contributing
Feel free to open issues or PRs to share your experiences with Unity Catalog OSS version.