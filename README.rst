===========
``date.py``
===========


``date.py`` is a utility to assist with dealing with dates. Namely, questions
such as "what is this input, in my timezone?", or, "what is this input's POSIX
timestamp?

It's still a work-in-progress, but some things are already doable.

An example::

    % python date.py 2015-03-14T09:26:53+01:00
    Your input: 2015-03-14 09:26:53+01:00
    In America/Los_Angeles: 2015-03-14 01:26:53-07:00
    In UTC: 2015-03-14 08:26:53+00:00
    As a POSIX timestamp: 1426321613.0

The program, at a minimum, attempts to output things that are useful to you.
Here, it defaults to showing the local timezone (here,
``America/Los_Angeles``), the entered time in UTC, and the entered time as a
POSIX timestamp.
