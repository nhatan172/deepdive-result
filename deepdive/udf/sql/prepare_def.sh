#!/usr/bin/env bash

set -eux
cd "$(dirname "$0")"  # move into the directory where this script is

# update samples for tagging
deepdive sql eval "
SELECT mention_id
    , concept_expression
    , explain_text
    , expectation

  FROM has_definition_inference natural join definition_mention

 WHERE  expectation >= 0.7

 ORDER BY random()
 LIMIT 100" format=csv header=1 >def_precision.csv
