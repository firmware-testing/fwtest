#!/bin/bash

set -eu -o pipefail
FW=$1
RUN_ID=$2

LOG_DIR=log/$FW-$RUN_ID
mkdir -p $LOG_DIR

for f in fwtest/tests/0*; do
  test_name=$(basename $f | awk -F. '{print $1}')
  printf "%20s : " $test_name
  python -m fwtest.run $FW $RUN_ID $test_name > $LOG_DIR/$test_name.log
  if [ $? -eq 0 ]; then
    printf "\x1b[32mok\x1b[0m\n"
  else
    printf "\x1b[31mFAIL\x1b[0m\n"
  fi
done

