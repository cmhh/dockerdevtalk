## Seasonal Adjustment as a Service

This container pulls a comiled version of a basic seasonal adjustment service from github, and runs it via internal port 9001.  To build the container from the `seasadj` folder:

```bash
docker build -t seasadj .
```

To start the container:

```bash
docker run -d --rm --name seasadj \
  -p 9001:9001 \
  seasadj
```

As an example of how to call the service:

```bash
curl \
  -X POST \
  -H "Content-Type: application/json" \
  -d @airpassengers.min.json \
  localhost:9001/seasadj/adjust \
  --compressed --output airpassengers.output.json
```

And as a simple R session:

```R
library(httr)

response <- POST(
  "https://cmhh.hopto.org/seasadj/adjust?save=ori,sa,trn", 
  body = upload_file("~/Downloads/airpassengers.json")
)

res <- content(response)$airpassengers

ori <- data.frame(
  date = unlist(res$series$ori$date),
  ori = unlist(res$series$ori$value)
)

sa <- data.frame(
  date = unlist(res$series$sa$date),
  sa = unlist(res$series$sa$value)
)

trn <- data.frame(
  date = unlist(res$series$trn$date),
  trn = unlist(res$series$trn$value)
)

plot(1:nrow(ori), ori$ori, type = "l", axes = FALSE, xlab = "month", ylab = "number", lty = 3, col = "grey")
axis(1, at = 1:nrow(ori), labels = ori$date)
axis(2)
box()
lines(1:nrow(sa), sa$sa, col = "grey", lwd = 2)
lines(1:nrow(trn), trn$trn, col = "black")
```

To measure performance:

```bash
siege -b -c 12 -t 30s --content-type "application/json" \
  'http://127.0.0.1:9001/seasadj/adjust?allDates=false&save=ori,sa,trn POST < airpassengers.min.json' 
```
```as.is
** SIEGE 4.0.7
** Preparing 12 concurrent users for battle.
The server is now under siege...
Lifting the server siege...
Transactions:                   6855 hits
Availability:                 100.00 %
Elapsed time:                  29.66 secs
Data transferred:              24.32 MB
Response time:                  0.04 secs
Transaction rate:             231.12 trans/sec
Throughput:                     0.82 MB/sec
Concurrency:                    9.52
Successful transactions:        6855
Failed transactions:               0
Longest transaction:            1.06
Shortest transaction:           0.02
```