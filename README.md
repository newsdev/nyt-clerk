# nyt-clerk

## Usage
```
python -m clerk.scdb
python -m clerk.scotus
```

## Data
`clerk/data/scdb_cases.json`: SCDB fields about decided merits cases, excluding the justice and vote details.
`clerk/data/scdb_justices.json`: SCDB fields about individual justices.
`clerk/data/scdb_votes.json`: SCDB fields about a single justice's vote in a single case.
`clerk/data/scotus_cases.json`: Case data from the SupremeCourt.gov site, including transcripts and audio where available.

### SCDB Data
SCDB data includes cases from 1946 term to the 2014 term. Many fields need to be mapped to their full values. The SCDB [maintains an online codebook](http://scdb.wustl.edu/documentation.php) with these maps.

### SCOTUS Data
The SupremeCourt.gov site has case data from the 2000 term until the present for some cases.
* Argument transcripts: 2000-present
* Slip opinions (decision PDFs): 2006-present
* Oral argument audio: 2010-present

## Todos
* Build inflator for turning JSON into Python objects.
* Think a bit more about the developer API.