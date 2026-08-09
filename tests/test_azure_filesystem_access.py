from etl.spark_session import get_spark_session


def main():
    spark = get_spark_session()

    try:
        jvm = spark.sparkContext._jvm
        hadoop_conf = spark.sparkContext._jsc.hadoopConfiguration()

        uri = jvm.java.net.URI(
            "wasbs://bronze@devstoreaccount1/"
        )

        print("=" * 60)
        print("TESTANDO ACESSO AO AZURITE VIA WASBS")
        print("=" * 60)
        print("URI:", uri)

        filesystem = jvm.org.apache.hadoop.fs.FileSystem.get(
            uri,
            hadoop_conf,
        )

        print("FILESYSTEM CRIADO!")
        print("Classe:", filesystem.getClass().getName())

        path = jvm.org.apache.hadoop.fs.Path("/")

        print("=" * 60)
        print("LISTANDO CONTEÚDO DO CONTAINER")
        print("=" * 60)

        statuses = filesystem.listStatus(path)

        if len(statuses) == 0:
            print("Container vazio.")
        else:
            for status in statuses:
                print(status.getPath())

        print("=" * 60)
        print("ACESSO AO AZURITE VIA WASBS FUNCIONOU!")
        print("=" * 60)

    finally:
        spark.stop()


if __name__ == "__main__":
    main()