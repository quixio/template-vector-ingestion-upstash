#!/bin/bash
# Wait a bit for initial setup scripts to complete (if needed)
sleep 10

# Modify the configuration
sed -i "s/$conf['servers'][0]['host'] = 'localhost';/$conf['servers'][0]['host'] = 'postgresdb';/" /var/www/html/conf/config.inc.php
sed -i "s/$conf['servers'][0]['sslmode'] = 'allow';/$conf['servers'][0]['sslmode'] = 'allow';/" /var/www/html/conf/config.inc.php
sed -i "s/$conf['servers'][0]['defaultdb'] = 'template1';/$conf['servers'][0]['defaultdb'] = 'test_db';/" /var/www/html/conf/config.inc.php

# Continue to the original entrypoint
exec "$@"
