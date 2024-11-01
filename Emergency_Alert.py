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
                # 定期的に疎通確認を行っているので、ハートビートが送られてくる
                # ハートビートは不要なので、それ以外のメッセージをprintするように設定する。
                if json_message["type"] != "heartbeat":
                    print(f"Received message: {json_message}")
                    
                    data = json_message
                    type = data["type"]
                    title = data["Title"]
                    code_type = data["CodeType"]
                    issue_source = data["Issue"]["Source"]
                    issue_status = data["Issue"]["Status"]
                    event_id = data["EventID"]
                    serial = data["Serial"]
                    announced_time = data["AnnouncedTime"]
                    origin_time = data["OriginTime"]
                    hypocenter = data["Hypocenter"]
                    latitude = data["Latitude"]
                    longitude = data["Longitude"]
                    magunitude = data["Magunitude"]
                    depth = data["Depth"]
                    max_intensity = data["MaxIntensity"]
                    accuracy_epicenter = data["Accuracy"]["Epicenter"]
                    accuracy_depth = data["Accuracy"]["Depth"]
                    accuracy_magnitude = data["Accuracy"]["Magnitude"]
                    max_int_change_string = data["MaxIntChange"]["String"]
                    max_int_change_reason = data["MaxIntChange"]["Reason"]
                    warn_area = data["WarnArea"]
                    is_sea = data["isSea"]
                    is_training = data["isTraining"]
                    is_assumption = data["isAssumption"]
                    is_warn = data["isWarn"]
                    is_final = data["isFinal"]
                    is_cancel = data["isCancel"]
                    original_text = data["OriginalText"]
                    pond = data["Pond"]

                    print(f"type: {type}")
                    print(f"title: {title}")
                    print(f"code_type: {code_type}")
                    print(f"issue_source: {issue_source}")
                    print(f"issue_status: {issue_status}")
                    print(f"event_id: {event_id}")
                    print(f"serial: {serial}")
                    print(f"announced_time: {announced_time}")
                    print(f"origin_time: {origin_time}")
                    print(f"hypocenter: {hypocenter}")
                    print(f"latitude: {latitude}")
                    print(f"longitude: {longitude}")
                    print(f"magunitude: {magunitude}")
                    print(f"depth: {depth}")
                    print(f"max_intensity: {max_intensity}")
                    print(f"accuracy_epicenter: {accuracy_epicenter}")
                    print(f"accuracy_depth: {accuracy_depth}")
                    print(f"accuracy_magnitude: {accuracy_magnitude}")
                    print(f"max_int_change_string: {max_int_change_string}")
                    print(f"max_int_change_reason: {max_int_change_reason}")
                    print(f"warn_area: {warn_area}")
                    print(f"is_sea: {is_sea}")
                    print(f"is_training: {is_training}")
                    print(f"is_assumption: {is_assumption}")
                    print(f"is_warn: {is_warn}")
                    print(f"is_final: {is_final}")
                    print(f"is_cancel: {is_cancel}")
                    print(f"original_text: {original_text}")
                    print(f"pond: {pond}")


                else:
                    timestamp = json_message["timestamp"]
                    if time_flag:
                        timestamp = timestamp_ref(timestamp)
                        time_flag = False
                    

                #print(json_message)
                #timestamp = json_message["timestamp"]
                
                #if time_flag:
                #    timestamp = timestamp_ref(timestamp)
                #    time_flag = False

                

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
