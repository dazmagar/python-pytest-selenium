# AzureDevOps-agents
Images for self-hosted DevOps agents running in Docker.

## Building images
```
cd azure-agents\ubuntu22.04-base
docker build -t devopsagentubuntu22.04-base .
```

Then create other images that depend on it (Python support for agent jobs).
```
cd azure-agents/ubuntu22.04-python
docker build -t devopsagentubuntu22.04-python .
```
## To run the images
Create an access token `$(access_token)` in Azure DevOps
```
# from start-agents
./start_agent_N.sh $(agent_id) $(access_token)
``` 
## Additional info
forwarding MFA into local network: `--add-host {host-name}:{ip-mapped-to-host}`
mount volume for reports: `-v /work/www:/_work/reports`
