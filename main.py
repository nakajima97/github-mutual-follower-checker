import requests
import os
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
      print("エラー: GITHUB_USERNAME と GITHUB_TOKEN 環境変数を設定してください。")
      return

    try:
        followers = get_users(FOLLOWERS_URL)
        following = get_users(FOLLOWING_URL)

        not_followed_back, not_following_back = find_non_mutual_followers(followers, following)
        
        print("あなたがフォローしているが、あなたをフォローしていないユーザー:")
        for user in not_followed_back:
            print(f"- {user}")

        print("\nあなたをフォローしているが、あなたがフォローしていないユーザー:")
        for user in not_following_back:
            print(f"- {user}")


    except requests.exceptions.RequestException as e:
        print(f"APIリクエストエラー: {e}")
        if e.response:
            print(f"詳細: {e.response.text}")
    except Exception as e:
        print(f"予期せぬエラー: {e}")


if __name__ == "__main__":
    main()