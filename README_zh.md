# Jina.ai替代搜索结果抓取器及Markdown输出使用FastAPI, SearXNG, Browserless和AI集成

[English](README.md) | 中文版

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## 描述

这个项目提供了一个强大的网页抓取工具，它使用FastAPI、SearXNG和Browserless获取搜索结果并将其转换为Markdown格式。该工具包含使用代理进行网页抓取的能力，并高效地将HTML内容转换为Markdown格式。现在还增加了AI集成功能以过滤搜索结果。替代方案包括Jina.ai、FireCrawl AI、Exa AI和2markdown，提供各种针对开发者的网页抓取和搜索引擎解决方案。

## 目录
- [Jina.ai替代搜索结果抓取器及Markdown输出使用FastAPI, SearXNG, Browserless和AI集成](#jinaai替代搜索结果抓取器及markdown输出使用fastapi-searxng-browserless和ai集成)
  - [描述](#描述)
  - [目录](#目录)
  - [替代方案:](#替代方案)
  - [功能](#功能)
  - [先决条件](#先决条件)
  - [Docker设置](#docker设置)
  - [手动设置](#手动设置)
  - [使用方法](#使用方法)
    - [搜索端点](#搜索端点)
    - [获取URL内容](#获取url内容)
  - [使用代理](#使用代理)
  - [代码解释](#代码解释)
  - [许可证](#许可证)
  - [作者](#作者)
  - [贡献](#贡献)
  - [致谢](#致谢)
  - [星标历史](#星标历史)

## 替代方案:

- [Jina.ai](https://jina.ai/): 为开发者提供的强大搜索引擎。
- [FireCrawl AI](https://firecrawl.dev/): 面向开发者的网页抓取API。
- [Exa AI](https://exa.ai/): 面向开发者的网页抓取API。
- [2markdown](https://2markdown.com/): 将HTML转换为Markdown的网页抓取工具。

## 功能

- **FastAPI**: 一个现代的、快速的Python API框架。
- **SearXNG**: 一个开源的互联网元搜索引擎。
- **Browserless**: 一个网页浏览器自动化服务。
- **Markdown输出**: 将HTML内容转换为Markdown格式。
- **代理支持**: 利用代理进行安全匿名抓取。
- **AI集成**: 使用AI过滤搜索结果，提供最相关的内容。

## 先决条件

确保您已安装以下内容：

- Python 3.11
- Virtualenv
- Docker

## Docker设置

您可以使用Docker简化设置过程。按照以下步骤操作：

1. **克隆存储库**:
    ```sh
    git clone https://github.com/essamamdani/search-result-scraper-markdown.git
    cd search-result-scraper-markdown
    ```

2. **运行Docker Compose**:
    ```sh
    docker compose up --build
    ```

使用此设置，如果更改`.env`或`main.py`文件，您不再需要重新启动Docker。更改将自动重新加载。

## 手动设置

按照以下步骤进行手动设置：

1. **克隆存储库**:
    ```sh
    git clone https://github.com/essamamdani/search-result-scraper-markdown.git
    cd search-result-scraper-markdown
    ```

2. **创建并激活虚拟环境**:
    ```sh
    virtualenv venv
    source venv/bin/activate
    ```

3. **安装依赖项**:
    ```sh
    pip install -r requirements.txt
    ```

4. **在根目录创建一个.env文件**，内容如下：
    ```bash
    SEARXNG_URL=http://searxng:8080
    BROWSERLESS_URL=http://browserless:3000
    TOKEN=your_browserless_token_here  # 替换为您的实际令牌
    # PROXY_PROTOCOL=http
    # PROXY_URL=your_proxy_url
    # PROXY_USERNAME=your_proxy_username
    # PROXY_PASSWORD=your_proxy_password
    # PROXY_PORT=your_proxy_port
    REQUEST_TIMEOUT=30

    # AI集成用于搜索结果过滤
    FILTER_SEARCH_RESULT_BY_AI=true
    AI_ENGINE=groq
    # GROQ
    GROQ_API_KEY=yours_groq_api_key_here
    GROQ_MODEL=llama3-8b-8192
    # OPENAI
    # OPENAI_API_KEY=your_openai_api_key_here
    # OPENAI_MODEL=gpt-3.5-turbo-0125
    ```

5. **为SearXNG和Browserless运行Docker容器**:
    ```sh
    ./run-services.sh
    ```

6. **启动FastAPI应用**:
    ```sh
    uvicorn main:app --host 0.0.0.0 --port 8000
    ```

## 使用方法

### 搜索端点

要执行搜索查询，请发送GET请求到根端点`/`，并附带查询参数`q`（搜索查询）、`num_results`（结果数量）和`format`（获取JSON格式或默认Markdown格式的响应）。

示例:
```sh
curl "http://localhost:8000/?q=python&num_results=5&format=json" # 获取JSON格式
curl "http://localhost:8000/?q=python&num_results=5" # 默认Markdown格式
```

### 获取URL内容

要抓取并转换特定URL的内容为Markdown格式，请发送GET请求到端点`/r/{url:path}`。

示例:
```sh
curl "http://localhost:8000/r/https://example.com&format=json" # 获取JSON格式
curl "http://localhost:8000/r/https://example.com" # 默认Markdown格式
```

## 使用代理

这个项目使用Geonode代理进行网页抓取。您可以使用[我的Geonode推荐链接](https://geonode.com/invite/47389)开始使用他们的代理服务。

## 代码解释

有关代码的详细解释，请访问文章[这里](https://www.essamamdani.com/articles/search-result-scraper-markdown)。

## 许可证

这个项目是根据MIT许可证授权的。查看[LICENSE](LICENSE)文件以了解详情。

## 作者

Essa Mamdani - [essamamdani.com](https://essamamdani.com)

## 贡献

欢迎贡献！请随时提交Pull Request。

## 致谢

- [FastAPI](https://fastapi.tiangolo.com/)
- [SearXNG](https://github.com/searxng/searxng)
- [Browserless](https://www.browserless.io/)

## 星标历史

[![Star History Chart](https://api.star-history.com/svg?repos=essamamdani/search-result-scraper-markdown&type=Date)](https://star-history.com/#essamamdani/search-result-scraper-markdown&Date)