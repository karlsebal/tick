Developer’s Manual
******************

Overview
========

There are two components doing the job:

- the shell script as controller, making entries, calling the parser and sending reports.

- the parser creating the `xlsx` files

files and formats
=================

The controller files are stored in :file:`~/.tick/` where for each month a `<YYYYMM>.csv` is created. Additionally there is an `.info` file containing the months values like working hour account and holidays left.

info file
---------

The `.info` file contains the month’s values::

   [<YYMM>]
   WorkingHoursAccount = <value>
   WorkingHoursWorthDay = <value>
   HolidaysLeft = <value>


csv format
----------

The csv follows the **standard format** of `comma separated values` [#csv_spec]_.

- tag
- day
- duration in seconds
- from unixtime
- to unixtime
- description

It is not neccessary that both duration and from/to are set but if they are those two times spans are validated against each other.

available tags
^^^^^^^^^^^^^^

Tags available in version |release| are:

+------------+-----------------------+
| tag string | meaning               |
+============+=======================+
|#           | First Line            |
+------------+-----------------------+
|~           | Comment               |
+------------+-----------------------+
|e           | Entry                 |
+------------+-----------------------+
|h           | Holiday               |
+------------+-----------------------+
|c           | Overtime Compensation |
+------------+-----------------------+
|i           | Illness               |
+------------+-----------------------+

.. fix vim syntax highlighting: ||

.. [#csv_spec] https://en.wikipedia.org/wiki/Comma-separated_values
 

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

Legacy Formats
--------------

The predecessor :program:`etime` used two files:

- the tracker put the data of a month into :file:`~/.etime/<YY-MM.elog` whith each line in the form ``<DD> <duration in hours in float> <description>``
- when parsing two files where created: 
   - a :file:`csv` with each line of the form ``<DD>.<MM>.;<Duration in float, comma as separator>;"<description>"``
   - a :file:`xlsx` containing a bare, unsorted list with full dates

configuration
=============

Configuration is hard coded. Change the email address the report is sent to in the shell script.

Components
==========

Controller
----------

Parser
------

API
===

Parser
------

parser
^^^^^^

.. automodule:: parser
   :members:

protocol
^^^^^^^^

.. automodule:: protocol
   :members:



.. vim: ai sts=3 ts=3 sw=3 expandtab ft=rst
