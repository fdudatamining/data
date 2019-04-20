# Fairleigh Dickinson University Datamining Open Data

The purpose of this repository is to document the data fetch and clean steps used to produce our working local database and used in our code.

## Installation

This is meant to download, populate, and clean the data used in our open data analysis. After setting up the system (see http://github.com/fdudatamining/system), run `docker-compose build && docker-compose run data` to populate the database.

Because there is *a lot* of a data--it makes sense to only download the data you need, to do so add the name of the dataset at the end of the command: `docker-compose run data the_data_name`; the name here corresponds to the name of the table in the database (and in code).

## Description

Each folder represents a database and each script populates a table in that database.
