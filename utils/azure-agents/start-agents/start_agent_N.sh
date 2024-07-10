docker run -itd --init --name agent-$1 \
-v /work/www:/_work/reports \
--restart=always \
-e AZP_URL=https://dev.azure.com/<project_name> \
-e AZP_TOKEN=$2 \
-e AZP_POOL=<agents_pool> \
-e AZP_AGENT_NAME='agent-'$1 devopsagentubuntu22.04-python:latest
