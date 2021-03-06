# -*- coding: utf-8 -*-
##
## This file is part of SCOAP3 Repository.
## Copyright (C) 2013 CERN.
##
## SCOAP3 Repository is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## SCOAP3 Repository is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with SCOAP3 Repository; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""
Add publisher information
"""
from invenio.bibrecord import record_get_field_value

CFG_JOURNAL_TO_PUBLISHER_MAP = {
    'physics letters b': 'Elsevier',
    'nuclear physics b': 'Elsevier',
    'advances in high energy physics': 'Hindawi Publishing Corporation',
    'chinese phys. c': 'Institute of Physics Publishing/Chinese Academy of Sciences',
    'jcap': 'Institute of Physics Publishing/SISSA',
    'new j. phys.': 'Institute of Physics Publishing/Deutsche Physikalische Gesellschaft',
    'acta physica polonica b': 'Jagiellonian University',
    'ptep': 'Oxford University Press/Physical Society of Japan',
    'epjc': 'Springer/Società Italiana di Fisica',
    'jhep': 'Springer/SISSA',
}

def check_records(records):
    """
    Add publisher if missing
    """
    for record in records:
        journal = record_get_field_value(record, '773', code='p').lower()
        publisher = record_get_field_value(record, '260', code='b')
        if not publisher:
            if journal not in CFG_JOURNAL_TO_PUBLISHER_MAP:
                record.warn("Unknown journal: %s" % journal)
                continue
            else:
                publisher = CFG_JOURNAL_TO_PUBLISHER_MAP[journal]
            for position, value in record.iterfield('260__%'):
                ## A field 260 already exist. let's add a subfield.
                record.add_subfield(position, 'b', publisher)
                break
            else:
                ## The field does not already exist. Let's add a whole field
                record.add_field('260__', value='', subfields=[('b', publisher)])
