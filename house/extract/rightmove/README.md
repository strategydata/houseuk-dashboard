## Rightmove Extractor

this extractor crawler rightmove website for datasets:

Instead of pulling info from search pages, we now get data from individual property pages. Our crawler runs daily to keep the info updated.

To deal with duplicates:

We’ll switch the crawler to Iceberg with upsert, which should take care of duplicate issues.
