# GitHub Mutual Followers Checker

GitHubの相互フォロー状態を確認するツールです。フォローしていても、フォローバックされていないユーザーや、フォローされているが、フォローバックしていないユーザーを特定します。

## 機能

- GitHubのフォロワーとフォロー中のユーザーリストを取得
- 相互フォローでないユーザーを特定
- 結果をJSON形式で出力
- Docker対応

## セットアップ

### 必要条件

- Python 3.9以上
- GitHubのPersonal Access Token

### インストール方法

1. リポジトリをクローン：
```bash
git clone https://github.com/yourusername/github-mutual-followers.git
cd github-mutual-followers
```

2. 依存パッケージをインストール：
```bash
pip install -r requirements.txt
```

3. 環境変数の設定：
`.env.example`ファイルを`.env`にコピーし、適切な値を設定します：
```bash
cp .env.example .env
```

そして、`.env`ファイルを編集して、以下の値を設定してください：
- `GITHUB_USERNAME`: あなたのGitHubユーザー名
- `GITHUB_TOKEN`: GitHubのPersonal Access Token（[トークンの作成方法](https://docs.github.com/ja/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)）

### Dockerを使用する場合

1. イメージのビルド：
```bash
docker build -t github-mutual-followers .
```

2. コンテナの実行：
```bash
docker run --env-file .env github-mutual-followers
```

## 使用方法

プログラムを実行すると、JSON形式で結果が出力されます：

```bash
python main.py
```

### 出力例

```json
{
  "timestamp": "2025-02-22T08:58:12+09:00",
  "username": "example_user",
  "stats": {
    "followers_count": 100,
    "following_count": 120
  },
  "not_followed_back": ["user1", "user2"],
  "not_following_back": ["user3", "user4"]
}
```
