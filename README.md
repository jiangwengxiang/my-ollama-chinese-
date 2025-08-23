# Ollama Python 库

Ollama Python 库为 Python 3.8+ 项目集成 [Ollama](https://github.com/ollama/ollama) 提供了最简单的方式。

## 先决条件

- 需要已安装并运行 [Ollama](https://ollama.com/download)
- 使用本库前需拉取一个模型：`ollama pull <model>`，例如 `ollama pull gemma3`
  - 更多可用模型信息参见 [Ollama.com](https://ollama.com/search)。

## 安装

```sh
pip install ollama
```

## 用法

```python
from ollama import chat
from ollama import ChatResponse

response: ChatResponse = chat(model='gemma3', messages=[
  {
    'role': 'user',
    'content': '为什么天空是蓝色的？',
  },
])
print(response['message']['content'])
# 或直接从响应对象访问字段
print(response.message.content)
```

更多响应类型信息见 [_types.py](ollama/_types.py)。

## 流式响应

设置 `stream=True` 可启用响应流式输出。

```python
from ollama import chat

stream = chat(
    model='gemma3',
    messages=[{'role': 'user', 'content': '为什么天空是蓝色的？'}],
    stream=True,
)

for chunk in stream:
  print(chunk['message']['content'], end='', flush=True)
```

## 自定义客户端
可通过实例化 `ollama` 中的 `Client` 或 `AsyncClient` 创建自定义客户端。

所有额外的关键字参数将传递给 [`httpx.Client`](https://www.python-httpx.org/api/#client)。

```python
from ollama import Client
client = Client(
  host='http://localhost:11434',
  headers={'x-some-header': 'some-value'}
)
response = client.chat(model='gemma3', messages=[
  {
    'role': 'user',
    'content': '为什么天空是蓝色的？',
  },
])
```

## 异步客户端

`AsyncClient` 类用于发起异步请求。可用与 `Client` 类相同的配置字段。

```python
import asyncio
from ollama import AsyncClient

async def chat():
  message = {'role': 'user', 'content': '为什么天空是蓝色的？'}
  response = await AsyncClient().chat(model='gemma3', messages=[message])

asyncio.run(chat())
```

设置 `stream=True` 时，函数将返回 Python 异步生成器：

```python
import asyncio
from ollama import AsyncClient

async def chat():
  message = {'role': 'user', 'content': '为什么天空是蓝色的？'}
  async for part in await AsyncClient().chat(model='gemma3', messages=[message], stream=True):
    print(part['message']['content'], end='', flush=True)

asyncio.run(chat())
```

## API

Ollama Python 库的 API 设计基于 [Ollama REST API](https://github.com/ollama/ollama/blob/main/docs/api.md)

### Chat 聊天

```python
ollama.chat(model='gemma3', messages=[{'role': 'user', 'content': '为什么天空是蓝色的？'}])
```

### Generate 生成

```python
ollama.generate(model='gemma3', prompt='为什么天空是蓝色的？')
```

### List 列表

```python
ollama.list()
```

### Show 显示

```python
ollama.show('gemma3')
```

### Create 创建

```python
ollama.create(model='example', from_='gemma3', system="你是超级马里奥里的马里奥。")
```

### Copy 复制

```python
ollama.copy('gemma3', 'user/gemma3')
```

### Delete 删除

```python
ollama.delete('gemma3')
```

### Pull 拉取

```python
ollama.pull('gemma3')
```

### Push 推送

```python
ollama.push('user/gemma3')
```

### Embed 嵌入

```python
ollama.embed(model='gemma3', input='天空是蓝色的因为有瑞利散射')
```

### Embed（批量）

```python
ollama.embed(model='gemma3', input=['天空是蓝色的因为有瑞利散射', '草是绿色的因为含有叶绿素'])
```

### Ps 进程

```python
ollama.ps()
```

## 错误处理

如请求返回错误状态或流式处理时检测到错误，将会抛出异常。

```python
model = 'does-not-yet-exist'

try:
  ollama.chat(model)
except ollama.ResponseError as e:
  print('错误:', e.error)
  if e.status_code == 404:
    ollama.pull(model)
```
