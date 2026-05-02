import vertexai
from vertexai.generative_models import GenerativeModel
import subprocess

# プロジェクトIDを動的に取得（タイポ防止）
PROJECT_ID = subprocess.check_output(['gcloud', 'config', 'get-value', 'project']).decode('utf-8').strip()
print(f"Target Project: {PROJECT_ID}")

# 初期化：あえて us-central1 ではなく、アジアの asia-northeast1 で再試行
vertexai.init(project=PROJECT_ID, location="asia-northeast1")

# モデル名を「gemini-1.5-flash-001」に固定
# (404が出る場合は、ここが認識されていない可能性が高いです)
model = GenerativeModel("gemini-2.0-flash-light-001")

def main():
    try:
        # シンプルな生成テスト
        response = model.generate_content("エクセル操作を自動化するAIサービスのキャッチコピーを3つ考えて。")
        print("\n--- 接続成功！ ---")
        print(response.text)
    except Exception as e:
        print("\n--- デバッグ情報 ---")
        print(f"Error Type: {type(e).__name__}")
        print(f"Message: {e}")
        print("\n[対策] もし 403 なら認証、404 ならAPI有効化の反映待ちです。")

if __name__ == "__main__":
    main()

