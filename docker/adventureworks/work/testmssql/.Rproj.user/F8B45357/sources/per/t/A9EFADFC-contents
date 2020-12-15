rJava::.jinit(parameters = "-Xmx1g")

library(RJDBC)
if (!require(dbplyr)) renv::install("dbplyr")
library(dplyr)
library(data.table)

# connect to SQL Server --------------------------------------------------------
ip <- "database"
p <- "jar/mssql-jdbc-8.4.1.jre8.jar"
drv <- RJDBC::JDBC("com.microsoft.sqlserver.jdbc.SQLServerDriver" , p)

conn <- DBI::dbConnect(
  drv,
  sprintf(
    "jdbc:sqlserver://%s:%d;databaseName=%s;username=%s;password=%s",
    ip, 1433, "tempdb", "sa", "password-1234"
  )
)

# test the connection
cat(DBI::dbGetQuery(conn, "select @@version")[1,1])

# make test dataset ------------------------------------------------------------
n <- 100000
years <- 2015:2020
bins <- 10

dt <- data.table(
  year = rep(years, each = n),
  id = rep(1:n, length(years)),
  g1 = ceiling(runif(n * length(years)) * 2),
  g2 = ceiling(runif(n * length(years)) * 5),
  ind = do.call(
    cbind, 
    lapply(
      rep(n, length(years)), 
      function(x) as(runif(x) <= 0.1, "integer")
    )
  ),
  X = do.call(
    cbind, 
    lapply(
      rep(n, length(years)), 
      function(x) rnorm(x, 100))
    )
  )

setnames(
  dt, colnames(dt), gsub(".V", "", colnames(dt), fixed = TRUE)
)

# summary via data.table -------------------------------------------------------
(t0 <- system.time({
  res0 <- dt[, .(n = sum(ind1)), by = list(year, g1)]
}))

# write to SQL Server ----------------------------------------------------------
system.time({
  DBI::dbWriteTable(conn, "test", dt)
})

# summary via SQL Server -------------------------------------------------------
(t1 <- system.time({
  res1 <-  DBI::dbGetQuery(
    conn, 
    "
    SELECT
      year, g1, sum(ind1) as n
    FROM
      test
    GROUP BY
      year, g1
    ORDER BY 
      year, g1
    "
  )
}))

# summary via SQL Server with clustered index --------------------------------
query <- "create clustered index ic1 on test (year, id, g1, g2)"
DBI::dbSendQuery(conn, query)

(t2 <- system.time({
  res2 <- DBI::dbGetQuery(
    conn, 
    "
    SELECT
      year, g1, sum(ind1) as n
    FROM
      test
    GROUP BY
      year, g1
    ORDER BY 
      year, g1
    "
  )
}))

# summary via SQL Server with columnstore index --------------------------------
query <- "create clustered columnstore index ic1 on test with (drop_existing = ON)"
DBI::dbSendQuery(conn, query)

(t3 <- system.time({
  res3 <-  DBI::dbGetQuery(
    conn, 
    "
    SELECT
      year, g1, sum(ind1) as n
    FROM
      test
    GROUP BY
      year, g1
    ORDER BY 
      year, g1
    "
  )
}))

# tidy up ----------------------------------------------------------------------
DBI::dbSendQuery(conn, "drop table test")
DBI::dbDisconnect(conn)
rm(list=ls())
