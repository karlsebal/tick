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

The csv follows the **standard format** of `comma separated values`.

.. TODO link to spec

- first line
   .. hlist::
      :columns: 5

      - `#`
      - version
      - month
      - holidays left
      - over/under hours
- rest
   .. hlist::
      :columns: 6

      - tag
      - day
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
|#           | First Line            |
+------------+-----------------------+
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

Module tick
^^^^^^^^^^^

.. automodule:: tick
   :members:

Module protocol
^^^^^^^^^^^^^^^

.. automodule:: protocol
   :members:



.. vim: ai sts=3 ts=3 sw=3 expandtab ft=rst
