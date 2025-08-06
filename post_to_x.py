# post_to_x.py
import os
import argparse
import tweepy

def get_api():
    auth = tweepy.OAuth1UserHandler(
        consumer_key    = os.getenv('X_API_KEY'),
        consumer_secret = os.getenv('X_API_SECRET_KEY'),
        access_token    = os.getenv('X_ACCESS_TOKEN'),
        access_token_secret = os.getenv('X_ACCESS_TOKEN_SECRET')
    )
    return tweepy.API(auth)

def main():
    parser = argparse.ArgumentParser(description="Post media to X")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--file',   help="Path to media file and auto-read matching .txt for text")
    group.add_argument('--video',  help="Path to video file (requires --text)")
    parser.add_argument('--text',  help="Text content or path to text file", required=False)
    args = parser.parse_args()

    api = get_api()

    # 汎用的にファイルとテキストを取り扱う
    if args.file:
        media_path = args.file
        # 同名の .txt があれば自動読み込み
        base = os.path.splitext(media_path)[0]
        txt_path = f"{base}.txt"
        if os.path.isfile(txt_path):
            with open(txt_path, encoding='utf-8') as f:
                text = f.read()
        else:
            text = ""
    else:
        # --video が指定された場合は --text 必須
        if not args.text:
            parser.error("--video を使うときは --text を指定してください")
        media_path = args.video
        # 引数がファイルパスなら中身を、直接テキストならそのまま
        if os.path.isfile(args.text):
            with open(args.text, encoding='utf-8') as f:
                text = f.read()
        else:
            text = args.text

    # メディアアップロード＆投稿
    media = api.media_upload(media_path)
    api.update_status(status=text, media_ids=[media.media_id_string])
    print(f"Posted {media_path} with text length {len(text)}")

if __name__ == '__main__':
    main()
