# -*- coding: utf-8 -*-
# @Time    : 2023/12/9 22:31
# @Author  : 之落花--falling_flowers
# @File    : GPT.py
# @Software: PyCharm
import json

import requests
import wcferry

import Config

URL = "http://w5.xjai.cc/api/chat-process"
SYSTEM_MESSAGE = "You are ChatGPT, a large language model trained by OpenAI. Follow the user's instructions carefully. Respond using markdown."
HEADERS = {
    "Host": "w5.xjai.cc",
    "Proxy-Connection": "keep-alive",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Content-Type": "application/json",
    "Origin": "http://w5.xjai.cc",
    "Referer": "http://w5.xjai.cc/",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

GPT_HELP = '''gpt command:
  /xxx 与gpt对话
  /gpt help 获取帮助
  /gpt start 开启gpt连续对话
  /gpt end 关闭gpt连续对话
  /gpt clear 清空当前会话'''


class GPTInfo(object):
    def __init__(self) -> None:
        self.__state: bool = False
        self.__top_p: float = 1.0
        self.__temperature: float = 0.8
        self.pmid: str = ""

    @property
    def state(self) -> bool:
        return self.__state

    @property
    def top_p(self) -> float:
        return self.__top_p

    @property
    def temperature(self) -> float:
        return self.__temperature

    @top_p.setter
    def top_p(self, value: float) -> None:
        if value < 0 or value > 1:
            raise ValueError("You must enter a number between 0 and 1")
        else:
            self.__top_p = value

    @temperature.setter
    def temperature(self, value: float) -> None:
        if value < 0 or value > 2:
            raise ValueError("You must enter a number between 0 and 2")
        else:
            self.__temperature = value

    def command(self, order: str) -> str:
        match order:
            case "start":
                self.__state = True
                return "ChatGPT has been turned on"
            case "end":
                self.__state = False
                return "ChatGPT has been turned off"
            case "clear":
                self.pmid = ""
                return "ChatGPT has been cleared memory"
            case "help":
                return GPT_HELP
            case _:
                return '指令错误,可发送"/gpt help"获取帮助'


class GPT(object):
    def __init__(self, wcf: wcferry.Wcf) -> None:
        self.__wcf = wcf
        self.__url: str = URL
        self.__info: dict[str, GPTInfo] = {}

    def private_reply(self, msg: wcferry.WxMsg) -> None:
        sender = msg.sender
        if sender not in Config.GPT:
            return
        user = self.__info.setdefault(sender, GPTInfo())
        content = msg.content
        if content.startswith("/gpt"):
            self.__wcf.send_text(user.command(content.split(" ")[-1]), sender)
            return
        if user.state or content.startswith("/"):
            response = self.__reply(content[int(not user.state) :], user)
            user.pmid = response["id"]
            self.__wcf.send_text("[GPT]%s" % response["text"], sender)

    @staticmethod
    def __reply(msg: str, info: GPTInfo) -> dict:
        response = json.loads(
            requests.post(
                URL,
                headers=HEADERS,
                json={
                    "prompt": msg,
                    "options": {"parentMessageId": info.pmid} if info.pmid else {},
                    "systemMessage": SYSTEM_MESSAGE,
                    "temperature": info.temperature,
                    "top_p": info.top_p,
                },
            ).text.split("&KFw6loC9Qvy&")[-1]
        )
        return {"id": response["id"], "text": response["text"]}
