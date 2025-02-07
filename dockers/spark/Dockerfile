FROM spark:3.5.3-java17-python3

USER root
# Install Python and pip
RUN apt-get update && pip install lakeops

# Set environment variables
ENV SPARK_HOME=/opt/spark
ENV SPARK_CONF_DIR=/opt/spark/conf
ENV PATH=$PATH:$SPARK_HOME/bin

COPY config/spark-defaults.conf $SPARK_CONF_DIR/

# Download necessary JARs
RUN wget https://repo1.maven.org/maven2/org/apache/iceberg/iceberg-spark-runtime-3.5_2.12/1.4.2/iceberg-spark-runtime-3.5_2.12-1.4.2.jar -P $SPARK_HOME/jars/ && \
    wget https://repo1.maven.org/maven2/io/delta/delta-spark_2.12/3.3.0/delta-spark_2.12-3.3.0.jar -P $SPARK_HOME/jars/ && \
    wget https://repo1.maven.org/maven2/io/delta/delta-storage/3.3.0/delta-storage-3.3.0.jar -P $SPARK_HOME/jars/ && \
    wget https://repo1.maven.org/maven2/io/delta/delta-iceberg_2.12/3.3.0/delta-iceberg_2.12-3.3.0.jar -P $SPARK_HOME/jars/ && \
    wget https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.2/hadoop-aws-3.3.2.jar -P $SPARK_HOME/jars/ && \
    wget https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.261/aws-java-sdk-bundle-1.12.261.jar -P $SPARK_HOME/jars/ && \
    wget https://repo1.maven.org/maven2/io/unitycatalog/unitycatalog-spark_2.12/0.2.1/unitycatalog-spark_2.12-0.2.1.jar -P $SPARK_HOME/jars/ && \
    wget https://repo1.maven.org/maven2/io/unitycatalog/unitycatalog-client/0.2.1/unitycatalog-client-0.2.1.jar -P $SPARK_HOME/jars/


RUN chown -R spark:spark $SPARK_HOME

WORKDIR /app
USER spark
