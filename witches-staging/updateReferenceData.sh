#!/usr/bin/env bash

if [ $# -ne 2 ]; then
    echo "usage: $0 <from> <to>"
    exit 1
fi

echo "Creating reference tables in $2 from $1"

if [ -e dump ]; then
    rm -rf dump
fi

COLS=( "Affinities"
    "Alignments"
    "AvatarItems"
    "Books"
    "BooksPrizes"
    "Categories"
    "ChapterTable"
    "Characters"
    "ClothingCoordinates"
    "EmailTemplates"
    "GameProperties"
    "Glossary"
    "Ingredients"
    "ItemCategoryLayers"
    "ItemExchangeRate"
    "LogInBonusesMaster"
    "Potions"
    "Recipes"
    "SceneTable"
    "ShopItems"
    "UnlockBooksPoints" )

for c in ${COLS[@]}; do
    echo "dumping: $c"
    mongodump --host $1 --db witches -c $c
done

for c in ${COLS[@]}; do
    echo "restoring: $c"
    mongorestore --host $2 --db witches -c $c --drop dump/witches/${c}.bson
done
