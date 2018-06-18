#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Altium Database Library (DbLib) setup."""

import scottopart.dblib_conventions as dblib

for t, fl in dblib.table_fields.items():
    sql = "create table \"" + t + "\" (\n"
    sql += ',\n'.join(['    "{}" {}'.format(f, dblib.field_type_lookup(f)) for f in fl])
    sql += '\n);\n'
    print(sql)
            
