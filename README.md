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
