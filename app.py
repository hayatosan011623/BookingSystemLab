import streamlit as st
import datetime
#import random
import requests
import json
import pandas as pd

page = st.sidebar.selectbox("Choose your page", ["users", "rooms", "bookings"])


if page == "users":

    st.title("ユーザー登録画面")

    with st.form(key="user"):
        # user_id: int = random.randint(0, 10) ->登録したときに番号がつく
        user_name: str = st.text_input("ユーザー名", max_chars=12)
        data = {
            # "user_id": user_id,
            "user_name": user_name
        }
        submit_button = st.form_submit_button(label="ユーザー登録")

    if submit_button:
        # st.write("## 送信データ")
        # st.json(data)
        # st.write("## レスポンス結果")
        url = "http://127.0.0.1:8000/users"
        res = requests.post(url, json=data)
        if res.status_code == 200:
            st.success("ユーザー登録完了")
        # st.write(res.status_code)
        st.json(res.json())

elif page == "rooms":

    st.title("会議室登録画面")

    with st.form(key="room"):
        #room_id: int = random.randint(0, 10)
        room_name: str = st.text_input("会議室名", max_chars=12)
        capacity: int = st.number_input("定員", step=1)
        data = {
            # "room_id": room_id,
            "room_name": room_name,
            "capacity": capacity
        }
        submit_button = st.form_submit_button(label="会議室登録")

    if submit_button:
        # st.write("## 送信データ") #Userで確認済みなので、コメントアウト
        # st.json(data)
        # st.write("## レスポンス結果")
        url = "http://127.0.0.1:8000/rooms"
        res = requests.post(url, json=data)
        if res.status_code == 200:
            st.success("会議室登録完了")
        # st.write(res.status_code)
        st.json(res.json())

elif page == "bookings":

    st.title("会議室予約画面")

    # ユーザー一覧の取得を追加する
    url_users = "http://127.0.0.1:8000/users"
    res = requests.get(url_users)
    users = res.json()
    # st.json(users)
    # ユーザー名をキー、ユーザーIDをバリューに
    users_name = {}
    for user in users:
        # st.write(user)
        users_name[user["user_name"]] = user["user_id"]
    # st.write(users_dict)

    # 会議室一覧の取得
    url_rooms = "http://127.0.0.1:8000/rooms"
    res = requests.get(url_rooms)
    rooms = res.json()
    # st.json(rooms)
    # room名をキー、room IDをバリューに
    rooms_name = {}
    for room in rooms:
        # st.write(room)
        #rooms_dict[room["room_name"]] = [room["room_id"], room["capacity"]]
        rooms_name[room["room_name"]] = {
            "room_id": room["room_id"],
            "capacity": room["capacity"]
        }
    # st.write(rooms_dict)

    st.write("## 会議室一覧")
    df_rooms = pd.DataFrame(rooms)
    df_rooms.columns = ["会議室名", "定員", "会議室ID"]
    st.table(df_rooms)

    # 会議室予約一覧を取得する
    url_bookings = "http://127.0.0.1:8000/bookings"
    res = requests.get(url_bookings)
    bookings = res.json()
    df_bookings = pd.DataFrame(bookings)

    # idで表示すると見にくいので、idからユーザー名や会議室名で表示するようにする
    users_id = {}
    for user in users:
        users_id[user["user_id"]] = user["user_name"]

    rooms_id = {}
    for room in rooms:
        rooms_id[room["room_id"]] = {
            "room_name": room["room_name"],
            "capacity": room["capacity"]
        }

    # IDを各値に変更
    def to_user_name(x): return users_id[x]
    def to_room_name(x): return rooms_id[x]["room_name"]

    def to_datetime(x): return datetime.datetime.fromisoformat(
        x).strftime("%Y/%m/%d %H:%M")

    # 特定の列に関数を適用していく
    df_bookings["user_id"] = df_bookings["user_id"].map(to_user_name)
    df_bookings["room_id"] = df_bookings["room_id"].map(to_room_name)
    df_bookings["start_datetime"] = df_bookings["start_datetime"].map(
        to_datetime)
    df_bookings["end_datetime"] = df_bookings["end_datetime"].map(to_datetime)

    df_bookings = df_bookings.rename(columns={
        "user_id": "予約者名",
        "room_id": "会議室名",
        "booked_num": "予約人数",
        "start_datetime": "開始時刻",
        "end_datetime": "終了時刻",
        "booking_id": "予約番号",
    })

    st.write("### 予約一覧")
    st.table(df_bookings)

    with st.form(key="booking"):
        # booking_id: int = random.randint(0, 10) idは確定した後に取得する
        # user_id: int = random.randint(0, 10)　#Submitする際に表示させたいので、移動する
        # room_id: int = random.randint(0, 10)
        user_name: str = st.selectbox("予約者名", users_name.keys())
        room_name: str = st.selectbox("会議室名", rooms_name.keys())
        booked_num: int = st.number_input("予約人数", step=1, min_value=1)
        date = st.date_input("日付を入力", min_value=datetime.date.today())
        start_time = st.time_input(
            "開始時刻: ", value=datetime.time(hour=9, minute=0))
        end_time = st.time_input(
            "終了時刻: ", value=datetime.time(hour=20, minute=0))
        # data = {
        #     "booking_id": booking_id,
        #     "user_id": user_id,
        #     "room_id": room_id,
        #     "booked_num": booked_num,
        #     "start_datetime": datetime.datetime(
        #         year=date.year,
        #         month=date.month,
        #         day=date.day,
        #         hour=start_time.hour,
        #         minute=start_time.minute
        #     ).isoformat(),
        #     "end_datetime": datetime.datetime(
        #         year=date.year,
        #         month=date.month,
        #         day=date.day,
        #         hour=end_time.hour,
        #         minute=end_time.minute
        #     ).isoformat(),
        # }　#Submitボタンの中に移動する
        submit_button = st.form_submit_button(label="予約登録")

    if submit_button:
        user_id: int = users_name[user_name]
        # room_dict内は２つの辞書があるため指定する
        room_id: int = rooms_name[room_name]["room_id"]
        capacity: int = rooms_name[room_name]["capacity"]
        data = {
            # "booking_id": booking_id,
            "user_id": user_id,
            "room_id": room_id,
            "booked_num": booked_num,
            "start_datetime": datetime.datetime(
                year=date.year,
                month=date.month,
                day=date.day,
                hour=start_time.hour,
                minute=start_time.minute
            ).isoformat(),
            "end_datetime": datetime.datetime(
                year=date.year,
                month=date.month,
                day=date.day,
                hour=end_time.hour,
                minute=end_time.minute
            ).isoformat(),
        }
        # 定員より多い予約人数の場合
        if booked_num > capacity:
            st.error(
                f'{room_name}の定員は、　{capacity}名です。{capacity}名以下の予約人数のみ受け付けております')
        # 開始時刻＞終了時刻
        elif start_time >= end_time:
            st.error("開始時刻が終了時刻を超えています")
        elif start_time < datetime.time(hour=9, minute=0, second=0) or end_time > datetime.time(hour=20, minute=0, second=0):
            st.error("利用時間は9:00~20:00になります")

        else:
            # 会議室予約
            url = "http://127.0.0.1:8000/bookings"
            res = requests.post(url, json=data)
            if res.status_code == 200:
                st.success("予約完了しました")
            elif res.status_code == 404 and res.json()["detail"] == "Already booked":
                st.error("指定の時刻にはすでに予約が入っています")
            # st.write(res.status_code)
            st.json(res.json())
