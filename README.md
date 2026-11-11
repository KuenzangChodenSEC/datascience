# Gaming Preferences and Habits — Streamlit Dashboard

## Files
- `app.py` — Streamlit dashboard application.
- `data/cleaned_gaming_survey.xlsx` — cleaned 500-response survey dataset supplied in the project ZIP.
- `requirements.txt` — Python dependencies.

## Run locally
1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the dashboard:
   ```bash
   streamlit run app.py
   ```
5. Open the local URL shown in the terminal (usually `http://localhost:8501`).

## Deploy with Streamlit Community Cloud
1. Push this folder to a GitHub repository.
2. In Streamlit Community Cloud, choose **Create app**.
3. Select the repository, branch, and `app.py` as the main file.
4. Deploy.

Keep the dataset in the `data` folder so the app can load it. If the dataset contains sensitive or identifying information, do not publish it publicly without permission.

## Dashboard pages
Overview, Demographics, Gaming Behaviour, Preferences, Relationships & Tests, and Data Explorer.

The numeric weekly-hour and monthly-spending variables are midpoint estimates converted from categorical ranges. Treat tests using these values as approximate, and do not interpret association as causation.
