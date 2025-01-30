SHELL := /bin/bash

setup:
	@echo "Initializing the testing environment"
	@docker compose up -d --build


prepare_dataset:
	@echo "Preparing the dataset with table format=$(table_format) for the spark job"
	@docker exec -it uc-spark-master spark-submit \
		--master spark://uc-spark-master:7077 \
		/app/prepare_dataset.py --table-format=$(table_format);


resync_schema:
	@echo "Resyncing the schema with the latest version"
	@docker exec -it uc-spark-master spark-submit \
		--master spark://uc-spark-master:7077 \
		/app/resync_schema.py --table-format=$(table_format);