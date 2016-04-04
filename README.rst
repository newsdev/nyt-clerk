.. figure:: https://cloud.githubusercontent.com/assets/109988/9503675/7a4bdfee-4c06-11e5-8619-e8f85ccb49f2.png
   :alt: 

Usage
=====

::

    pip install -e git@github.com:newsdev/nyt-clerk.git#egg=clerk
    clerk justices

Data
====

-  ``clerk cases``: SCDB fields about decided merits
   cases, excluding the justice and vote details.
-  ``clerk votes``: SCDB fields about a single justice's
   vote in a single case.
-  ``clerk courts``: Data about the ideology for 
   each Court term.
-  ``clerk justices``: Data about the ideology and
   qualifications for each Justice before they were confirmed.
-  ``clerk justice_terms``: Data about the ideology of
   each individual Justice during each Court term.

SCDB Data
---------

SCDB data includes cases from 1791 term to the 2014 term. Many fields
need to be mapped to their full values. The SCDB `maintains an online
codebook <http://scdb.wustl.edu/documentation.php>`__ with these maps.


Ideology / Qualification Scores
-------------------------------

Martin-Quinn scores measure the relative ideology of a Justice or a
Supreme Court term to the median Justice. Andrew Martin and Kevin Quinn
`wrote an excellent
paper <http://mqscores.berkeley.edu/media/pa02.pdf>`__ about the method.

Segal-Cover scores measure the ideology and qualification of an
individual Justice *before* their appointment to the Court. Jeffrey
Segal `wrote a
summary <http://www.stonybrook.edu/commcms/polisci/jsegal/QualTable.pdf>`__
and shows the raw data as a table (warning: PDF).
