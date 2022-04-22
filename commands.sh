export FLASK_ENV=development # These commands are mostly used in production but this means it will live reload changes
alias start-https='sudo flask run --host=0.0.0.0 --port=443 --cert=adhoc'
alias start-http='sudo flask run --host=0.0.0.0 --port=80'
alias kill-foodmon='pgrep -f flask | xargs sudo kill -9'
alias foodmon-reset='curl --insecure -X POST https://0.0.0.0/cron/reset/ & curl --insecure -X POST http://0.0.0.0/cron/reset/'
