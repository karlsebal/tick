User’s Manual
*************

CLI
===

Options
^^^^^^^

-h, --help    help
-y, --year    set year
-m, --month	  set month
-d, --day	  set day
-D, --date	  set date
-Y, --yesterday   set date to yesterday
-L, --lastmonth   set month to ``last month``

.. note::
   The date given via :option:`-D` is parsed directly into :program:`date`. So simulating the option :option:`-Y` via ``-D yesterday`` is absolutely possible.

Commands
^^^^^^^^

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