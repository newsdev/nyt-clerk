# nyt-clerk

## Usage
```
python -m clerk.scdb
python -m clerk.scotus
python -m clerk.scores
```

## Data
* `clerk/data/scdb_cases.json`: SCDB fields about decided merits cases, excluding the justice and vote details.
* `clerk/data/scdb_justices.json`: SCDB fields about individual justices.
* `clerk/data/scdb_votes.json`: SCDB fields about a single justice's vote in a single case.
* `clerk/data/scotus_cases.json`: Case data from the SupremeCourt.gov site, including transcripts and audio where available.
* `clerk/data/scores_courtterms.json`: Data about the ideology of a given Court term.
* `clerk/data/scores_justices.json`: Data about the ideology and qualifications of a given Justice before they were confirmed.
* `clerk/data/scores_justicetterms.json`: Data about the ideology of an individual Justice in a given Court term.

### SCDB Data
SCDB data includes cases from 1946 term to the 2014 term. Many fields need to be mapped to their full values. The SCDB [maintains an online codebook](http://scdb.wustl.edu/documentation.php) with these maps.

### SCOTUS Data
The SupremeCourt.gov site has case data from the 2000 term until the present for some cases.
* Argument transcripts: 2000-present
* Slip opinions (decision PDFs): 2006-present
* Oral argument audio: 2010-present

### Ideology / Qualification Scores
Martin-Quinn scores measure the relative ideology of a Justice or a Supreme Court term to the median Justice. Andrew Martin and Kevin Quinn [wrote an excellent paper](http://mqscores.berkeley.edu/media/pa02.pdf) about the method.

Segal-Cover scores measure the ideology and qualification of an individual Justice *before* their appointment to the Court. Jeffrey Segal [wrote a summary](http://www.stonybrook.edu/commcms/polisci/jsegal/QualTable.pdf) and shows the raw data as a table (warning: PDF).

## Todos
* Build inflator for turning JSON into Python objects.
* Think a bit more about the developer API.