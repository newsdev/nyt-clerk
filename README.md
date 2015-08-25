# nyt-clerk

## SCDB data
From the SCDB, `nyt-clerk` can extract Cases, Justices and Votes.

### Usage
```
python -m clerk.scdb
```
`nyt-clerk` will download the data to `clerk/data/*.json`.

## Todos
* Finish SupremeCourt.gov parser.
* Build inflator for turning JSON into Python objects.
* Think a bit more about the developer API.