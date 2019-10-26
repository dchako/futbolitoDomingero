#set -v
psql -U postgres -c "DROP IF EXISTS DATABASE $DB_NAME"
psql -U postgres -c "CREATE DATABASE $DB_NAME ENCODING 'UTF-8'"

m syncdb --noinput
#$MANAGE migrate

#set +v
#if [ "$1" != "--no-data" ] ; then
#$MANAGE loaddata auth.json
#$MANAGE loaddata bigdeal.json
#$MANAGE loaddata flat.json
#$MANAGE loaddata planisys.json
#$MANAGE loaddata newsletter.json
#fi
