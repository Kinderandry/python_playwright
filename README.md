# Project requirements
1. Use Python 3.12 for the project
2. Install requirements.txt
3. Execute the following commands in the terminal: `playwright install`


# Test execution
To execute all tests, open the terminal and execute the command `pytest`. If you need the specific execution options, 
modify the command as said below.

#### Selecting configuration file
Configuration files allow to store parameters for future executions.- To select a config file, 
add `-c 'configuration_file_name'`, e.g. `-c chrome.ini`


#### With Allure report generation
1. Add `--alluredir=report`
2. After tests execution, run the command `allure serve report`


#### Selecting number of parallel processes
Add `--numprocesses: N`, where N = 1, 2, 3... or 'auto'. It is recommended to set N to auto or number of CPU/2.


#### Headed browser
If you need to see, what is going on during test execution, add the command `--headed`. 
Be careful to use during parallel tests execution, because for each process a new browser window will be opened.