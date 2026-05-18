# Johns Hopkins Readmission & Quality Intelligence Dashboard

A source-verified Streamlit dashboard focused on public readmission, safety, and quality intelligence for The Johns Hopkins Hospital in Baltimore, Maryland.

## Why this project exists

This project was built as a public-health and hospital-quality intelligence portfolio project using official, publicly available U.S. sources only.  
It is designed to show:

- source verification
- healthcare data governance
- separation of current vs historical metrics
- dashboard development with Python and Streamlit
- professional documentation and auditability

## What this dashboard does

The dashboard summarizes selected public institutional metrics and context for The Johns Hopkins Hospital, including:

- readmission measure distribution from Medicare Care Compare
- latest federal public data update used in the app
- Leapfrog safety grade
- historical institutional context such as bed count
- historical readmission-reduction impact reported by Johns Hopkins
- official readmission-related intervention descriptions

## Data integrity rules

This project follows strict data-integrity rules:

1. Official public sources only
2. Current and historical data are clearly separated
3. No patient-level data
4. No diagnosis or treatment advice
5. No unsupported claims about Johns Hopkins outcomes
6. Every fact must trace back to a public source URL

## Verified source freshness used in this project

### Current public data used
- Medicare Care Compare page for The Johns Hopkins Hospital  
  Data last updated on 2026-05-13【40†L236-L239】【39†L80-L82】  
- CMS Hospital Readmissions Reduction Program dataset page  
  Released on 2026-05-13 and last modified on 2026-01-26  
- Leapfrog Hospital Safety Grade  
  B for Spring 2026【19†L112-L115】

### Historical / institutional context used
- Johns Hopkins Medicine Fast Facts PDF (bed count)  
  Licensed beds 1146 (Aug 2023)【23†L76-L79】  
- Johns Hopkins News article on readmission interventions  
  Historical results for 2016 (12.66% reduction, $1.4M savings)【39†L80-L82】【39†L99-L100】

## Official sources

- Medicare Care Compare - The Johns Hopkins Hospital (Medicare official site)【40†L236-L239】  
  https://www.medicare.gov/care-compare/details/hospital/210009/view-all?city=Baltimore&state=MD&zipcode=

- CMS Hospital Readmissions Reduction Program (HRRP) dataset【40†L236-L239】  
  https://data.cms.gov/provider-data/dataset/9n3s-kdb3

- CMS Hospital General Information  
  https://data.cms.gov/provider-data/dataset/xubh-q36u

- Johns Hopkins Readmissions (Patient Safety & Quality)【40†L164-L168】【40†L176-L179】  
  https://www.hopkinsmedicine.org/patient-safety/readmissions

- Johns Hopkins Readmission Impact Article (Johns Hopkins News)【39†L80-L82】【39†L99-L100】  
  https://www.hopkinsmedicine.org/news/articles/2018/08/interventions-reduce-unnecessary-readmissions

- Johns Hopkins Medicine Fast Facts PDF【23†L76-L79】  
  https://www.hopkinsmedicine.org/-/media/jhm/documents/entity-fact-sheets/jhm-fast-facts.pdf

- Leapfrog Hospital Safety Grade (The Johns Hopkins Hospital)【19†L112-L115】  
  https://www.hospitalsafetygrade.org/h/the-johns-hopkins-hospital

## Tech stack

- Python
- Streamlit
- Pandas
- Plotly

## Project structure

```text
johns-hopkins-readmission-intelligence/
├── .streamlit/
│   └── config.toml
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── data_loader.py
│   └── utils.py
├── data/
│   ├── manual/
│   │   └── jhh_verified_facts.json
│   └── raw/
│       └── .gitkeep
└── assets/
    └── screenshots/
        └── .gitkeep
