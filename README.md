<h1 align='center'>datasets-earth</h1>

<p align=center>
  Catalogue for environmental datasets on the internet. <br><br>
  <img src="assets/map.svg" width="569"/>
</p>


## Goal

There are a lot of environmental datasets available on the internet.
But unfortunately finding these are difficult.
This repository helps searching, finding and making ones datasets public.
The main goals are:

1. low mainteanance :eyes:
2. easy discoverability :mag:
3. and fast search :runner:

## Architecture

### Datasets
All datasets are described using yaml configuration files.
These configuration files are validated against a json schema file.
A json schema is being used, because currently there is no native equivalent for yaml files.
YAML files are used, because they are more human-readable than json IMHO :shrug:.
The advantge of using a json schema is:
- standardized syntax
- informative
- supported by IDEs (`codium` :love_you_gesture:)
- validation can be automated

**Metadata**
For easy usage and mainteanance the json schema will follow the guidlines of [Dublin Core](https://en.wikipedia.org/wiki/Dublin_Core).
This allows us to have a *somewhat* :eyes: standardized naming and definition.

### Database
All datasets will be imported into a MongoDB.
Since we expect major differences between datasets a strict relational database would perform poorly.
Therfore the database will be written in MongoDB.
The document-based data structure allows for a more flexible data loading.
Further, yaml files can be directly parsed into json and saved into the database.

## Usage

### Adding new datasets
Open a PR with a new dataset file according to the json schema provided.
GitHub Actions will check for compatability and validate links.
The database and website is updated on merge.

### Updating datasets
Open PR with changes to the yaml file of the the dataset you want to change.
Github Actions, database and website updates will be the same as adding a new dataset.

### Deleting datasets
Open PR with a missing yaml file of the the dataset you want to delete.
Github Actions, database and website updates will be the same as adding a new dataset.

## Docker

- Build docker image
```bash
docker build --tag datasets-earth .
```

- Run docker image
```bash
docker run datasets-earth
```

- Enter docker image
```
docker run -it datasets-earth bash
```

- Add new dependency
```bash
docker run -v $(pwd):/code datasets-earth poetry add <package>
```

- Validate file
```bash
docker run -v $(pwd):/code datasets-earth validate <yml file> <schema>
```

## Postgresql JSON Query

Create table with id and info where json data is saved in info
```
CREATE TABLE orders (
 id serial NOT NULL PRIMARY KEY,
 info json NOT NULL
);
```

Add several rows
```
INSERT INTO orders (info)
VALUES('{ "customer": "Lily Bush", "items": {"product": "Diaper","qty": 24}}'),
      ('{ "customer": "Josh William", "items": {"product": "Toy Car","qty": 1}}'),
      ('{ "customer": "Mary Clark", "items": {"product": "Toy Train","qty": 2}}');
```

### Exact (substring) search

Search individual keys using LIKE
```
SELECT * FROM orders WHERE info ->> 'customer' LIKE '%osh%';
```

### trigram fuzzy search (in order)

Add trigram extension
```
CREATE EXTENSION pg_trgm;
```

Search using trigrams with custom threshold (default is 0.3)
```
SELECT * FROM orders WHERE SIMILARITY(info ->> 'customer', 'Jos') > 0.1;
```

Search and sort all entries using trigrams
```
SELECT * FROM orders ORDER BY SIMILARITY(info ->> 'customer', 'Jos') DESC LIMIT 3;
SELECT * FROM orders ORDER BY (info ->> 'customer') % 'Jos' DESC LIMIT 3;
SELECT * FROM orders ORDER BY 'Jos' % (info ->> 'customer') DESC LIMIT 3;
```

### trigram fuzzy search (in artifical order)

For partly comparison the ANY operator lets you compare against an array of strings
```
SELECT * FROM orders ORDER BY 'Josham' % ANY(STRING_TO_ARRAY((info ->> 'customer'), ' ')) DESC LIMIT 3;
```

### phonetic search

Add phonetic extension using SOUNDEX and METAPHONE
```
CREATE EXTENSION fuzzystrmatch;
```

### phonetic fuzzy search (this applies SOUNDEX on the whole customer string)
```
SELECT * FROM orders WHERE SOUNDEX('Jos Willi') % SOUNDEX(info ->> 'customer');
```

Split string into several words
```sql
SELECT STRING_TO_ARRAY((info ->> 'customer'), ' ') FROM orders;  -- Split each name of customer
SELECT SOUNDEX(info ->> 'customer') FROM orders;  -- Apply soundex to each customer name
SELECT METAPHONE(info ->> 'customer', 10) FROM orders;  -- Apply metaphone to each customer name with code word length limit
```

Define function to apply METAPHONE/SOUNDEX on an array of text
```sql
/* To efficiently use these methods on an array,
the query must also be split into an array of strings.
Otherwise the query results are not applicable. */

-- METAPHONE
CREATE OR REPLACE FUNCTION METAPHONE(text[], int)
RETURNS text[]
AS
$$
DECLARE
   arrStrings ALIAS FOR $1;
   maxCodeLength ALIAS FOR $2;
   returnArray text[];
BEGIN
  FOR i IN array_lower(arrStrings, 1)..array_upper(arrStrings, 1) LOOP
    returnArray[i] := METAPHONE(arrStrings[i], maxCodeLength);
  END LOOP;
  RETURN returnArray;
END;
$$
LANGUAGE plpgsql
    STABLE
RETURNS NULL ON NULL INPUT;

-- SOUNDEX
CREATE OR REPLACE FUNCTION SOUNDEX(text[])
RETURNS text[]
AS
$$
DECLARE
   arrStrings ALIAS FOR $1;
   returnArray text[];
BEGIN
  FOR i IN array_lower(arrStrings, 1)..array_upper(arrStrings, 1) LOOP
    returnArray[i] := SOUNDEX(arrStrings[i]);
  END LOOP;
  RETURN returnArray;
END;
$$
LANGUAGE plpgsql
    STABLE
RETURNS NULL ON NULL INPUT;

```

For international search one can use DMETAPHONE or DMETAPHONE_ALT
```
SELECT * FROM orders ORDER BY DMETAPHONE('Jos William') % DMETAPHONE(info ->> 'customer') DESC;
```

Order by LEVENSHTEIN distance
```
SELECT * FROM orders ORDER BY LEVENSHTEIN(info ->> 'customer', 'Jos Willi') ASC;
```

Next step is to combine these results and maybe return a weighted average for the final result table.
Additionally it would be nice to have the actually calculated values returned from the database.

## Enable JSON Schema for VSCode

The json schema can also be used to validate local files.
An example setting is added in [`./vscode/settings.json`](.vscode/settings.json) for VSCode or Codium.
Please install the yaml extension [YAML](https://marketplace.visualstudio.com/items?itemName=redhat.vscode-yaml)


## Resources

- https://medium.com/better-programming/api-development-in-python-with-flask-resful-and-mongodb-71e56a70b3a6
- https://www.digitalocean.com/community/tutorials/how-to-set-up-flask-with-mongodb-and-docker
- https://www.freecodecamp.org/news/fuzzy-string-matching-with-postgresql/
- https://www.postgresqltutorial.com/postgresql-json/
