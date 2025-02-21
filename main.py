import requests
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

# GitHubユーザー名とアクセストークンを設定
USERNAME = os.getenv("GITHUB_USERNAME")  # .envファイルから取得
TOKEN = os.getenv("GITHUB_TOKEN")  # .envファイルから取得

# GitHub APIのエンドポイント
FOLLOWERS_URL = f"https://api.github.com/users/{USERNAME}/followers"
FOLLOWING_URL = f"https://api.github.com/users/{USERNAME}/following"

# リクエストヘッダー (認証情報を含む)
HEADERS = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json"  # GitHub API v3を指定
}

def get_users(url):
    """指定されたURLからユーザーリストを取得する"""
    users = []
    page = 1
    while True:
        response = requests.get(f"{url}?page={page}&per_page=100", headers=HEADERS)
        response.raise_for_status()  # エラーがあれば例外を発生させる

        data = response.json()
        if not data:
            break  # データがなくなったらループを抜ける

        users.extend([user["login"] for user in data])
        page += 1
    return users

def find_non_mutual_followers(followers, following):
    """相互フォローでないユーザーを見つける"""
    followers_set = set(followers)
    following_set = set(following)

    # フォローしているが、フォローされていないユーザー
    not_followed_back = following_set - followers_set
    # フォローされているが、フォローしていないユーザー
    not_following_back = followers_set - following_set

    return not_followed_back, not_following_back


def main():
    """メイン処理"""
    if not USERNAME or not TOKEN:
        result = {
            "error": "GITHUB_USERNAME と GITHUB_TOKEN 環境変数を設定してください。",
            "timestamp": datetime.now().isoformat()
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    try:
        followers = get_users(FOLLOWERS_URL)
        following = get_users(FOLLOWING_URL)

        not_followed_back, not_following_back = find_non_mutual_followers(followers, following)
        
        # 結果をJSON形式で構造化
        result = {
            "timestamp": datetime.now().isoformat(),
            "username": USERNAME,
            "stats": {
                "followers_count": len(followers),
                "following_count": len(following)
            },
            "not_followed_back": list(not_followed_back),
            "not_following_back": list(not_following_back)
        }

        # JSON形式で出力
        print(json.dumps(result, ensure_ascii=False, indent=2))

    except requests.exceptions.RequestException as e:
        error_result = {
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }
        print(json.dumps(error_result, ensure_ascii=False, indent=2))
    except Exception as e:
        error_result = {
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }
        print(json.dumps(error_result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()