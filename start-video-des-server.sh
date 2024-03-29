#!/bin/bash
# 视频 API

workdir=/data/work/LLaMA-VID/
echo "workdir=$workdir"
cd $workdir

. colors.sh

venvBinDir=venv/bin/
pythonPath=${workdir}${venvBinDir}python
echo "Python path:  $pythonPath"
. colors

jobName=uvicorn
TAILPID=`ps aux | grep "$jobName" | grep -v grep | awk '{print $2}'`
echo "${YELLOW}check $jobName pid $TAILPID ${NOCOLOR}"
[ "0$TAILPID" != "0" ] && kill -9 $TAILPID

jobName=multiprocessing
TAILPID=`ps aux | grep "$jobName" | grep -v grep | awk '{print $2}'`
echo "${YELLOW}check $jobName pid $TAILPID ${NOCOLOR}"
[ "0$TAILPID" != "0" ] && kill -9 $TAILPID



echo "${YELLOW}${pythonPath} -m uvicorn api_server:app --port 9690 --reload${NOCOLOR}"
nohup ${pythonPath} -m uvicorn api_server:app --port 9690 --reload > /dev/null 2>&1 &


