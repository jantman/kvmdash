#!/bin/bash
#
# Script to strip out unwanted parts of the DataTables <http://datatables.net/> archive, for release
#
# Unfortunately the DataTables downloadable archive includes lots of extras, docs, examples, testing, etc.
# that we don't want to distribute with kvmdash. This script strips out the unwanted portions, so we have
# an easy and reproducable way of upgrading DataTables.
#

rm -f DataTables/component.json
rm -Rf DataTables/docs
rm -Rf DataTables/examples
find DataTables/extras -type d -name docs -exec rm -Rf {} \;
rm -f DataTables/license-bsd.txt
rm -Rf DataTables/media/src
rm -f DataTables/media/images/favicon.ico
rm -f DataTables/media/images/Sorting\ icons.psd
rm -Rf DataTables/media/unit_testing
rm -f DataTables/package.json
rm -Rf DataTables/scripts
