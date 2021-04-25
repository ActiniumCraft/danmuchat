# -*- coding: utf-8 -*-
# 实现一个可被其他 Python 程序调用的 BiliBili 弹幕获取 API，并支持发送消息
import requests
import time


class BiliBiliLive(object):
    def __init__(self, room_id=''):
        """Initialize the information of the live broadcast room.

        Args:
            room_id: Live room id, as string.
        """
        self.room_id = room_id
        self.get_payload = {'roomid': self.room_id}

    def get_barrage(self) -> str:
        barrage = requests.get('https://api.live.bilibili.com/xlive/web-room/v1/dM/gethistory', params=self.get_payload)
        return barrage.text

    def send_barrage(self, message='', cookies=''):  # 能用是能用，不过设置起来比较麻烦
        send_payload = {'msg': message,
                        'roomid': self.room_id,
                        'color': '16777215',
                        'fontsize': '25',
                        'mode': '1',
                        'rnd': str(int(time.time())),
                        'csrf_token': '',
                        'csrf': '',
                        'bubble': '0'}
        cookies_payload = {'cookies': cookies}
        requests.post('https://api.live.bilibili.com/msg/send', data=send_payload, cookies=cookies_payload)
