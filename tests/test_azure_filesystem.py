from etl.spark_session import get_spark_session


def main():
    spark = get_spark_session()

    try:
        jvm = spark.sparkContext._jvm
        hadoop_conf = spark.sparkContext._jsc.hadoopConfiguration()

        filesystem_class = jvm.org.apache.hadoop.fs.FileSystem.getFileSystemClass(
            "wasbs://bronze@devstoreaccount1/",
            hadoop_conf,
        )

        print("=" * 60)
        print("Azure Filesystem encontrado!")
        print("Classe:", filesystem_class.getName())
        print("=" * 60)

    finally:
        spark.stop()


if __name__ == "__main__":
    main()