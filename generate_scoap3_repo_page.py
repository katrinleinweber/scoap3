# -*- coding: utf-8 -*-
##
## This file is part of Invenio.
## Copyright (C) 2014, 2015 CERN.
##
## Invenio is free software; you can redistribute it and/or
## modify it under the terms of the GNU General Public License as
## published by the Free Software Foundation; either version 2 of the
## License, or (at your option) any later version.
##
## Invenio is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
## General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with Invenio; if not, write to the Free Software Foundation, Inc.,
## 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

from cgi import escape

from invenio.htmlutils import remove_html_markup
from invenio.search_engine import get_collection_reclist, get_coll_i18nname, get_record
from invenio.bibrecord import record_get_field_value

CFG_JOURNALS = ['Acta',
                'Advances in High Energy Physics',
                'Chinese Physics C',
                'European Physical Journal C',
                'Journal of Cosmology and Astroparticle Physics',
                'Journal of High Energy Physics',
                'New Journal of Physics',
                'Nuclear Physics B',
                'Physics Letters B',
                'Progress of Theoretical and Experimental Physics']

def main():
    for journal in CFG_JOURNALS:
        name = get_coll_i18nname(journal)
        reclist = get_collection_reclist(journal)
        print "<h2>%s</h2>" % escape(name)
        if not reclist:
            print "<p>None yet.</p>"
            continue
        print "<p><ul>"
        for recid in reclist:
            record = get_record(recid)
            title = remove_html_markup(record_get_field_value(record, '245', code='a'), remove_escaped_chars_p=False).strip()
            doi = record_get_field_value(record, '024', '7', code='a')
            print '<li><a href="http://dx.doi.org/%s" target="_blank">%s</a>: %s</li>' % (escape(doi, True), escape(doi), title)
        print "</ul></p>"

if __name__ == "__main__":
    main()
