#!/bin/bash

docker stop agent-$1
docker rm agent-$1
/bin/bash ./start_agent_N.sh $1 $2
