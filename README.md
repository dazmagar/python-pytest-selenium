## Virtual Environment Setup

1. Run `python -m venv venv`.
3. Activate the virtual environment: `.\venv\Scripts\activate` or `source ./venv/bin/activate`
> To deactivate simply run `deactivate`
4. Replace `config.example.yaml` with your modified `config.yaml`


## Requirements Setup

After the virtual environment has been setup;

1. Run `pip install -r requirements_dev.txt --use-pep517` This should download and add all dependencies from requirements_dev.txt file.

## Linter & Formatter Setup (vs code)
1. Install `Flake8` plugin.
2. Install `Black Formatter` plugin.

## Run cases

### Local

1. `pytest` simply to run all tests with default configs
2. `pytest -k "smoke"` to run all tests with tag 'smoke'
3. `pytest -n 5` to run in 5 threads mode. 

Full doc is here: 
https://docs.pytest.org/

### Remote 
To run in remote (Lambdatest platform) you need to provide credentials to framework and run the tunnel. 

To run the tunnel:
1. Download LT binary from Lambdatest site.
2. Run it with command: 
`LT.exe --user <user> --key <key> --tunnelName <tunnel name> --verbose`

Full documentation available here: https://www.lambdatest.com/support/docs/testing-locally-hosted-pages/

To provide the framework connection parameters you can use config.yaml file or command line arguments.

For example: 
```
pytest \
-n 5 \
-k "smoke" \
--testrun_type=local \
--browser="chrome-headless" \
--alluredir="/_work/logs/allure_report" \
```
```
pytest \
-n 5 \
-k "smoke" \
--testrun_type=remote \
--browser="Chrome" \
--remote_options.lt_username="<username>" \
--remote_options.lt_access_key="<key>" \
--remote_options.lt_tunnel="smoke_tag_cases_debug" \
--remote_options.lt_build_id="smoke_tag_cases_debug_06.10" \
--alluredir="/_work/logs/allure_report" \
```

### CL Arguments list
Some custom arguments were implemented to make CI more convenient:
```
--base_url                                  Application base url (may also contain '<ENV>' substring which will be replaced with 'env' config option or --env cl argument)
--env                                       '<ENV>' part of base_url param which will be replaced with value provided
--browser={chrome,chrome-headless}          Browser name to be used during the tests
--testrun_type={local,remote}               Testrun type - may be local or remote (usually LambdaTest)
--remote_options.platform                   Remote Selenium Grid (LambdaTest) vm platform (Windows 10, etc.)
--remote_options.browser_version            Remote Selenium Grid (LambdaTest) browser version
--remote_options.lt_username                Username for LambdaTest Tunnel
--remote_options.lt_access_key              Access Key for LambdaTest Tunnel
--remote_options.lt_tunnel                  LambdaTest Tunnel name
--remote_options.lt_build_id                LambdaTest BuildID
```

For getting current version of this list simply type `pytest --help` and find section "custom options"


## Generate Reports
All information regarding to allure cl tool installation could be founded here:
https://docs.qameta.io/allure/#_installing_a_commandline

1. Run `pytest ... ` with `--alluredir` cl argument to get json-formatted report in the folder provided. 
2. Run `allure serve <allure_result_folder>` will generate the report and will run web-service version on free port to view.
