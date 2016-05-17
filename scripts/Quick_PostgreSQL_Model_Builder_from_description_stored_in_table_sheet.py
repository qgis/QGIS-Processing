##Database=group
##Quick_PostgreSQL_Model_Builder_from_description_stored_in_table_sheet=name
##Layer_containing_tables_description=table
##Field_with_table_name=field Layer_containing_tables_description
##Field_with_table_schema=field Layer_containing_tables_description
##Field_with_table_comment=field Layer_containing_tables_description
##Field_with_table_primary_key=field Layer_containing_tables_description
##Layer_containing_columns_description=table
##Field_with_column_table_name=field Layer_containing_columns_description
##Field_with_column_name=field Layer_containing_columns_description
##Field_with_column_type=field Layer_containing_columns_description
##Field_with_column_not_null_status=field Layer_containing_columns_description
##Field_with_column_constraint=field Layer_containing_columns_description
##Field_with_column_comment=field Layer_containing_columns_description
##Field_with_column_index_status=field Layer_containing_columns_description
##Create_needed_schemas=boolean False
##sql=output string
##Output_SQL_file=output file

from qgis.core import QgsMapLayer, QgsVectorLayer, QgsFeature, QgsFeatureRequest
from PyQt4.QtCore import QVariant
import os, re

# Utility class
class qgisPostgresqlQuickModeler():

    def createTable(self, tname, tschema='', tcomment=''):
        sql=''

        sql+= '\n\n-- Table %s \n' % tname

        if tschema and Create_needed_schemas:
            sql+= 'CREATE SCHEMA IF NOT EXISTS "%s" ;\n' % tschema
        if tschema:    
            sql+= 'SET search_path TO %s,public ;\n' % tschema

        sql+= 'CREATE TABLE IF NOT EXISTS "%s" () ;\n\n' % (
            tname
        )

        if tcomment:
            sql+= 'COMMENT ON TABLE "%s" IS \'%s\' ;\n' % (
                tname,
                tcomment.replace("'", "''")
            )

        return sql


    def addColumn(self, tname, cname, ctype, cconstraint='', cnotnull='', ccomment='', cindex=''):
        sql = ''
        notnull = 'NOT NULL' if cnotnull == '1' else ''
        index = True if cindex == 1 else False

        # Add column
        sql+= '\nALTER TABLE "%s" ADD COLUMN "%s" %s %s ;\n' % (
            tname,
            cname,
            ctype,
            notnull
        )

        # Add constraint
        if cconstraint:
            sql+= 'ALTER TABLE "%s" ADD CONSTRAINT %s; \n' % (
                tname,
                cconstraint
            )

        # Add comment
        if ccomment:
            sql+= 'COMMENT ON COLUMN "%s".%s IS \'%s\' ; \n' % (
                tname,
                cname,
                ccomment.replace("'", "''")
            )

        # Create index
        if cindex:
            sql+= 'CREATE INDEX ON "%s" (%s) ;\n' % (
                tname,
                cname
            )

        return sql

    def addPkey(self, tname, tpkey=''):
        sql = ''
        if tpkey:
            sql+= 'ALTER TABLE "%s" ADD PRIMARY KEY (%s);\n' % (
                tname,
                tpkey
            )
        return sql

# Get layers objects
tlayer = processing.getObject(Layer_containing_tables_description)
clayer = processing.getObject(Layer_containing_columns_description)

# rename inputs
t_name = Field_with_table_name
t_schema = Field_with_table_schema
t_comment = Field_with_table_comment
t_pkey = Field_with_table_primary_key

c_table_name = Field_with_column_table_name
c_name = Field_with_column_name
c_type = Field_with_column_type
c_not_null = Field_with_column_not_null_status
c_constraint = Field_with_column_constraint
c_comment = Field_with_column_comment
c_index = Field_with_column_index_status

# Get tools
modeler = qgisPostgresqlQuickModeler()

# Build SQL
sql = ''

if tlayer and clayer:

    # Loop through features describing tables
    for tfeat in tlayer.getFeatures():
        sql+= modeler.createTable(
            tfeat[t_name],
            tfeat[t_schema],
            tfeat[t_comment]
        )

        # Get features from column layer filtered by current table
        request = QgsFeatureRequest().setFilterExpression(
            u' "%s" = \'%s\' ' % (
                c_table_name,
                tfeat[t_name]
            )
        )

        # Loop through features describing columns
        for cfeat in clayer.getFeatures(request):
            sql+= modeler.addColumn(
                cfeat[c_table_name],
                cfeat[c_name],
                cfeat[c_type],
                cfeat[c_constraint],
                cfeat[c_not_null],
                cfeat[c_comment],
                cfeat[c_index]
            )
            
        # Add primary key(s)
        sql+= modeler.addPkey(
            tfeat[t_name],
            tfeat[t_pkey]
        )            

sql = 'BEGIN;\n' + sql + '\nCOMMIT;'
try:
    with open(Output_SQL_file, "w") as f:
        f.write(sql.encode('UTF8'))
except:
    raise GeoAlgorithmExecutionException(u'Error while writing SQL file into !' % Output_SQL_file)

progress.setInfo(u'SQL content has been written into %s' % Output_SQL_file)
