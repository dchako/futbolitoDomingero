set -v
sudo -u postgres psql -c "DROP IF EXISTS DATABASE $DB_NAME"
sudo -u postgres psql -c "CREATE DATABASE $DB_NAME ENCODING 'UTF-8'"

$MANAGE syncdb --noinput
#$MANAGE migrate

#set +v
#if [ "$1" != "--no-data" ] ; then
#$MANAGE loaddata auth.json
#$MANAGE loaddata bigdeal.json
#$MANAGE loaddata flat.json
#$MANAGE loaddata planisys.json
#$MANAGE loaddata newsletter.json
#fi
