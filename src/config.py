from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
MANUAL_DIR = DATA_DIR / "manual"

FACTS_FILE = MANUAL_DIR / "jhh_verified_facts.json"

APP_TITLE = "Johns Hopkins Readmission & Quality Intelligence Dashboard"
APP_SUBTITLE = "Source-verified dashboard for public quality, safety, and readmission intelligence"

SOURCE_PAGES = {
    "Medicare Care Compare - The Johns Hopkins Hospital": "https://www.medicare.gov/care-compare/details/hospital/210009/view-all?city=Baltimore&state=MD&zipcode=",
    "CMS Hospital Readmissions Reduction Program (HRRP)": "https://data.cms.gov/provider-data/dataset/9n3s-kdb3",
    "CMS Hospital General Information": "https://data.cms.gov/provider-data/dataset/xubh-q36u",
    "Johns Hopkins Readmissions": "https://www.hopkinsmedicine.org/patient-safety/readmissions",
    "Johns Hopkins Readmission Impact Article": "https://www.hopkinsmedicine.org/news/articles/2018/08/interventions-reduce-unnecessary-readmissions",
    "Johns Hopkins Medicine Fast Facts PDF": "https://www.hopkinsmedicine.org/-/media/jhm/documents/entity-fact-sheets/jhm-fast-facts.pdf",
    "Leapfrog Hospital Safety Grade": "https://www.hospitalsafetygrade.org/h/the-johns-hopkins-hospital"
}
