from etl.spark_session import get_spark_session


HADOOP_AZURE_JAR = (
    "/home/yumeda/.ivy2.5.2/cache/"
    "org.apache.hadoop/hadoop-azure/jars/"
    "hadoop-azure-3.4.2.jar"
)


def main():
    spark = (
        get_spark_session()
        .builder
        .config("spark.jars", HADOOP_AZURE_JAR)
        .getOrCreate()
    )

    try:
        jvm = spark.sparkContext._jvm
        hadoop_conf = spark.sparkContext._jsc.hadoopConfiguration()

        print("=" * 60)
        print("TESTANDO REGISTRO DO WASBS")
        print("=" * 60)

        filesystem_class = (
            jvm.org.apache.hadoop.fs.FileSystem.getFileSystemClass(
                "wasbs",
                hadoop_conf,
            )
        )

        print("WASBS REGISTRADO!")
        print("Classe:", filesystem_class.getName())

    except Exception:
        print("=" * 60)
        print("WASBS NÃO ESTÁ REGISTRADO")
        print("=" * 60)
        raise

    finally:
        spark.stop()


if __name__ == "__main__":
    main()