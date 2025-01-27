# Wxbot

Papersus's Wxbot is a WeChat bot with ChatGPT(only Windows)

WeChat robot framework and examples based on wcferry

## Basic Usage

Now the bot only supports private chats, and does not support group chats for the time being

### Environment

- Python `>=3.9`
- WeChat `3.9.2.23`

### Install

```Shell
git clone https://github.com/flowerfalling/wxbot.git
```

### Dependencies

```Shell
# Update pip
python -m pip install -U pip

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `config.yaml` file and then enter the configuration in the `config.template.yaml` style

_If you do not use gemini and do not fill in the gemini token, please do not set the enable item of genimi to true_

### Get Start

```Shell
python demo.py

# To stop, press Ctrl+C
```

#### Users' command(your friends)

```Text
@菜单  # get the menu
```

```Text
gpt command:
  /xxx  # 与gpt对话
  /gpt help  # 获取帮助
  /gpt start  # 开启gpt连续对话
  /gpt end  # 关闭gpt连续对话
  /gpt clear  # 清空当前会话
```

```Text
gemini command:
  %xxx  # 与gpt对话
  %gemini help  # 获取帮助
  %gemini start  # 开启gpt连续对话
  %gemini end  # 关闭gpt连续对话
  %gemini clear  # 清空当前会话
```

```Text
@一言  # get a sentence
```

#### Administrator's command(you)

The following functions are currently available:

- menu
- gpt
- gemini
- hitokoto

Call any of them func

```Text
func command[me]
  /func start 开启func
  /func stop 关闭func
  /func enable username 开启用户func权限
  /func disable username 关闭用户func权限
  /func help 获取帮助
```

## Do not abuse gpt

I **picked up** this gpt API, so it could have serious consequences if misused
