#!/bin/bash
BASEREAL="ghostBD"
DBTEMPLATE="ghostBD_template"
USER="ghost"

dropdb $BASEREAL ; createdb -T $DBTEMPLATE $BASEREAL -O $USER
echo "GRANT SELECT, UPDATE, INSERT, DELETE ON geometry_columns TO $USER;GRANT SELECT ON spatial_ref_sys TO $USER;ALTER  TABLE spatial_ref_sys OWNER TO $USER;ALTER  TABLE geometry_columns OWNER TO $USER;\q" | psql $BASEREAL
