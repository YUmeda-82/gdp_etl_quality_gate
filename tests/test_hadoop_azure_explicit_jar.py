from pyspark.sql import SparkSession


HADOOP_AZURE_JAR = (
    "/home/yumeda/.ivy2.5.2/cache/"
    "org.apache.hadoop/hadoop-azure/jars/"
    "hadoop-azure-3.4.2.jar"
)


def main():
    spark = (
        SparkSession.builder
        .appName("test_hadoop_azure_class")
        .config("spark.jars", HADOOP_AZURE_JAR)
        .getOrCreate()
    )

    try:
        jvm = spark.sparkContext._jvm

        print("=" * 60)
        print("TESTANDO HADOOP AZURE")
        print("=" * 60)

        azure_class = jvm.java.lang.Class.forName(
            "org.apache.hadoop.fs.azure.NativeAzureFileSystem"
        )

        print("HADOOP AZURE CARREGADO!")
        print("Classe:", azure_class.getName())

    except Exception:
        print("=" * 60)
        print("HADOOP AZURE NÃO ESTÁ DISPONÍVEL NO JVM")
        print("=" * 60)
        raise

    finally:
        spark.stop()


if __name__ == "__main__":
    main()