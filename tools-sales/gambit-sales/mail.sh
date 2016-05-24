#!/usr/bin/env bash
set -o errexit
START_DATE=$(date +"%Y-%m-%d" --date="$(date +%Y-%m-%d) last month")

printf "お疲れさまです。 \nGambit serverから直接送らせていただいております。\n Gambitの課金データを添付致しました。ご確認ください。\n よろしくお願い致します。\n\n Gambit Server" \
| mutt -a /home/sysdev/gambit-sales/gambit_* -s "Gambit monthly sales report for $START_DATE" \
-- yoshi.miyamoto@voltage-ent.com, s-takahashi@voltage.co.jp, se@voltage-ent.com, syspr@voltage.co.jp, koichi.miyamae@voltage-ent.com
