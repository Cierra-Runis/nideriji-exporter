'''
将你的日记里导出的 json 转化为 Mercurius 里的 json
diary.py
'''

import datetime
import json
import os
import time
import tkinter
from tkinter import filedialog
from typing import Iterable

MOOD_DICT: dict = {
    'excited': '大笑',
    'tongue': '大笑',
    'cool': '开心',
    'devil': '生气',
    'happy': '开心',
    'poop': '大哭',
    'neutral': '一般',
    'sad': '失落',
    'dead': '我死',
    'normal': '一般',
}

WEATHER_DICT: dict = {
    'lightning-rainy': '303',
    'pouring': '307',
    'snow': '400',
    'snowy': '400',
    'cloudy': '104',
    'sunny': '100',
    'rainy': '305',
    'fog': '500',
    'windy': '100',
    'hail': '402',
}


class NiderijiDiary():
    '''
    Nideriji 内的 Diary 类
    '''

    deleteddate: str  # 非 'None' 则删去该类, 无用, 删去该项
    status: str  # 状态码, 无用, 删去该项
    mood: str  # 心情, 需要映射, '' 映射为 '一般' 至 Mercurius.mood
    title: str  # 标题, '' 映射为 None 至 Mercurius.titleString
    space: str  # 性别, 无用, 删去该项
    ts: str  # 最后修改时间, 映射为 Mercurius.latestEditTime
    content: str  # 内容, 假定内容为 string
    # 则映射为 [{'insert': string + '\n'}] 至 Mercurius.contentJsonString
    weather: str  # 天气, 需要映射, '' 映射为 '100' 至 Mercurius.weather
    user: str  # 用户 id, 无用, 删去该项
    createddate: str  # 日记所属日期, 映射为 Mercurius.createDateTime
    createdtime: str  # 日记创建日期, 无用, 删去该项
    id: str  # 日记 id, 无用, 删去该项


class MercuriusDiary():
    '''
    Mercurius 内的 Diary 类
    '''
    mood: str
    weather: str
    id: int
    latestEditTime: int
    createDateTime: int
    contentJsonString: str
    titleString: str | None


def select_file_dir(
    title: str,
    filetype: Iterable[tuple[str, str | list[str] | tuple[str, ...]]]
    | None = ...
) -> str:
    '''
    选择文件并返回文件地址
    '''
    root = tkinter.Tk()
    root.withdraw()
    return filedialog.askopenfilename(
        title=title,
        filetypes=filetype,
    )


if __name__ == '__main__':
    os.system('cls')

    nideriji: list[NiderijiDiary] = []
    mercurius: list[dict] = []

    with open(
            select_file_dir(
                title='请选取 Nideriji Exporter 导出的 json 文件',
                filetype=(('json files', '*.json'), ),
            ),
            'r',
            encoding='utf-8',
    ) as f:
        data = json.loads(f.read())
        for i in reversed(data):
            niderijiDiary = NiderijiDiary()
            niderijiDiary.__dict__ = i
            nideriji.append(niderijiDiary)

    index = 0
    for i in nideriji:
        if i.__dict__['deleteddate'] == 'None':
            mercuriusDiary = MercuriusDiary()
            mercuriusDiary.mood = i.mood != '' and MOOD_DICT[i.mood] or '一般'
            mercuriusDiary.weather = i.weather != '' and WEATHER_DICT[
                i.weather] or '100'
            mercuriusDiary.id = index
            index += 1
            mercuriusDiary.latestEditTime = int(
                time.mktime(
                    datetime.datetime.strptime(
                        i.ts,
                        "%Y-%m-%d %H:%M:%S",
                    ).timetuple())) * 1000000
            mercuriusDiary.createDateTime = int(
                time.mktime(
                    datetime.datetime.strptime(
                        i.createddate,
                        "%Y-%m-%d",
                    ).timetuple())) * 1000000
            mercuriusDiary.contentJsonString = json.dumps(
                [{
                    'insert': i.content + '\n'
                }],
                ensure_ascii=False,
            )
            mercuriusDiary.titleString = i.title is not '' and i.title or None
            mercurius.append(mercuriusDiary.__dict__)

    mercurius.reverse()

    with open(
            'convert_output.json',
            'w+',
            encoding="utf-8",
    ) as f:
        f.write(json.dumps(
            mercurius,
            indent=4,
            ensure_ascii=False,
        ))
