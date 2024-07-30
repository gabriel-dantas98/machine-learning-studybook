import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from recipe_transforms import *
from awsglue.dynamicframe import DynamicFrame
import gs_now
from pyspark.sql import functions as SqlFuncs

# Generated recipe steps for DataPreparationRecipe_node1721964147886
def applyRecipe_node1721964147886(inputFrame, glueContext, transformation_ctx):
    frame = inputFrame.toDF()
    gc = glueContext
    df1 = DateTimeFunctions.DateDiff.apply(
        data_frame=frame,
        glue_context=gc,
        transformation_ctx="DataPreparationRecipe_node1721964147886-df1",
        target_column="diff_data_source_com_execucao_glue_minutos",
        units="MINUTES",
        source_column1="data_extracao",
        source_column2="date_glue_execuction",
    )
    return DynamicFrame.fromDF(df1, gc, transformation_ctx)

def sparkAggregate(glueContext, parentFrame, groups, aggs, transformation_ctx) -> DynamicFrame:
    aggsFuncs = []
    for column, func in aggs:
        aggsFuncs.append(getattr(SqlFuncs, func)(column))
    result = parentFrame.toDF().groupBy(*groups).agg(*aggsFuncs) if len(groups) > 0 else parentFrame.toDF().agg(*aggsFuncs)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Script generated for node Amazon S3
AmazonS3_node1721963138730 = glueContext.create_dynamic_frame.from_options(format_options={}, connection_type="s3", format="parquet", connection_options={"paths": ["s3://gd-ibov-data/b3-2024-07-26.parquet"], "recurse": True}, transformation_ctx="AmazonS3_node1721963138730")

# Script generated for node Drop other column
Dropothercolumn_node1721963433418 = DropFields.apply(frame=AmazonS3_node1721963138730, paths=["other"], transformation_ctx="Dropothercolumn_node1721963433418")

# Script generated for node Rename quantidade field
Renamequantidadefield_node1721963440630 = RenameField.apply(frame=Dropothercolumn_node1721963433418, old_name="quantidade", new_name="qtd", transformation_ctx="Renamequantidadefield_node1721963440630")

# Script generated for node Count by acao
Countbyacao_node1721963468839 = sparkAggregate(glueContext, parentFrame = Renamequantidadefield_node1721963440630, groups = ["acao", "data_extracao"], aggs = [["qtd", "count"]], transformation_ctx = "Countbyacao_node1721963468839")

# Script generated for node Rename count(qtd)
Renamecountqtd_node1721963806377 = RenameField.apply(frame=Countbyacao_node1721963468839, old_name="`count(qtd)`", new_name="quantidade_por_acao", transformation_ctx="Renamecountqtd_node1721963806377")

# Script generated for node Rename acao field
Renameacaofield_node1721963863435 = RenameField.apply(frame=Renamecountqtd_node1721963806377, old_name="acao", new_name="nome_acao", transformation_ctx="Renameacaofield_node1721963863435")

# Script generated for node Add Current Timestamp
AddCurrentTimestamp_node1721964428610 = Renameacaofield_node1721963863435.gs_now(colName="date_glue_execuction")

# Script generated for node Data Preparation Recipe
# Adding configuration for certain Data Preparation recipe steps to run properly
spark.conf.set("spark.sql.legacy.timeParserPolicy", "LEGACY")
# Recipe name: DataPreparationRecipe_node1721964147886
DataPreparationRecipe_node1721964147886 = applyRecipe_node1721964147886(
    inputFrame=AddCurrentTimestamp_node1721964428610,
    glueContext=glueContext,
    transformation_ctx="DataPreparationRecipe_node1721964147886")

# Script generated for node Amazon S3
AmazonS3_node1721964620045 = glueContext.getSink(path="s3://gd-ibov-data/refined/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=["data_extracao", "nome_acao"], enableUpdateCatalog=True, transformation_ctx="AmazonS3_node1721964620045")
AmazonS3_node1721964620045.setCatalogInfo(catalogDatabase="gd-database-glue",catalogTableName="B3_ETL_table")
AmazonS3_node1721964620045.setFormat("glueparquet", compression="snappy")
AmazonS3_node1721964620045.writeFrame(DataPreparationRecipe_node1721964147886)
job.commit()
