# tf vacation manager

Tool which creates an out of office notice and sends it via scp to the mail server.

## Install
`pip install -U -I https://github.com/trigrab/tf-vacation-manager/archive/master.zip`

## Launch
### Windows
Use Windows Run (Win+R) and execute `tf_vacation_manager.exe`.

### Linux
Open shell and execute `tf_vacation_manager`

## First Start
Initially the tool creates all necessary config files. 

### file_path
Leave this field blank to create a single configuration for each user.
  - Win: `%appdata%\.tf-vacation-manager\`
  - Linux: `~/.tf-vacation-manager/`

### server
URL to the where vacation file should be send

### username
For authentification at server   
