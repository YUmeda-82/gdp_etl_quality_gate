from delta import configure_spark_with_delta_pip
from pyspark.sql import SparkSession


HADOOP_AZURE_JAR = (
    "/home/yumeda/.ivy2.5.2/cache/"
    "org.apache.hadoop/hadoop-azure/jars/"
    "hadoop-azure-3.4.2.jar"
)


def get_spark_session() -> SparkSession:
    """
    Creates or reuses a SparkSession configured for Azurite local storage
    with Delta Lake support.
    """

    builder = (
        SparkSession.builder.appName("gdp_etl_quality_gate")
        .config("spark.jars", HADOOP_AZURE_JAR)
        .config(
            "spark.hadoop.fs.azure.account.auth.type.devstoreaccount1.blob.core.windows.net",
            "SharedKey",
        )
        .config(
            "spark.hadoop.fs.azure.account.key.devstoreaccount1.blob.core.windows.net",
            "Eby8vdM02xNOcqFlUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==",
        )
        .config(
            "spark.hadoop.fs.azure.storage.emulator.enabled",
            "true",
        )
        .config(
            "spark.hadoop.fs.azure.storage.emulator.account.name",
            "devstoreaccount1",
        )
        .config(
            "spark.hadoop.fs.azure.storage.emulator.rest.endpoint",
            "http://127.0.0.1:10000",
        )
        .config(
            "spark.sql.extensions",
            "io.delta.sql.DeltaSparkSessionExtension",
        )
        .config(
            "spark.sql.catalog.spark_catalog",
            "org.apache.spark.sql.delta.catalog.DeltaCatalog",
        )
    )

    return configure_spark_with_delta_pip(
        builder,
        extra_packages=[
            "org.apache.hadoop:hadoop-azure:3.4.2",
        ],
    ).getOrCreate()
