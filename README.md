# 学生成績管理システム

本アプリケーションは、学生の成績を管理・記録・可視化するための Web アプリケーションである。
学習者および管理者がそれぞれの権限に応じてデータを操作でき、リアルタイムで成績の照会および管理を行うことができる。

## 機能一覧

* 一覧表示：科目別・学籍番号別・氏名別に成績一覧を検索・表示
* 新規追加：学生情報および成績データの新規登録
* 詳細表示：特定の学生または成績の詳細情報を閲覧

## ディレクトリ構成

```
プロジェクトルート/
├── fastapi-app/          # バックエンド（FastAPI）
│   ├── app/
│   │   ├── models/       # データモデル
│   │   ├── routes/       # API ルーティング
│   │   └── main.py       # エントリーポイント
│   └── requirements.txt  # Python 依存関係
├── sys-kadai/            # フロントエンド（Vue）
│   ├── src/
│   │   ├── router/       # ルーティング設定
│   │   ├── views/        # 画面コンポーネント
│   │   └── App.vue       # ルートコンポーネント
│   ├── public/           # 静的リソース
│   └── package.json      # Node.js 依存関係
└── README.md             # 本ドキュメント
```

## 動作環境

* Node.js v18 以上
* Python 3.10 以上
* FastAPI
* データ保存方式：MongoDB

## セットアップおよび起動手順

### フロントエンド（Vue）

```bash
cd sys-kadai
npm install
npm run serve
```

以下の URL にブラウザでアクセスする。
[http://localhost:8080](http://localhost:8080)

### バックエンド（FastAPI）

```bash
cd fastapi-app
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API は以下の URL で起動する。
[http://localhost:8000](http://localhost:8000)

※ MongoDB サービスが起動していることを確認すること。
デフォルト接続先：`mongodb://localhost:27017`

## ユーザー種別

* **学生（Student）**：成績照会（科目・学籍番号・氏名）
* **管理者（Admin）**：学生管理、成績管理
* **スーパー管理者（Super Admin）**：ユーザー管理

## データモデル

* **ユーザー**：ID、タイプ、ユーザー名、パスワード
* **学生**：学籍番号、氏名、性別、状態（在学／非在学）
* **科目**：ID、科目名
* **成績**：ID、学籍番号、科目 ID、成績

## API 仕様（最低限）

| メソッド   | パス             | 内容          |
| ------ | -------------- | ----------- |
| GET    | /students      | 学生一覧取得      |
| POST   | /students      | 学生情報の新規追加   |
| GET    | /students/{id} | 特定学生の詳細情報取得 |
| PUT    | /students/{id} | 学生情報の更新     |
| DELETE | /students/{id} | 学生情報の削除     |
| GET    | /scores        | 成績一覧取得      |
| POST   | /scores        | 成績データの新規追加  |
| GET    | /scores/{id}   | 特定成績の詳細取得   |
| PUT    | /scores/{id}   | 成績の更新       |
| DELETE | /scores/{id}   | 成績の削除       |
| GET    | /courses       | 科目一覧取得      |
| POST   | /courses       | 科目の新規追加     |
| PUT    | /courses/{id}  | 科目の更新       |
| DELETE | /courses/{id}  | 科目の削除       |

## 保存戦略と選定理由

### 採用した保存方式

MongoDB

### データ構造の特徴

* データ件数：中規模
* 構造：可変
* 配列・タグ構造：あり
* 利用想定：複数ユーザーによる同時利用

### 選定理由

学生・成績・科目といったデータは相互に関連性を持つ一方で、将来的に項目追加や構造変更が発生する可能性がある。
また、複数ユーザーによる同時アクセスを想定し、拡張性と柔軟性を確保する必要がある。

MongoDB はドキュメント指向データベースであり、動的スキーマをサポートし、水平方向のスケーラビリティに優れている。
これらの特性が本アプリケーションの要件に適しているため、MongoDB を採用した。

## アクセス先

* バックエンド API：[http://localhost:8000](http://localhost:8000)
* フロントエンド：[http://localhost:8080](http://localhost:8080)
* API ドキュメント：[http://localhost:8000/docs](http://localhost:8000/docs)
