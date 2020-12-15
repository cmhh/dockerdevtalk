rJava::.jinit(parameters = "-Xmx1g")

library(RJDBC)
library(dplyr)

# connect to SQL Server --------------------------------------------------------
ip <- "database"
p <- "jar/mssql-jdbc-8.4.1.jre8.jar"
drv <- RJDBC::JDBC("com.microsoft.sqlserver.jdbc.SQLServerDriver" , p)

conn <- DBI::dbConnect(
  drv,
  sprintf(
    "jdbc:sqlserver://%s:%d;databaseName=%s;username=%s;password=%s",
    ip, 1433, "adventureworks", "sa", "password-1234"
  )
)

# extract address table --------------------------------------------------------
address <- tbl(conn, dbplyr::in_schema("SalesLT", "Address")) %>% collect
View(address)

# tidy up ----------------------------------------------------------------------
DBI::dbDisconnect(conn)
rm(list=ls())
