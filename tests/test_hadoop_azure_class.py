from etl.spark_session import get_spark_session


def main():
    spark = get_spark_session()

    try:
        jvm = spark.sparkContext._jvm

        print("=" * 60)
        print("SPARK CLASSPATH")
        print("=" * 60)

        classpath = jvm.java.lang.System.getProperty("java.class.path")

        for entry in classpath.split(":"):
            print(entry)

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