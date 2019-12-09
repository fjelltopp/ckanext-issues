#!/bin/sh -e
set -ex

#nosetests --ckan \
#          --nologcapture \
#          --with-pylons=subdir/test.ini \
#          --with-coverage \
#          --cover-package=ckanext.issues \
#          --cover-inclusive \
#          --cover-erase \
#          --cover-tests \
#          ckanext/issues

/usr/local/bin/ckan-nosetests \
 --ckan --with-pylons=/usr/lib/adx/ckanext-issues/test.ini /usr/lib/adx/ckanext-issues/ckanext/issues/tests