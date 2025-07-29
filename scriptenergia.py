import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import col
from awsglue.dynamicframe import DynamicFrame


"""
    Este código lee desde el AWS Glue Datacatalog dos tablas en una base de datos, después realiza un join entre ambas tablas y calcula el total de la venta. 
    Finalmente, escribe el resultado en un archivo Parquet en S3. 
"""

args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

dyf_transacciones = glueContext.create_dynamic_frame.from_catalog(
    database="dbbronce", 
    table_name="transacciones",
    transformation_ctx="dyf_transacciones"
)

dyf_clientes = glueContext.create_dynamic_frame.from_catalog(
    database="dbbronce",
    table_name="clientes",
    transformation_ctx="dyf_clientes"
)

df_transacciones = dyf_transacciones.toDF()
df_clientes = dyf_clientes.toDF()
df_transacciones = df_transacciones.withColumn("energia_kwh", col("energia_kwh").cast("int"))
df_transacciones = df_transacciones.withColumn("price", col("precio_total_usd").cast("float"))
   
df_joined = df_transacciones.join(df_clientes, on="id_cliente", how="inner")

df_transformed = df_joined.withColumn("total_amount", col("energia_kwh") * col("precio_total_usd"))

dyf_transformed = DynamicFrame.fromDF(df_transformed, glueContext, "dyf_transformed")

glueContext.write_dynamic_frame.from_options(
    frame = dyf_transformed,
    connection_type = "s3",
    connection_options = {"path": "s3://datawarehouse-energia-carlos"},
    format = "parquet",
    transformation_ctx = "write_parquet"
)

job.commit()