import os
from fastapi import FastAPI, UploadFile, File
import pandas as pd
import vertexai
from vertexai.generative_models import GenerativeModel
import uvicorn

app = FastAPI()

# Cloud Runの環境変数からプロジェクトIDを取得（設定されていない場合は手動入力）
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "project-9a26ccc0-c176-4ee3-91f")
vertexai.init(project=PROJECT_ID, location="us-central1")
model = GenerativeModel("gemini-2.5-flash-lite")

@app.get("/")
def read_root():
    return {"status": "AI Excel Agent is running"}

@app.post("/analyze")
async def analyze_excel_api(file: UploadFile = File(...)):
    # アップロードされたファイルを一時的に読み込む
    df = pd.read_excel(file.file)
    data_summary = f"列名: {list(df.columns)}\nサンプル:\n{df.head(3).to_string()}"
    
    prompt = f"このエクセルデータの概要を100文字以内で解説して:\n{data_summary}"
    response = model.generate_content(prompt)
    
    return {
        "filename": file.filename,
        "analysis": response.text
    }

if __name__ == "__main__":
    # Cloud Runは環境変数 PORT で指定されたポートで待機する必要がある
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)

