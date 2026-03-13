# Publication candidates for review

These items appeared in **Google Scholar** but not in **OpenAlex** when comparing with `_data/publications.yml`. Review each and mark **Approve** or **Reject** for addition to the site. After you approve, add the chosen entries to `_data/publications.yml` (you can look up DOI/URL on Scholar or the journal).

---

## Recommended to ADD (likely missing peer‑reviewed papers)

| # | Year | Title | Note |
|---|------|--------|------|
| 1 | 2021 | Maximum CO2 diffusion inside leaves is limited by the scaling of cell size and genome size | Plant biophysics; likely journal article. |
| 2 | 2017 | Excess Diffuse Light Absorption in Upper Mesophyll Limits CO2 Drawdown and Depresses Photosynthesis | Leaf-level photosynthesis. |
| 3 | 2018 | In vivo quantification of plant starch reserves at micrometer resolution using X‑ray microCT imaging and machine learning | Ag + imaging + ML. |
| 4 | 2022 | End-to-end deep learning for directly estimating grape yield from ground-based imagery | Grape yield; fits lab theme. |
| 5 | 2023 | Standardizing and Centralizing Datasets for Efficient Training of Agricultural Deep Learning Models | Ag ML / data; likely workshop or conference. |
| 6 | 2022 | A workflow for segmenting soil and plant X-ray computed tomography images with deep learning in Google's Colaboratory | Methods paper (X-ray CT + DL). |
| 7 | 2024 | VisTA-SR: improving the accuracy and resolution of low-cost thermal imaging cameras for agriculture | Thermal imaging + agriculture. |
| 8 | 2022 | End-to-end prediction of uniaxial compression profiles of apples during in vitro digestion using time-series micro-computed tomography and deep learning | Food/physics + imaging + DL. |
| 9 | 2024 or 2026 | CMAViT: Integrating Climate, Management, and Remote Sensing Data for Crop Yield Prediction With Multimodel Vision Transformers | Same work may appear as 2024 (e.g. workshop) and 2026 (journal); add **one** entry once you confirm which version to list. |
| 10 | 2025 | Integration of crop modeling and sensing into molecular breeding for nutritional quality and stress tolerance | Crop modeling + sensing + breeding. |
| 11 | 2025 | Enabling Plant Phenotyping in Weedy Environments using Multi-Modal Imagery via Synthetic and Generated Training Data | Phenotyping + synthetic data. |
| 12 | 2025 | Evapotranspiration Forecasting for Weather-Driven Agricultural Water Management by Harnessing Deep Learning | ET forecasting + DL. |
| 13 | 2024 | Forecasting Satellite-based Actual Evapotranspiration using Deep Learning in California Cropping Systems | Satellite ET + DL; California focus. |
| 14 | 2023 | Site-Specific Soil Pest Management in Strawberry and Vegetable Cropping Systems Using Crop Rotation and a Needs-Based Variable Rate Fumigation Strategy | Strawberry/vegetable pest management. |
| 15 | 2022 | Leveraging Artificial Intelligence in the Improvement of Yield and Quality in Nutritional Security Crops | AI for yield/quality. |
| 16 | 2013 | Integrated economic equilibrium and life cycle assessment modeling for policy‑based consequential LCA | Early career; LCA/economics—add only if you want pre‑plant‑AI work on the site. |
| 17 | 2021 | Site-specific soil pest management in strawberry & vegetable cropping systems | May be same project as #14 (2023); add only one if duplicate. |

---

## Recommended to SKIP (already on site or not a paper)

| # | Year | Title | Reason |
|---|------|--------|--------|
| 18 | 2024 | Large-scale spatio-temporal yield estimation via deep learning using satellite and management data fusion in vineyards | **Already in** `publications.yml` (2024). |
| 19 | 2025 | California Crop Yield Benchmark: Combining Satellite Image, Climate, Evapotranspiration, and Soil Data Layers... | **Already in** `publications.yml` (2025). |
| 20 | 2023 | Davis-ag: a synthetic plant dataset for developing domain-inspired active vision in agricultural robots | **Already in** `publications.yml` as “DAVIS-Ag: A Synthetic Plant Dataset...” (2024). |
| 21 | 2025 / None | Predicting crop yield lows through the highs via binned deep imbalanced regression (two entries) | **Already in** `publications.yml` (2024). |
| 22 | 2025 | iNatAg: Multi-Class Classification Models Enabled by a Large-Scale Benchmark Dataset with 4.7 M Images... | **Already in** `publications.yml` (2025). |
| 23 | 2025 | Leaf hyperspectral reflectance detects pre‑visual stress to Fusarium wilt in strawberries | **Already in** `publications.yml` (2025). |
| 24 | 2022 | X-ray CT data with semantic annotations for the paper "A workflow for segmenting soil and plant X-ray CT images..." | **Dataset**, not a publication—skip unless you list datasets separately. |
| 25 | 2022 | Special report: AI Institute for next generation food systems (AIFS) | **Report**; skip unless you want to list reports. |
| 26 | 2024 | NSF'S NATIONAL AI INSTITUTES | **Institutional / NSF**; skip. |

---

## Also consider (from OpenAlex only)

This one was in **OpenAlex** but not in your current `publications.yml`:

- **2021** — *Structural and functional leaf diversity lead to variability in photosynthetic capacity across a range of Juglans regia genotypes*

You can add it to `_data/publications.yml` if you want it on the site.

---

## How to add approved entries

1. In Google Scholar, open the paper and copy the **DOI** or **journal URL**.
2. Add a new list item to `_data/publications.yml` in the same format as existing entries, e.g.:

```yaml
- title: "Exact title of the paper"
  authors: "Author One, Author Two, J. Mason Earles"
  year: 2024
  url: "https://doi.org/10.xxxx/yyyy"
  # optional: github: "https://github.com/..."
  # optional: podcast_url: "https://..."
```

3. Place new entries in **reverse chronological order** (newest first) within the file.
