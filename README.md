# revision-grounding-eval

Asked "may I fly a small drone at night?", a retrieval pipeline over 14 CFR Part 107
answers "no" and cites § 107.29 verbatim. The citation is real. The regulation changed
in 2021 and the answer is now yes, under conditions.

Retrieval quality is not the problem. Both passages are topically correct, and the
prohibition sentence is nearly identical in both revisions: the entire difference is
the word "unless". Nothing in the pipeline knows which revision is in force.

This is a small harness for measuring that, on public documents. Work in progress.

## Where the data comes from

The eCFR API serves any CFR title as XML as it stood on a given date, back to
January 2017. Two snapshots of 14 CFR Part 107, small unmanned aircraft systems:

    curl --compressed \
      "https://www.ecfr.gov/api/versioner/v1/full/2017-01-01/title-14.xml?part=107" \
      -o data/raw/part107-2017-01-01.xml

    curl --compressed \
      "https://www.ecfr.gov/api/versioner/v1/full/2021-04-21/title-14.xml?part=107" \
      -o data/raw/part107-2021-04-21.xml

44 sections in the 2017 snapshot, 61 in the 2021 one. Of the 44 in common, 16 changed
and 17 sections were added, including the whole of Subpart D on operations over people.

The raw XML, the parsed sections and the embedded vectors are all committed, so this
is provenance rather than a build step: the pipeline runs offline with no API keys and
no model.

Two things worth knowing if you do re-fetch. The endpoint returns an error string
instead of XML unless the request permits compression, and point-in-time coverage
starts at 2017-01-01, so earlier amendment dates appear in the versions listing but
cannot be retrieved.

## How it works

Sections are chunked whole, since a section is what a person cites. Each one is
embedded with nomic-embed-text and normalised at index time, so a search is a plain
dot product rather than a cosine calculation. Every chunk carries the revision date it
came from, and each hit is checked against a per-section revision status derived by
comparing the two snapshots.

No frameworks. Cosine similarity is fifteen lines of plain Python, because the point of
this repo is what happens underneath, not which library was imported.

## Status

- `parse.py`: eCFR XML to sections as JSON. Done.
- `diff.py`: per-section revision status, added, changed, unchanged or removed. Done.
- `embed.py`: embeddings via Ollama, normalised and rounded at index time. Done.
- `search.py`: dot product, top-k, revision gate. Next.
- `evaluate.py`: recall@k and groundedness against a labelled question set. Next.
