from delta import configure_spark_with_delta_pip
from pyspark.sql import SparkSession


HADOOP_AZURE_JAR = (
    "/home/yumeda/.ivy2.5.2/cache/"
    "org.apache.hadoop/hadoop-azure/jars/"
    "hadoop-azure-3.4.2.jar"
)

DELTA_PATH = "wasbs://bronze@devstoreaccount1/delta_test"


def main():
    builder = (
        SparkSession.builder
        .appName("test_delta_write_azurite")
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

    spark = (
        configure_spark_with_delta_pip(
            builder,
            extra_packages=[
                "org.apache.hadoop:hadoop-azure:3.4.2",
            ],
        )
        .getOrCreate()
    )

    try:
        rw_data = [
            {"id": 1, "pais": "Brasil", "valor": 100},
            {"id": 2, "pais": "Argentina", "valor": 200},
            {"id": 3, "pais": "Chile", "valor": 300},
        ]

        print("=" * 60)
        print("TESTE: createDataFrame + Delta + WASBS + Azurite")
        print("=" * 60)

        df = spark.createDataFrame(rw_data)

        print("DataFrame criado:")
        df.show()

        print("=" * 60)
        print("GRAVANDO DELTA")
        print("=" * 60)
        print(f"Destino: {DELTA_PATH}")

        (
            df.write
            .format("delta")
            .mode("overwrite")
            .save(DELTA_PATH)
        )

        print("=" * 60)
        print("GRAVAÇÃO DELTA CONCLUÍDA!")
        print("=" * 60)

        print("=" * 60)
        print("LENDO DELTA NOVAMENTE")
        print("=" * 60)

        df_read = (
            spark.read
            .format("delta")
            .load(DELTA_PATH)
        )

        df_read.show()

        print("=" * 60)
        print("LEITURA DELTA CONCLUÍDA!")
        print("=" * 60)

        print("=" * 60)
        print("SUCESSO!")
        print("Delta + WASBS + Azurite funcionando.")
        print("=" * 60)

    finally:
        spark.stop()


if __name__ == "__main__":
    main()