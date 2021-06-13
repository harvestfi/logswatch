# Cloudwatch logs watcher and telegram alerter
Python script using boto3 and python-telegram-bot

## Quickstart
- clone git repo, copy config file from example and enter your values
```
git clone https://github.com/harvestfi/logswatch.git
cd cloudwatch
cp cloudwatch.logs.example cloudwatch.example
vim cloudwatch.example
```
- run periodicaly using e.g. cron (align interval with `querySeconds` config value)
```
*/5 * * * * root /usr/bin/python3 /your/directory/logswatch.py > /var/log/logswatch.log 2>&1
```

