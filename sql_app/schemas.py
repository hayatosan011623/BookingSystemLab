import datetime
from pydantic import BaseModel, Field

# BookingもCreateする時点ではidは必要ではない。


class BookingCreate(BaseModel):
    user_id: int
    room_id: int
    booked_num: int
    start_datetime: datetime.datetime
    end_datetime: datetime.datetime

# class Booking(BaseModel):
#     booking_id: int
#     user_id: int
#     room_id: int
#     booked_num: int
#     start_datetime: datetime.datetime
#     end_datetime: datetime.datetime

#     class Config:
#         orm_mode = True


class Booking(BookingCreate):
    booking_id: int

    class Config:
        orm_mode = True

# ユーザーを登録する際は、user_idはもっていないので、createのときと分けて作る必要がある


class UserCreate(BaseModel):
    user_name: str = Field(max_length=12)


# class User(BaseModel):
#     user_id: int
#     user_name: str = Field(max_length=12)

#     class Config:
#         orm_mode = True

# UserCreateを継承することで、user_nameはもっている状態になるので、idだけ追加する
class User(UserCreate):
    user_id: int

    class Config:
        orm_mode = True

# RoomもUserと同じなので割愛


class RoomCreate(BaseModel):
    room_name: str = Field(max_length=12)
    capacity: int


class Room(RoomCreate):
    room_id: int

    class Config:
        orm_mode = True
