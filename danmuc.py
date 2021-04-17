import os
import time
import json
import re

#from mcdreforged.api.rtext import *
from mcdreforged.api.decorator import new_thread
from watchdog.observers import Observer
from watchdog.events import *

PLUGIN_METADATA = {
	'id': 'danmuc',
	'version': '0.0.1',
	'name': 'danmuc',
	'author': [
		'Shamil_Sawaumi'
   ],
	'link': '没'
}

danmu_sub_list = set('Shamil_Sawaumi')
danmu_connection = False
server_temp = ''
help_msg = '''
================== §bBotKikai §r==================
§l这是一个通过读取弹幕姬工作日志同步服务器订阅的直播间弹幕到聊天栏的暴力插件
§6Git还没上，等我吃完了米
§7!!danmu §r显示本帮助信息
§7!!danmu toggle §r切换全局弹幕日志监听状态
§7!!danmu sub <player> §r切换名为<player>的玩家的弹幕订阅状态
'''

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        global server_temp
        if event.src_path == r'C:\Users\Administrator\Documents\弹幕姬\lastrun.txt':
            print_danmu(server_temp)
    
def on_info(server, info):
    args = info.content.split(" ")  
    if args[0] == '!!danmu':
        if (len(args) == 2):
            if args[1] == 'toggle':
                global danmu_connection
                global server_temp
                server_temp = server
                if danmu_connection:
                    danmu_connection = False
                else:
                    danmu_connection = True
                    server.execute('tellraw @a "§e§l弹幕链接启动"')
                    print_danmu(server)
                    live_track(server)
        elif (len(args) == 3):
            if args[1] == 'sub':
                global danmu_sub_list
                try:
                    danmu_sub_list.remove(args[2])
                    text = '%s%s%s' % ('"§7§o已解除玩家', args[2], '的弹幕订阅"')
                    server.execute('tellraw {} {}'.format(args[2], text))
                except KeyError:
                    danmu_sub_list.add(args[2])
                    text = '%s%s%s' % ('"§7§o已订阅弹幕至玩家', args[2], '的聊天栏"')
                    server.execute('tellraw {} {}'.format(args[2], text))
        else:
            server.reply(info, help_msg)
            
@new_thread('danmuc')
def live_track(server):
    global danmu_connection
    path = r'C:\Users\Administrator\Documents\弹幕姬'
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while danmu_connection:
            time.sleep(1)
            #server.execute(r'tellraw @a[scores={can_see_danmu=1}] "§e§l1"')
        observer.stop()
    except Warning:
        observer.stop()
    observer.join()
    server.execute('tellraw @a "§e§l弹幕链接关闭"')

def print_danmu(server):
    global danmu_sub_list
    with open(r'C:\Users\Administrator\Documents\弹幕姬\lastrun.txt', encoding="utf-8") as fp:
        lines = fp.readlines()
        last_line = '§7'+lines[-1][11:-1]
    '''
    摁读最后一行，反正不长
    '''
    for player in danmu_sub_list:
        server.execute('tellraw {} {}'.format(player, json.dumps(last_line, ensure_ascii=False)))
    fp.close()
        
def on_load(server, old):
    global danmu_connection
    danmu_connection = False
    global danmu_sub_list
    server.register_help_message('!!danmu', '同步直播间弹幕到聊天栏')   
    if old is not None and old.danmu_sub_list is not None:
        danmu_sub_list = old.danmu_sub_list
    #server.execute('scoreboard objectives add can_see_danmu dummy')
    #server.execute('scoreboard players set @a can_see_danmu 1')
    
def on_unload(server, old):
    global danmu_connection
    danmu_connection = False
    live_track(server).join()