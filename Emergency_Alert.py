import asyncio
import websockets
import json
import datetime


def timestamp_ref(time):
    # ミリ秒を秒に変換
    timestamp_sec = time / 1000

    # タイムスタンプをUTCからJST (UTC+9) に変換
    utc_time = datetime.datetime.fromtimestamp(timestamp_sec, tz=datetime.timezone.utc)

    # 日本標準時 (JST) のタイムゾーン
    jst = datetime.timezone(datetime.timedelta(hours=9))
    jst_time = utc_time.astimezone(jst)
    # フォーマットして表示
    print(f"日本時間: {jst_time.strftime('%Y-%m-%d %H:%M:%S')}")

    return jst_time

# データを取得する為の関数
async def receive_data():
    websocket_url = "wss://ws-api.wolfx.jp/jma_eew"
    async with websockets.connect(websocket_url) as websocket:
        time_flag = True
        while True:
            try:
                message = await websocket.recv()
                json_message = json.loads(message)
                timestamp = json_message["timestamp"]
                
                if time_flag:
                    timestamp = timestamp_ref(timestamp)
                    time_flag = False
                # 定期的に疎通確認を行っているので、ハートビートが送られてくる
                # ハートビートは不要なので、それ以外のメッセージをprintするように設定する。
                if json_message["type"] != "heartbeat":
                    print(f"Received message: {json_message}")

                #print(f"Received message: {json_message}")
            except websockets.exceptions.ConnectionClosed:
                print("Connection closed")
                break

async def main():
    while True:
        try:
            await receive_data()
        except Exception as e:
            print(f"Error: {e}")
            print("Retrying in 5 seconds...")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
