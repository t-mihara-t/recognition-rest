FROM python:3.12-slim

WORKDIR /app

# 依存ライブラリのインストール（キャッシュ効率化のため先にコピー）
COPY requirement.txt .
RUN pip install --no-cache-dir -r requirement.txt

# アプリケーションコードのコピー
COPY main.py .

# Cloud RunはPORT環境変数で待機ポートを指定する
ENV PORT=8080
EXPOSE 8080

# uvicornを直接起動（本番環境向け）
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
