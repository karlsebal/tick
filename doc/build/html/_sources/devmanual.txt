Developer’s Manual
******************

Overview
========

There are two components doing the job:

- the shell script as controller, making entries, calling the parser and sending reports.

- the parser creating the `xlsx` files

files and formats
=================

The controller files are stored in :file:`~/.tick/` where for each month a `csv` file is created.

csv format
----------

- first line
   - the marker ``#``
   - version
   - holidays left
   - over/under hours
- rest
   - tag
   - date
   - duration
   - from unixtime
   - to unixtime
   - description

available tags
^^^^^^^^^^^^^^

Tags available in version |release| are:

+------------+-----------------------+
| tag string | meaning               |
+============+=======================+
|e           | Entry                 |
+------------+-----------------------+
|h           | Holiday               |
+------------+-----------------------+
|c           | Overtime Compensation |
+------------+-----------------------+
|i           | Illness               |
+------------+-----------------------+

xlsx scheme
-----------

The `excel` file consists of roughly 3 Parts:

- Header with
   - Name
   - Month
   - Overview
- Body
- Footer with
   - legend
   - infoline containing technical informations like parsing date and so on

configuration
=============

Configuration is hard coded. Change the email address the report is sent to in the shell script.



.. vim: ai sts=3 ts=3 sw=3 expandtab ft=rst
