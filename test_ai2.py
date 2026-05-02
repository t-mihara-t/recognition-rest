import vertexai
from vertexai.generative_models import GenerativeModel
import subprocess
import sys

def get_project_id():
    """現在設定されているGoogle CloudプロジェクトIDを自動取得する"""
    try:
        project_id = subprocess.check_output(
            ['gcloud', 'config', 'get-value', 'project'],
            stderr=subprocess.STDOUT
        ).decode('utf-8').strip()
        
        if not project_id or project_id == "(unset)":
            print("エラー: プロジェクトIDが設定されていません。'gcloud config set project [ID]' を実行してください。")
            sys.exit(1)
        return project_id
    except Exception as e:
        print(f"プロジェクトIDの取得に失敗しました: {e}")
        sys.exit(1)

def main():
    # 1. プロジェクト情報の取得と表示
    PROJECT_ID = get_project_id()
    # 2026年現在、最も安定しているアイオワリージョンを使用
    LOCATION = "us-central1" 
    
    print(f"--- 実行環境情報 ---")
    print(f"Project ID: {PROJECT_ID}")
    print(f"Location  : {LOCATION}")
    print(f"--------------------\n")

    # 2. Vertex AIの初期化
    vertexai.init(project=PROJECT_ID, location=LOCATION)

    # 3. モデルの準備 (2026年標準の Gemini 1.5 Flash)
    # 404が出る場合は 'gemini-1.5-flash-001' などの詳細指定も試せるよう変数化
    model_name = "gemini-2.5-flash-lite"
    model = GenerativeModel(model_name)

    print(f"モデル '{model_name}' に接続中...")

    try:
        # 4. コンテンツ生成の実行
        prompt = "エクセル操作を自動化するAIサービスのキャッチコピーを、製造業のDX担当者に刺さる内容で5つ考えてください。"
        
        response = model.generate_content(prompt)
        
        print("\n=== 接続成功！AIからの回答 ===")
        print(response.text)
        print("==============================\n")
        print("おめでとうございます！これでAIエージェント開発の土台が完成しました。")

    except Exception as e:
        print("\n!!! エラーが発生しました !!!")
        print(f"エラー種別: {type(e).__name__}")
        print(f"詳細内容: {e}")
        print("\n[チェックリスト]")
        print("1. コンソールで 'Vertex AI API' が有効になっていますか？")
        print("2. 'gcloud auth application-default login' を実行しましたか？")
        print("3. プロジェクトIDに間違いはありませんか？")

if __name__ == "__main__":
    main()
