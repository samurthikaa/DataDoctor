from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import pandas as pd
import io

from analyzer import analyze_data
from cleaner import clean_data

app = FastAPI()

# ✅ Enable CORS (safe for dev)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠️ restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Serve frontend (index.html)
@app.get("/")
def home():
    return FileResponse("index.html")


# ✅ Analyze Dataset
@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    try:
        content = await file.read()
        df = pd.read_csv(io.StringIO(content.decode("utf-8", errors="ignore")))
    except Exception:
        return {"error": "Invalid CSV file"}

    issues = analyze_data(df)

    return {
        "issues": issues,
        "summary": {
            "rows": len(df),
            "columns": len(df.columns),
            "totalIssues": len(issues)
        }
    }


# ✅ Rectify Dataset
@app.post("/rectify")
async def rectify(file: UploadFile = File(...)):
    try:
        content = await file.read()
        df = pd.read_csv(io.StringIO(content.decode("utf-8", errors="ignore")))
    except Exception:
        return {"error": "Invalid CSV file"}

    cleaned_df = clean_data(df)

    return {
        "cleanedData": cleaned_df.to_csv(index=False)
    }