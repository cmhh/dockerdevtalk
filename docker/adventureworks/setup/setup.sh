#! /bin/bash

# wait for the SQL Server to come up
sleep 40s

# run the setup script to create the DB
/opt/mssql-tools/bin/sqlcmd -S localhost -U SA -P ${MSSQL_SA_PASSWORD} -i setup-db.sql