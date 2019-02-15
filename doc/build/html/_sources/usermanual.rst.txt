User’s Manual
*************

CLI
===

Options
^^^^^^^

.. option:: -h, --help    

help

.. option:: -y, --year <year>

set year

.. option:: -m, --month <month>

set month

.. option:: -d, --day <dom>

set day of month

.. option:: -D, --date

set date as if set via ``date -d``

.. option:: -Y, --yesterday   

set date to yesterday

.. note::
   The date given via :option:`-D` is parsed directly into :program:`date -d`. 

Commands
^^^^^^^^

<HH[:MM]|:MM> <description>
      appends a work <description> with the duration of <number>. Duration is given either in hours or 
      hours and minutes separated by colon or minutes preceded by a colon.

<HH:MM>-<HH:MM> <description>
   appends a work <description> for the period given.
   
parse
   parse the protocol related to the month set

   The file named :file:`Arbeitszeiten_<YY-MM>.xlsx` will be placed in the working directory

report
   parse the protocol related to the month set and send the `xlsx` file to a configured mail address

undo
   remove the last entry in the month’s protocol to which the date is set

Configuration
=============

As with version |release| all configuration is hard coded. Changes are to be made in the shell script. See :doc:`devmanual` for details.


.. vim: ai sts=3 ts=3 sw=3 expandtab ft=rst
