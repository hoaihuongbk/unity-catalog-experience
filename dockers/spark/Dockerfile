FROM apache/spark:3.5.3

USER root
# Install Python and pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Set environment variables
ENV SPARK_HOME=/opt/spark
ENV SPARK_CONF_DIR=/opt/spark/conf
ENV PATH=$PATH:$SPARK_HOME/bin

COPY extra-jars/* $SPARK_HOME/jars/
COPY config/spark-defaults.conf $SPARK_CONF_DIR/

RUN chown -R spark:spark $SPARK_HOME

WORKDIR /app
USER spark
