#!/bin/bash

cd trading_result_app

if [ "${1}" == "celery"];
then    
    celery --app=tasks.tasks:celery worker -l INFO
elif [ "${1}" == "flower" ];
then
    celery --app=tasks.tasks:celery flower
fi