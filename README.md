# hacknation_2025

zadanie: Dane bez twarzy
nazwa_zespolu:"nazwa_druzyny"


In our solution we are using regex and Morfeusz2 together with our defined rules and LLM engine (Gliner - NER) to anonymize sensitive data.

# Structure

Code is located in /src                                                                         \
/src                                                                                            \
|                                                                                               \
|- main.py     - launches an http server listening on :8000.                                    \
|- perftest.py - generates ouput and performance information based in test input.               \
|- rules/      - contains some base classes.                                                    \
|--- static/    - contains anonymizing rules for data that doesn't require context to process.   \

# Data flow

Incoming data is split into sentences and the passed to each of the anonymizing rules for processing.
In each pass sensitive data is replaced with corresponding token that can be used to either return a data template with fragments in brackets, or to generate new randomized data in appropriate places.


# Running

## Docker (recommended)

```bash
docker build -t anonymization .
docker run -p8000:8000 anonymization
```

## Local
For local run requirest installed and setup [morfeus](https://morfeusz.sgjp.pl/download/).

```bash

just install-env
    just install
    just main
```

In both cases the ui and api will be available at `http://localhost:8000`.

API contains only one endpoint `http://localhost:8000/api/parse` which expects a json body in format:
```json
{
  "text": "Cześć. Nazywam się Jan Kowalski"
}
```

And returning:
```json
{
  "anonymized": "Cześć, Nazywam się [firstname] [lastname]"
}
```
