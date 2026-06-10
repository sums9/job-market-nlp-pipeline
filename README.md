# End-to-End Data Pipeline & Machine Learning Project Documentation

### Prepared for: Engineering and Data Portfolio Development
**System Architecture Type:** Production-ready REST API Integration, Data Wrangling Engine, and Multi-Class Natural Language Processing (NLP) Classifier  
**Core Tech Stack:** `Python 3.14+`, `Requests`, `Pandas`, `NumPy`, `Seaborn`, `Matplotlib`, `Scikit-Learn` (TF-IDF Vectorization, Multinomial Naive Bayes)

---

## 1. System Architecture Overview

The project is built as a sequential ecosystem divided into three decoupled layers. Decoupling the pipeline stages ensures that a structural failure or latency spike at the ingestion layer does not cascade into the analytical or predictive components.

| Pipeline Stage | Core Responsibility | Primary Software Component | Data Input / Output State |
| :--- | :--- | :--- | :--- |
| **Stage 1: The Collector** | Ingests real-time raw job market records over the web via public API endpoints. | `scraper.py` (Python Standard Library + Requests) | **Input:** Network Stream (JSON) <br>**Output:** Unstructured Disk Storage (CSV) |
| **Stage 2: The Investigator** | Performs missing data evaluation, feature standardization, and token distribution tracking. | `analysis.ipynb` (Pandas, Matplotlib, Seaborn) | **Input:** Dirty Tabular File (CSV) <br>**Output:** Visual Reports & Clean Vectors |
| **Stage 3: The Predictor** | Tokenizes natural text strings into mathematical matrices to train an NLP classification model. | `analysis.ipynb` (Scikit-Learn Infrastructure) | **Input:** Labeled Token Arrays <br>**Output:** Predictive Inference Engine Model |

---

## 2. Stage 1 Deep-Dive: Data Gathering & API Infrastructure

Initially, a traditional document scraping approach was attempted. Document scraping relies on pulling the visual raw HTML tree of a website and using parsers to extract text. However, website designs change constantly. If a frontend engineer changes a single class name, the scraper crashes silently because it can no longer find the requested HTML elements.

To resolve this, we pivoted to an **Application Programming Interface (API)** model via the Arbeitnow ecosystem. An API functions as a direct contract between your script and the database server. Instead of sending formatted web pages meant for human eyes, the server drops raw, machine-readable JSON data directly into our application layer.

### Code Execution Logic Flow
1. **Network Ingestion:** The `requests.get()` function fires an HTTP GET query over port 443 (HTTPS) to the API server.
2. **State Verification:** The system evaluates the HTTP response status code. A status code of `200` implies an unhindered successful connection, whereas errors like `404` (Not Found) or `403` (Forbidden) trigger fallback error handlers.
3. **Algorithmic Dictionary Parsing:** The script unpacks the raw JSON array using `.json()` and uses structural loops to discard irrelevant fields, isolating five fundamental tracking vectors: `Job_Title`, `Company`, `Region`, `Remote`, and `URL`.
4. **Disk Writing:** The filtered records are structured into a Pandas DataFrame and committed to a local file stream as `real_live_jobs.csv`.

---

## 3. Stage 2 Deep-Dive: Feature Engineering & Exploratory Analysis

Once the data hits the disk, it enters the analytical layer inside Jupyter Notebook. Raw text is chaotic—different companies use completely different terminologies for identical positions. Before a computer can look for statistical correlations, the data must pass through structured cleaning and manipulation pipelines.

### Handling Missing Data (Null Value Mitigation)
Real-world datasets often contain missing parameters (represented as `NaN` or `Null` values) due to human entry errors or unmapped properties. Leaving null values in a dataset causes mathematical operations in Pandas and Scikit-Learn to instantly fail. We implemented a programmatic data imputation technique using `.fillna('Remote / Unspecified', inplace=True)`, mapping unrecorded geographical points into an analytical category without losing the rest of the job listing's useful text metrics.

### Algorithmic Label Generation
Because the raw API did not contain a categorical industry label to train a Machine Learning model, we engineered an active classification function that parses character sets within strings:

```python
def assign_category(title):
    title_low = str(title).lower()
    if 'analyst' in title_low or 'analytics' in title_low or 'bi' in title_low:
        return 'Data Analytics'
    elif 'data scientist' in title_low or 'machine learning' in title_low or 'ai' in title_low:
        return 'Data Science'
    elif 'engineer' in title_low or 'developer' in title_low or 'architect' in title_low:
        return 'Data Engineering'
    else:
        return 'General Tech'
