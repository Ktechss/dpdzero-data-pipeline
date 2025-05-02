## 🚀 How to Run


# 1. Clone the repository
```bash
git clone https://github.com/Ktechss/dpdzero-data-pipeline.git
cd dpdzero-data-pipeline
```
# 2. (Optional) Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate 
```

# 3. Install dependencies
```bash
pip install -r requirements.txt
```

# 4. Run the pipeline
```bash
python main.py \
  --call_logs data/call_logs.csv \
  --agent_roster data/agent_roster.csv \
  --disposition_summary data/disposition_summary.csv
```
