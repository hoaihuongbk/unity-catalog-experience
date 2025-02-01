#!/bin/bash

mysql -P 9030 -h 127.0.0.1 -u root --prompt="StarRocks > " <<EOF
create external catalog uc properties (
    "type" = "iceberg",
    "iceberg.catalog.type" = "rest",
    "iceberg.catalog.uri" = "http://uc-server:8080/api/2.1/unity-catalog/iceberg",
    "iceberg.catalog.security" = "oauth2",
    "iceberg.catalog.oauth2.token" = "not_used",
    "iceberg.catalog.warehouse" = "unity"
);
EOF