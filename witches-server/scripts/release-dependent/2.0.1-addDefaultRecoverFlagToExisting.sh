#!/usr/bin/env bash
set -e


DB=$1

COLLECTION=WUsers
FIELD=unrecovered

LEN_OLD_ID=8
LEN_NEW_ID=9

# note, escaping $set/$where/$exists operators and query double quotess

# old ID users
mongo ${DB}/witches --eval "db.${COLLECTION}.update({phone_id:{\$exists:true}, \$where:\"this.phone_id.length == ${LEN_OLD_ID}\"}, {\$set:{${FIELD}:true}}, {multi:true});"

# new ID users
mongo ${DB}/witches --eval "db.${COLLECTION}.update({phone_id:{\$exists:true}, \$where:\"this.phone_id.length == ${LEN_NEW_ID}\"}, {\$set:{${FIELD}:false}}, {multi:true});"