import boto3
from datetime import datetime, timedelta
import time
import json
from telegram import ParseMode
from telegram.ext import Updater
import logging
import configparser
import re
import os

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


config = configparser.ConfigParser()
config.read(os.path.dirname(__file__)+'/logswatch.conf')

# init telegram bot
updater = Updater(token=config['telegram']['token'], use_context=True)

# init cloudwatch logs client
client = boto3.client('logs')

queryStartTime = datetime.now()
start_query_response = client.start_query(
    logGroupName=config['cloudwatch']['logGroup'],
    startTime=int((datetime.today() - timedelta(seconds=int(config['cloudwatch']['querySeconds']))).timestamp()),
    endTime=int(datetime.now().timestamp()),
    queryString=config['cloudwatch']['query'],
)

query_id = start_query_response['queryId']
response = None
while response == None or response['status'] == 'Running':
    time.sleep(1)
    response = client.get_query_results(
        queryId=query_id
    )
logging.info(f'Received response after {(datetime.now()-queryStartTime).total_seconds()}s',)
for result in reversed(response['results']):
    jsonResult = json.loads(result[0]['value'])
    log = jsonResult['log_processed']['log']
    message = "<b>"+jsonResult['kubernetes']['namespace_name']
    message += " / "+jsonResult['kubernetes']['pod_name']
    message += "</b>\n<pre>"+log+"</pre>"
    regex = '^(.*?)'+config['cloudwatch']['excludeRegex']+'(.*?)$'
    if config['cloudwatch']['exclude'] == 'True' and re.match(regex, log):
        logging.info("EXCLUDED: "+log)
    else:
        updater.bot.send_message(chat_id=config['telegram']['chatId'], text=message, parse_mode=ParseMode.HTML)
        logging.info("SENT: "+log)
        time.sleep(1)
