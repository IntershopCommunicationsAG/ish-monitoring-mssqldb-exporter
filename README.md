# ISH-Monitoring-MsSQLDB Prometheus Exporter
MsSQL Exporter for Prometheus in python. Metrics are scraped by scheduler, and the interval is configurable via environment variable


## Integration
Run `docker-compose up`. When the image is not build yet, please run `docker-compose up --build`

After launching up, metrics show up in `http://localhost:8000/metrics`,
by using promql `{__name__=~".+",job="prometheusMssqlExporter"}`

To rebuild the image please run `docker-compose up --build`

The default SQL Server is local. If wanted to test with real data, it has to
either pull the data from production or pointing the SQL Server connection to the production one

## Setting up

##### Initialize a virtual environment

Windows:
```
$ python3 -m venv venv
$ venv\Scripts\activate.bat
```

Unix/MacOS:
```
$ python3 -m venv venv
$ source venv/bin/activate
```
Learn more in [the documentation](https://docs.python.org/3/library/venv.html#creating-virtual-environments).

Note: if you are using a python before 3.3, it doesn't come with venv. Install [virtualenv](https://docs.python-guide.org/dev/virtualenvs/#lower-level-virtualenv) with pip instead.

##### (If you're on a Mac) Make sure xcode tools are installed

```
$ xcode-select --install
```

##### Install the dependencies

```
$ source env/bin/activate
$ pip install -r requirements.txt
```

## Set Environment Variables

Please check `config.py`. `config.py` describes the environment, and
by setting `FLASK_CONFIG`  you can decide which environment to pick up, e.g.

`FLASK_CONFIG=config.TestingConfig`

or

`FLASK_CONFIG=config.DevelopmentConfig`

or

`FLASK_CONFIG=config.ProductionConfig`

## Running the app

```
$ source env/bin/activate
$ python3 manage.py runserver
```

## Formatting code

Before you submit changes, you may want to autoformat your code with `python manage.py format`.

## Development
Add new Metrics by extending `AbstractMetric`,
under `app/prom/metrics`, either `general`, which is related to system
or `business` that is related to business logic.

Check existing [examples](https://github.com/HungUnicorn/mssql-prom-exporter/tree/master/app/prom/metrics/general)
Check existing examples and the tests before adding them.

Before implementing a metric please go through the tips that ensure you
follow the [official guideline](https://prometheus.io/docs/practices/instrumentation/#things-to-watch-out-for)

In general the rules are:
#### Labels
- Use labels when required to aggregate the metrics, e.g. http status code should be one metrics with several labels(200, 400, 500)
- Do not use labels when cardinality is more than 100 and will increase more in the future

#### Existing metrics
```
# HELP mssql_batch_requests Number of Transact-SQL command batches received per second.\n            This statistic is affected by all constraints (such as I/O, number of users, cachesize, \n            complexity of requests, and so on). High batch requests mean good throughput
# TYPE mssql_batch_requests gauge
mssql_batch_requests 5.2578822e+07
# HELP mssql_connections Number of connections
# TYPE mssql_connections gauge
mssql_connections{database="ISTE_TP07137_TS57367",state="current"} 10.0
mssql_connections{database="ISTE_TP07137_TS57389",state="current"} 10.0
mssql_connections{database="ISTE_TP07137_TS57393",state="current"} 10.0
mssql_connections{database="ISTE_TP07137_TS57419",state="current"} 2.0
mssql_connections{database="ISTE_TP07137_TS57421",state="current"} 10.0
mssql_connections{database="ISTE_TP07137_TS57437",state="current"} 10.0
mssql_connections{database="ISTE_TP07137_TS57443",state="current"} 10.0
mssql_connections{database="ISTE_TP07137_TS57469",state="current"} 10.0
mssql_connections{database="ISTE_TP07137_TS57485",state="current"} 10.0
mssql_connections{database="ISTE_TP07137_TS57561",state="current"} 10.0
mssql_connections{database="ISTE_TP07137_TS57571",state="current"} 10.0
mssql_connections{database="ISTE_TP07137_TS57615",state="current"} 10.0
mssql_connections{database="ISTE_TP07137_TS57695",state="current"} 10.0
mssql_connections{database="ISTE_TP07137_TS58013",state="current"} 10.0
mssql_connections{database="ISTE_TP07137_TS58015",state="current"} 11.0
mssql_connections{database="ISTE_TP07137_TS58019",state="current"} 10.0
mssql_connections{database="master",state="current"} 52.0
# HELP mssql_deadlocks Number of lock requests per second that resulted in a deadlock since last restart
# TYPE mssql_deadlocks gauge
mssql_deadlocks 0.0
# HELP mssql_io_stall Wait time (ms) of stall since last restart
# TYPE mssql_io_stall gauge
mssql_io_stall{database="master",type="stall_read"} 77.0
mssql_io_stall{database="master",type="stall_write"} 1572.0
mssql_io_stall{database="master",type="stall_queued_read"} 0.0
mssql_io_stall{database="master",type="stall_queued_write"} 0.0
mssql_io_stall{database="tempdb",type="stall_read"} 51890.0
mssql_io_stall{database="tempdb",type="stall_write"} 37527.0
mssql_io_stall{database="tempdb",type="stall_queued_read"} 0.0
mssql_io_stall{database="tempdb",type="stall_queued_write"} 0.0
mssql_io_stall{database="model",type="stall_read"} 155.0
mssql_io_stall{database="model",type="stall_write"} 5.0
mssql_io_stall{database="model",type="stall_queued_read"} 0.0
mssql_io_stall{database="model",type="stall_queued_write"} 0.0
mssql_io_stall{database="msdb",type="stall_read"} 366.0
mssql_io_stall{database="msdb",type="stall_write"} 344.0
mssql_io_stall{database="msdb",type="stall_queued_read"} 0.0
mssql_io_stall{database="msdb",type="stall_queued_write"} 0.0
mssql_io_stall{database="ISTE_TP07137_TS57615",type="stall_read"} 164.0
mssql_io_stall{database="ISTE_TP07137_TS57615",type="stall_write"} 115.0
mssql_io_stall{database="ISTE_TP07137_TS57615",type="stall_queued_read"} 0.0
mssql_io_stall{database="ISTE_TP07137_TS57615",type="stall_queued_write"} 0.0
mssql_io_stall{database="ISTE_TP07137_TS57393",type="stall_read"} 148.0
mssql_io_stall{database="ISTE_TP07137_TS57393",type="stall_write"} 1718.0
mssql_io_stall{database="ISTE_TP07137_TS57393",type="stall_queued_read"} 0.0
mssql_io_stall{database="ISTE_TP07137_TS57393",type="stall_queued_write"} 0.0
mssql_io_stall{database="ISTE_TP07137_TS57367",type="stall_read"} 873.0
mssql_io_stall{database="ISTE_TP07137_TS57367",type="stall_write"} 1481.0
mssql_io_stall{database="ISTE_TP07137_TS57367",type="stall_queued_read"} 0.0
mssql_io_stall{database="ISTE_TP07137_TS57367",type="stall_queued_write"} 0.0
mssql_io_stall{database="ISTE_ICM_DEV",type="stall_read"} 635.0
mssql_io_stall{database="ISTE_ICM_DEV",type="stall_write"} 422.0
mssql_io_stall{database="ISTE_ICM_DEV",type="stall_queued_read"} 0.0
mssql_io_stall{database="ISTE_ICM_DEV",type="stall_queued_write"} 0.0
mssql_io_stall{database="ISTE_TP07141",type="stall_read"} 54.0
mssql_io_stall{database="ISTE_TP07141",type="stall_write"} 401.0
mssql_io_stall{database="ISTE_TP07141",type="stall_queued_read"} 0.0
mssql_io_stall{database="ISTE_TP07141",type="stall_queued_write"} 0.0
mssql_io_stall{database="ISTE_TP07137",type="stall_read"} 1402.0
mssql_io_stall{database="ISTE_TP07137",type="stall_write"} 31100.0
mssql_io_stall{database="ISTE_TP07137",type="stall_queued_read"} 0.0
mssql_io_stall{database="ISTE_TP07137",type="stall_queued_write"} 0.0
mssql_io_stall{database="ISTE_TP07137_TS57695",type="stall_read"} 177.0
mssql_io_stall{database="ISTE_TP07137_TS57695",type="stall_write"} 62.0
mssql_io_stall{database="ISTE_TP07137_TS57695",type="stall_queued_read"} 0.0
mssql_io_stall{database="ISTE_TP07137_TS57695",type="stall_queued_write"} 0.0
mssql_io_stall{database="ISTE_TP07115_TS48733",type="stall_read"} 7961.0
mssql_io_stall{database="ISTE_TP07115_TS48733",type="stall_write"} 2068.0
mssql_io_stall{database="ISTE_TP07115_TS48733",type="stall_queued_read"} 0.0
mssql_io_stall{database="ISTE_TP07115_TS48733",type="stall_queued_write"} 0.0
mssql_io_stall{database="ISTE_TP07137_TS58013",type="stall_read"} 3119.0
mssql_io_stall{database="ISTE_TP07137_TS58013",type="stall_write"} 2222.0
mssql_io_stall{database="ISTE_TP07137_TS58013",type="stall_queued_read"} 0.0
mssql_io_stall{database="ISTE_TP07137_TS58013",type="stall_queued_write"} 0.0
mssql_io_stall{database="ISTE_TP07137_TS57887",type="stall_read"} 66.0
mssql_io_stall{database="ISTE_TP07137_TS57887",type="stall_write"} 13.0
mssql_io_stall{database="ISTE_TP07137_TS57887",type="stall_queued_read"} 0.0
mssql_io_stall{database="ISTE_TP07137_TS57887",type="stall_queued_write"} 0.0
mssql_io_stall{database="ISTE_TP07115_TS48781",type="stall_read"} 3157.0
mssql_io_stall{database="ISTE_TP07115_TS48781",type="stall_write"} 655.0
mssql_io_stall{database="ISTE_TP07115_TS48781",type="stall_queued_read"} 0.0
mssql_io_stall{database="ISTE_TP07115_TS48781",type="stall_queued_write"} 0.0
mssql_io_stall{database="ISTE_TP07140",type="stall_read"} 1774.0
mssql_io_stall{database="ISTE_TP07140",type="stall_write"} 28113.0
mssql_io_stall{database="ISTE_TP07140",type="stall_queued_read"} 0.0
mssql_io_stall{database="ISTE_TP07140",type="stall_queued_write"} 0.0
mssql_io_stall{database="ISTE_TP07137_TS57437",type="stall_read"} 1071.0
mssql_io_stall{database="ISTE_TP07137_TS57437",type="stall_write"} 1640.0
mssql_io_stall{database="ISTE_TP07137_TS57437",type="stall_queued_read"} 0.0
mssql_io_stall{database="ISTE_TP07137_TS57437",type="stall_queued_write"} 0.0
mssql_io_stall{database="ISTE_TP07137_TS57419",type="stall_read"} 72.0
mssql_io_stall{database="ISTE_TP07137_TS57419",type="stall_write"} 13.0
mssql_io_stall{database="ISTE_TP07137_TS57419",type="stall_queued_read"} 0.0
mssql_io_stall{database="ISTE_TP07137_TS57419",type="stall_queued_write"} 0.0
mssql_io_stall{database="ISTE_TP07137_TS58019",type="stall_read"} 1120.0
mssql_io_stall{database="ISTE_TP07137_TS58019",type="stall_write"} 1413.0
mssql_io_stall{database="ISTE_TP07137_TS58019",type="stall_queued_read"} 0.0
mssql_io_stall{database="ISTE_TP07137_TS58019",type="stall_queued_write"} 0.0
mssql_io_stall{database="ISTE_TP07137_TS57401",type="stall_read"} 66.0
mssql_io_stall{database="ISTE_TP07137_TS57401",type="stall_write"} 14.0
mssql_io_stall{database="ISTE_TP07137_TS57401",type="stall_queued_read"} 0.0
mssql_io_stall{database="ISTE_TP07137_TS57401",type="stall_queued_write"} 0.0
mssql_io_stall{database="ISTE_TP07137_TS58023",type="stall_read"} 67.0
mssql_io_stall{database="ISTE_TP07137_TS58023",type="stall_write"} 17.0
mssql_io_stall{database="ISTE_TP07137_TS58023",type="stall_queued_read"} 0.0
mssql_io_stall{database="ISTE_TP07137_TS58023",type="stall_queued_write"} 0.0
mssql_io_stall{database="ISTE_TP07115_TS49311",type="stall_read"} 3610.0
mssql_io_stall{database="ISTE_TP07115_TS49311",type="stall_write"} 912.0
mssql_io_stall{database="ISTE_TP07115_TS49311",type="stall_queued_read"} 0.0
mssql_io_stall{database="ISTE_TP07115_TS49311",type="stall_queued_write"} 0.0
mssql_io_stall{database="ISTE_TP07137_TS57561",type="stall_read"} 780.0
mssql_io_stall{database="ISTE_TP07137_TS57561",type="stall_write"} 1180.0
mssql_io_stall{database="ISTE_TP07137_TS57561",type="stall_queued_read"} 0.0
mssql_io_stall{database="ISTE_TP07137_TS57561",type="stall_queued_write"} 0.0
mssql_io_stall{database="ISTE_TP07115_TS48857",type="stall_read"} 6037.0
mssql_io_stall{database="ISTE_TP07115_TS48857",type="stall_write"} 1494.0
mssql_io_stall{database="ISTE_TP07115_TS48857",type="stall_queued_read"} 0.0
mssql_io_stall{database="ISTE_TP07115_TS48857",type="stall_queued_write"} 0.0
mssql_io_stall{database="ISTE_TP07137_TS58035",type="stall_read"} 67.0
mssql_io_stall{database="ISTE_TP07137_TS58035",type="stall_write"} 14.0
mssql_io_stall{database="ISTE_TP07137_TS58035",type="stall_queued_read"} 0.0
mssql_io_stall{database="ISTE_TP07137_TS58035",type="stall_queued_write"} 0.0
mssql_io_stall{database="ISTE_TP07137_TS58071",type="stall_read"} 66.0
mssql_io_stall{database="ISTE_TP07137_TS58071",type="stall_write"} 17.0
mssql_io_stall{database="ISTE_TP07137_TS58071",type="stall_queued_read"} 0.0
mssql_io_stall{database="ISTE_TP07137_TS58071",type="stall_queued_write"} 0.0
mssql_io_stall{database="ISTE_TP07137_TS58031",type="stall_read"} 67.0
mssql_io_stall{database="ISTE_TP07137_TS58031",type="stall_write"} 15.0
mssql_io_stall{database="ISTE_TP07137_TS58031",type="stall_queued_read"} 0.0
mssql_io_stall{database="ISTE_TP07137_TS58031",type="stall_queued_write"} 0.0
mssql_io_stall{database="ISTE_TP07137_TS58009",type="stall_read"} 66.0
mssql_io_stall{database="ISTE_TP07137_TS58009",type="stall_write"} 14.0
mssql_io_stall{database="ISTE_TP07137_TS58009",type="stall_queued_read"} 0.0
mssql_io_stall{database="ISTE_TP07137_TS58009",type="stall_queued_write"} 0.0
mssql_io_stall{database="ISTE_TP07137_TS57389",type="stall_read"} 1364.0
mssql_io_stall{database="ISTE_TP07137_TS57389",type="stall_write"} 1047.0
mssql_io_stall{database="ISTE_TP07137_TS57389",type="stall_queued_read"} 0.0
mssql_io_stall{database="ISTE_TP07137_TS57389",type="stall_queued_write"} 0.0
mssql_io_stall{database="ISTE_TP07137_TS57485",type="stall_read"} 179.0
mssql_io_stall{database="ISTE_TP07137_TS57485",type="stall_write"} 371.0
mssql_io_stall{database="ISTE_TP07137_TS57485",type="stall_queued_read"} 0.0
mssql_io_stall{database="ISTE_TP07137_TS57485",type="stall_queued_write"} 0.0
mssql_io_stall{database="ISTE_TP07115_TS48765",type="stall_read"} 6387.0
mssql_io_stall{database="ISTE_TP07115_TS48765",type="stall_write"} 2241.0
mssql_io_stall{database="ISTE_TP07115_TS48765",type="stall_queued_read"} 0.0
mssql_io_stall{database="ISTE_TP07115_TS48765",type="stall_queued_write"} 0.0
mssql_io_stall{database="ISTE_TP07137_TS57443",type="stall_read"} 558.0
mssql_io_stall{database="ISTE_TP07137_TS57443",type="stall_write"} 751.0
mssql_io_stall{database="ISTE_TP07137_TS57443",type="stall_queued_read"} 0.0
mssql_io_stall{database="ISTE_TP07137_TS57443",type="stall_queued_write"} 0.0
mssql_io_stall{database="ISTE_TP07137_TS58015",type="stall_read"} 1281.0
mssql_io_stall{database="ISTE_TP07137_TS58015",type="stall_write"} 3180.0
mssql_io_stall{database="ISTE_TP07137_TS58015",type="stall_queued_read"} 0.0
mssql_io_stall{database="ISTE_TP07137_TS58015",type="stall_queued_write"} 0.0
mssql_io_stall{database="ISTE_TP07137_TS58033",type="stall_read"} 68.0
mssql_io_stall{database="ISTE_TP07137_TS58033",type="stall_write"} 16.0
mssql_io_stall{database="ISTE_TP07137_TS58033",type="stall_queued_read"} 0.0
mssql_io_stall{database="ISTE_TP07137_TS58033",type="stall_queued_write"} 0.0
mssql_io_stall{database="ISTE_TP07137_TS57571",type="stall_read"} 2116.0
mssql_io_stall{database="ISTE_TP07137_TS57571",type="stall_write"} 183.0
mssql_io_stall{database="ISTE_TP07137_TS57571",type="stall_queued_read"} 0.0
mssql_io_stall{database="ISTE_TP07137_TS57571",type="stall_queued_write"} 0.0
mssql_io_stall{database="ISTE_TP07137_TS58029",type="stall_read"} 70.0
mssql_io_stall{database="ISTE_TP07137_TS58029",type="stall_write"} 15.0
mssql_io_stall{database="ISTE_TP07137_TS58029",type="stall_queued_read"} 0.0
mssql_io_stall{database="ISTE_TP07137_TS58029",type="stall_queued_write"} 0.0
mssql_io_stall{database="ISTE_TP07137_TS57469",type="stall_read"} 461.0
mssql_io_stall{database="ISTE_TP07137_TS57469",type="stall_write"} 320.0
mssql_io_stall{database="ISTE_TP07137_TS57469",type="stall_queued_read"} 0.0
mssql_io_stall{database="ISTE_TP07137_TS57469",type="stall_queued_write"} 0.0
mssql_io_stall{database="ISTE_TP07137_TS57421",type="stall_read"} 1060.0
mssql_io_stall{database="ISTE_TP07137_TS57421",type="stall_write"} 636.0
mssql_io_stall{database="ISTE_TP07137_TS57421",type="stall_queued_read"} 0.0
mssql_io_stall{database="ISTE_TP07137_TS57421",type="stall_queued_write"} 0.0
# HELP mssql_io_stall_total Wait time (ms) of stall since last restart
# TYPE mssql_io_stall_total gauge
mssql_io_stall_total{database="master"} 1587.0
mssql_io_stall_total{database="tempdb"} 89417.0
mssql_io_stall_total{database="model"} 155.0
mssql_io_stall_total{database="msdb"} 710.0
mssql_io_stall_total{database="ISTE_TP07137_TS57615"} 164.0
mssql_io_stall_total{database="ISTE_TP07137_TS57393"} 1731.0
mssql_io_stall_total{database="ISTE_TP07137_TS57367"} 1492.0
mssql_io_stall_total{database="ISTE_ICM_DEV"} 1057.0
mssql_io_stall_total{database="ISTE_TP07141"} 413.0
mssql_io_stall_total{database="ISTE_TP07137"} 32502.0
mssql_io_stall_total{database="ISTE_TP07137_TS57695"} 177.0
mssql_io_stall_total{database="ISTE_TP07115_TS48733"} 10029.0
mssql_io_stall_total{database="ISTE_TP07137_TS58013"} 3236.0
mssql_io_stall_total{database="ISTE_TP07137_TS57887"} 71.0
mssql_io_stall_total{database="ISTE_TP07115_TS48781"} 3812.0
mssql_io_stall_total{database="ISTE_TP07140"} 29706.0
mssql_io_stall_total{database="ISTE_TP07137_TS57437"} 1653.0
mssql_io_stall_total{database="ISTE_TP07137_TS57419"} 76.0
mssql_io_stall_total{database="ISTE_TP07137_TS58019"} 1424.0
mssql_io_stall_total{database="ISTE_TP07137_TS57401"} 70.0
mssql_io_stall_total{database="ISTE_TP07137_TS58023"} 73.0
mssql_io_stall_total{database="ISTE_TP07115_TS49311"} 4441.0
mssql_io_stall_total{database="ISTE_TP07137_TS57561"} 1191.0
mssql_io_stall_total{database="ISTE_TP07115_TS48857"} 6983.0
mssql_io_stall_total{database="ISTE_TP07137_TS58035"} 71.0
mssql_io_stall_total{database="ISTE_TP07137_TS58071"} 70.0
mssql_io_stall_total{database="ISTE_TP07137_TS58031"} 71.0
mssql_io_stall_total{database="ISTE_TP07137_TS58009"} 71.0
mssql_io_stall_total{database="ISTE_TP07137_TS57389"} 1577.0
mssql_io_stall_total{database="ISTE_TP07137_TS57485"} 383.0
mssql_io_stall_total{database="ISTE_TP07115_TS48765"} 8628.0
mssql_io_stall_total{database="ISTE_TP07137_TS57443"} 763.0
mssql_io_stall_total{database="ISTE_TP07137_TS58015"} 3193.0
mssql_io_stall_total{database="ISTE_TP07137_TS58033"} 73.0
mssql_io_stall_total{database="ISTE_TP07137_TS57571"} 2117.0
mssql_io_stall_total{database="ISTE_TP07137_TS58029"} 74.0
mssql_io_stall_total{database="ISTE_TP07137_TS57469"} 464.0
mssql_io_stall_total{database="ISTE_TP07137_TS57421"} 1068.0
# HELP mssql_kill_connection_errors Number of kill connection errors/sec since last restart
# TYPE mssql_kill_connection_errors gauge
mssql_kill_connection_errors 0.0
# HELP mssql_log_growths Total number of times the transaction log for the database has been expanded since last restart.
# TYPE mssql_log_growths gauge
mssql_log_growths{database="ISTE_TP07171"} 0.0
mssql_log_growths{database="ISTE_TP07170_TS79174"} 0.0
mssql_log_growths{database="ISTE_1_TP03844"} 0.0
mssql_log_growths{database="ISTE_TP07170"} 0.0
mssql_log_growths{database="tempdb"} 0.0
mssql_log_growths{database="model"} 0.0
mssql_log_growths{database="ISTE_ICM_DEV"} 0.0
mssql_log_growths{database="msdb"} 0.0
mssql_log_growths{database="mssqlsystemresource"} 0.0
mssql_log_growths{database="master"} 0.0
# HELP mssql_log_total_size_in_bytes Total log size in bytes
# TYPE mssql_log_total_size_in_bytes gauge
mssql_log_total_size_in_bytes 2.08896e+06
# HELP mssql_log_used_space_in_bytes Used log space in bytes
# TYPE mssql_log_used_space_in_bytes gauge
mssql_log_used_space_in_bytes 966656.0
# HELP mssql_log_used_space_in_percentage Used log space in percentage
# TYPE mssql_log_used_space_in_percentage gauge
mssql_log_used_space_in_percentage 46.27450942993164
# HELP mssql_log_space_in_bytes_since_last_backup Log space in bytes since last backup
# TYPE mssql_log_space_in_bytes_since_last_backup gauge
mssql_log_space_in_bytes_since_last_backup 548864.0
# HELP mssql_page_fault_count Number of page faults since last restart
# TYPE mssql_page_fault_count gauge
mssql_page_fault_count 0.0
# HELP mssql_memory_utilization_percentage Percentage of memory utilization
# TYPE mssql_memory_utilization_percentage gauge
mssql_memory_utilization_percentage 29.0
# HELP mssql_total_physical_memory_kb Total physical memory in KB
# TYPE mssql_total_physical_memory_kb gauge
mssql_total_physical_memory_kb 7.9095808e+07
# HELP mssql_available_physical_memory_kb Available physical memory in KB
# TYPE mssql_available_physical_memory_kb gauge
mssql_available_physical_memory_kb 6.0057148e+07
# HELP mssql_total_page_file_kb Total page file in KB
# TYPE mssql_total_page_file_kb gauge
mssql_total_page_file_kb 7.9095808e+07
# HELP mssql_available_page_file_kb Available page file in KB
# TYPE mssql_available_page_file_kb gauge
mssql_available_page_file_kb 6.0057148e+07
# HELP mssql_page_life_expectancy Indicates the minimum number of seconds a page will stay in the buffer pool on this node without references.\n            The traditional advice from Microsoft used to be that the PLE should remain above 300 seconds
# TYPE mssql_page_life_expectancy gauge
mssql_page_life_expectancy 14820.0
# HELP mssql_uptime Gauge metric with uptime in days of the Instance.
# TYPE mssql_uptime gauge
mssql_uptime 1.0
# HELP mssql_user_errors Number of user errors/sec since last restart
# TYPE mssql_user_errors gauge
mssql_user_errors 179996.0
# HELP mssql_up UP status
# TYPE mssql_up gauge
mssql_up 1.0
```

### Build and Push

```
 docker build -t intershopde/ish-monitoring-mssqldb-exporter:latest .
 docker push intershopde/ish-monitoring-mssqldb-exporter:latest
```