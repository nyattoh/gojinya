import tweepy
import os
import datetime

# X APIの認証情報を環境変数から取得
api_key = os.getenv('X_API_KEY')
api_secret_key = os.getenv('X_API_SECRET_KEY')
access_token = os.getenv('X_ACCESS_TOKEN')
access_token_secret = os.getenv('X_ACCESS_TOKEN_SECRET')

# Tweepyを使用してAPI認証
auth = tweepy.OAuth1UserHandler(consumer_key=api_key, consumer_secret=api_secret_key,
                                 access_token=access_token, access_token_secret=access_token_secret)
api = tweepy.API(auth)

# 現在の日付と時間を取得
now = datetime.datetime.utcnow()  # UTCで取得

# ファイル名の生成
if now.hour == 5:
    # 午前5時の動画とテキスト
    video_path = f"content/{now.strftime('%Y%m%d')}05.mp4"
    text_path = f"content/{now.strftime('%y%m%d')}05.txt"
elif now.hour == 17:
    # 午後5時の動画とテキスト
    video_path = f"content/{now.strftime('%Y%m%d')}17.mp4"
    text_path = f"content/{now.strftime('%y%m%d')}17.txt"
else:
    raise Exception("Invalid time for posting")

# 投稿するテキストファイルを読み込む
with open(text_path, 'r', encoding='utf-8') as file:
    text = file.read()

# 動画のアップロード
media = api.media_upload(video_path)

# 投稿
api.update_status(status=text, media_ids=[media.media_id_string])
