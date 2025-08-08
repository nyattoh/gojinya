import os
import argparse
import sys
import tweepy

def get_api():
    consumer_key = os.getenv('X_API_KEY')
    consumer_secret = os.getenv('X_API_SECRET_KEY')
    access_token = os.getenv('X_ACCESS_TOKEN')
    access_token_secret = os.getenv('X_ACCESS_TOKEN_SECRET')

    missing = [
        name for name, val in [
            ('X_API_KEY', consumer_key),
            ('X_API_SECRET_KEY', consumer_secret),
            ('X_ACCESS_TOKEN', access_token),
            ('X_ACCESS_TOKEN_SECRET', access_token_secret),
        ] if not val
    ]
    if missing:
        print(f"Missing required environment variables: {', '.join(missing)}", file=sys.stderr)
        sys.exit(1)

    auth = tweepy.OAuth1UserHandler(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )
    return tweepy.API(auth, wait_on_rate_limit=True)

def main():
    parser = argparse.ArgumentParser(description="Post media to X")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--file',  help="Path to media file; will auto-read matching .txt")
    group.add_argument('--video', help="Path to video file (requires --text)")
    parser.add_argument('--text', help="Text or path to text file (required with --video)")

    args = parser.parse_args()
    api = get_api()

    # file モード: --file ひとつで動画 or 画像を投稿、同名 .txt があれば読む
    if args.file:
        media_path = args.file
        base = os.path.splitext(media_path)[0]
        txt_path = f"{base}.txt"
        if os.path.isfile(txt_path):
            with open(txt_path, encoding='utf-8') as f:
                text = f.read()
        else:
            text = ""
    else:
        # video モード: --video + --text が必須
        if not args.text:
            parser.error("--video を使う場合は --text を指定してください")
        media_path = args.video
        if os.path.isfile(args.text):
            with open(args.text, encoding='utf-8') as f:
                text = f.read()
        else:
            text = args.text

    # 投稿実行（大きい動画は chunked upload を使用）
    try:
        media = api.media_upload(filename=media_path, chunked=True) if media_path.lower().endswith('.mp4') else api.media_upload(filename=media_path)
        api.update_status(status=text, media_ids=[media.media_id_string])
        print(f"Posted {media_path} with text length {len(text)}")
    except Exception as e:
        print(f"Failed to post {media_path}: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
