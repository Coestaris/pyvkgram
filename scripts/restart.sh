cd ../src
pm2 restart main.py --update-env --merge-logs --log-date-format="YYYY-MM-DD HH:mm Z"