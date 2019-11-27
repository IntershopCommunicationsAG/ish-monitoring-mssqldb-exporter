# ISH-Monitoring-MsSQLDB Prometheus Exporter
MSSQL Exporter for Prometheus in python. Metrics are scraped by scheduler, and the interval is configurable via environment variable


## Integration
Run `docker-compose up`. When the image is not build yet, please run `docker-compose up --build`

After launching up, metrics show up in `http://localhost:8000/metrics`,
by using promql `{__name__=~".+",app="prometheus-mssql-exporter"}`

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
# HELP mssql_batch_requests Number of Transact-SQL command batches received per second.\n            This statistic is affected by all constraints (such as I/O, number of users, cachesize,\n            complexity of requests, and so on). High batch requests mean good throughput
# TYPE mssql_batch_requests gauge
mssql_batch_requests 16083.0
# HELP mssql_buffer_manager Several buffer manager counters of SQL Server.
# TYPE mssql_buffer_manager gauge
mssql_buffer_manager{counter_name="buffer_cache_hit_ratio"} 6.0
mssql_buffer_manager{counter_name="lazy_writessec"} 0.0
mssql_buffer_manager{counter_name="page_readssec"} 4310.0
mssql_buffer_manager{counter_name="page_writessec"} 92.0
mssql_buffer_manager{counter_name="page_life_expectancy"} 15704.0
# HELP mssql_deadlocks Number of lock requests per second that resulted in a deadlock since last restart
# TYPE mssql_deadlocks gauge
mssql_deadlocks 0.0
# HELP mssql_io_stall Wait time (ms) of stall since last restart
# TYPE mssql_io_stall gauge
mssql_io_stall{database="master",type="stall_read"} 92.0
mssql_io_stall{database="master",type="stall_write"} 336.0
mssql_io_stall{database="master",type="stall_queued_read"} 0.0
mssql_io_stall{database="master",type="stall_queued_write"} 0.0
mssql_io_stall{database="tempdb",type="stall_read"} 57.0
mssql_io_stall{database="tempdb",type="stall_write"} 6.0
mssql_io_stall{database="tempdb",type="stall_queued_read"} 0.0
mssql_io_stall{database="tempdb",type="stall_queued_write"} 0.0
mssql_io_stall{database="model",type="stall_read"} 61.0
mssql_io_stall{database="model",type="stall_write"} 11.0
mssql_io_stall{database="model",type="stall_queued_read"} 0.0
mssql_io_stall{database="model",type="stall_queued_write"} 0.0
mssql_io_stall{database="msdb",type="stall_read"} 137.0
mssql_io_stall{database="msdb",type="stall_write"} 1.0
mssql_io_stall{database="msdb",type="stall_queued_read"} 0.0
mssql_io_stall{database="msdb",type="stall_queued_write"} 0.0
# HELP mssql_io_stall_total Wait time (ms) of stall since last restart
# TYPE mssql_io_stall_total gauge
mssql_io_stall_total{database="master"} 371.0
mssql_io_stall_total{database="tempdb"} 58.0
mssql_io_stall_total{database="model"} 61.0
mssql_io_stall_total{database="msdb"} 137.0
# HELP mssql_kill_connection_errors Number of kill connection errors/sec since last restart
# TYPE mssql_kill_connection_errors gauge
mssql_kill_connection_errors 0.0
# HELP mssql_log_growths Total number of times the transaction log for the database has been expanded since last restart.
# TYPE mssql_log_growths gauge
mssql_log_growths{database="tempdb"} 0.0
mssql_log_growths{database="model"} 0.0
mssql_log_growths{database="msdb"} 0.0
mssql_log_growths{database="mssqlsystemresource"} 0.0
mssql_log_growths{database="master"} 0.0
# HELP mssql_log_total_size_in_bytes Total log size in bytes
# TYPE mssql_log_total_size_in_bytes gauge
mssql_log_total_size_in_bytes 2.08896e+06
# HELP mssql_log_used_space_in_bytes Used log space in bytes
# TYPE mssql_log_used_space_in_bytes gauge
mssql_log_used_space_in_bytes 1.41312e+06
# HELP mssql_log_used_space_in_percentage Used log space in percentage
# TYPE mssql_log_used_space_in_percentage gauge
mssql_log_used_space_in_percentage 67.64705657958984
# HELP mssql_log_space_in_bytes_since_last_backup Log space in bytes since last backup
# TYPE mssql_log_space_in_bytes_since_last_backup gauge
mssql_log_space_in_bytes_since_last_backup 1.056768e+06
# HELP mssql_page_fault_count Number of page faults since last restart
# TYPE mssql_page_fault_count gauge
mssql_page_fault_count 0.0
# HELP mssql_memory_utilization_percentage Percentage of memory utilization
# TYPE mssql_memory_utilization_percentage gauge
mssql_memory_utilization_percentage 100.0
# HELP mssql_virtual_address_space_committed_kb SQL Server resident memory size (AKA working set).
# TYPE mssql_virtual_address_space_committed_kb gauge
mssql_virtual_address_space_committed_kb 4.194304e+06
# HELP mssql_physical_memory_in_use_kb SQL Server committed virtual memory size.
# TYPE mssql_physical_memory_in_use_kb gauge
mssql_physical_memory_in_use_kb 210584.0
# HELP mssql_total_physical_memory_kb Total physical memory in KB
# TYPE mssql_total_physical_memory_kb gauge
mssql_total_physical_memory_kb 1.622016e+06
# HELP mssql_available_physical_memory_kb Available physical memory in KB
# TYPE mssql_available_physical_memory_kb gauge
mssql_available_physical_memory_kb 1.622016e+06
# HELP mssql_total_page_file_kb Total page file in KB
# TYPE mssql_total_page_file_kb gauge
mssql_total_page_file_kb 1.622016e+06
# HELP mssql_available_page_file_kb Available page file in KB
# TYPE mssql_available_page_file_kb gauge
mssql_available_page_file_kb 1.622016e+06
# HELP mssql_performance_counters Several performance counters of SQL Server.
# TYPE mssql_performance_counters gauge
mssql_performance_counters{counter_name="user_connections"} 4.0
mssql_performance_counters{counter_name="connection_memory_kb"} 1376.0
mssql_performance_counters{counter_name="lock_memory_kb"} 672.0
mssql_performance_counters{counter_name="lock_blocks_allocated"} 0.0
mssql_performance_counters{counter_name="lock_blocks"} 0.0
mssql_performance_counters{counter_name="lock_owner_blocks"} 0.0
mssql_performance_counters{counter_name="target_server_memory_kb"} 1.622016e+06
mssql_performance_counters{counter_name="total_server_memory_kb"} 210584.0
# HELP mssql_system_processes Number of system processes
# TYPE mssql_system_processes gauge
mssql_system_processes{database="master"} 54.0
# HELP mssql_up MsSQL exporter UP status
# TYPE mssql_up gauge
mssql_up 1.0
# HELP mssql_uptime Gauge metric with uptime in days of the Instance.
# TYPE mssql_uptime gauge
mssql_uptime 0.0
# HELP mssql_user_errors Number of user errors/sec since last restart
# TYPE mssql_user_errors gauge
mssql_user_errors 2527.0
```

### Build and Push

```
 docker build -t ishcloudopsicp.azurecr.io/intershop/ish-monitoring-mssqldb-exporter:latest .
 docker push ishcloudopsicp.azurecr.io/intershop/ish-monitoring-mssqldb-exporter:latest
```