# hacknation_2025

zadanie: Dane bez twarzy
nazwa_zespolu:"nazwa_druzyny"


# Running

In order to run either do:
    just install-env
    just install
    just main

Or run 
    docker build -t anonymization .
    docker run -p8000:8000 anonymization

In both cases the ui and api will be available at `http://localhost:8000`.

API contains only one endpoint `http://localhost:8000/api/parse` which expects a json body in format:
```json
{
  "text": "Cześć. Nazywam się Jan Kowalski"
}
```

I zwraca:
```json
{
  "anonymized": "Cześć, Nazywam się [firstname] [lastname]"
}
```