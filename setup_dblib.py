#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Altium Database Library (DbLib) setup."""

import psycopg2
from psycopg2 import sql
import scottopart.dblib_conventions as dblib

conn = psycopg2.connect("dbname=altium user=johnston")
cur = conn.cursor()

def make_sql():
    for t, fl in dblib.table_fields.items():
        s = sql.SQL("create table {} ").format(sql.Identifier(t))
        # s.as_string(conn)
        #for f in fl:
        #    sql += '"' + f + '" ' + field_type_lookup(f) + ', '
#                s = sql.SQL("{} {}").format(sql.Identifier(f), sql.SQL(field_type_lookup(f)))

        #    print(sql)
            
