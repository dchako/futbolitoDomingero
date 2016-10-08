source env/bin/activate

export DEBUG="True"
export DB_NAME="futbolito-domingero_prod"
echo 'PRODUCTION DATABASE (futbolito-domingero_prod)'
export DATABASE_URL="postgres://postgres:1@localhost/$DB_NAME"
echo 'FULBITO-DOMINGERO MIRROR'
export ROOT=`pwd`
export MANAGE="python $ROOT/manage.py"
alias m=$MANAGE

