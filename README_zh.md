# 使用 FastAPI、SearXNG、Browserless 和 AI 集成生成 Markdown 输出的 Jina.ai 替代搜索结果抓取器

中文 | [English](README.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## 描述

本项目提供了一个强大的网页抓取工具，它使用 FastAPI、SearXNG 和 Browserless 抓取搜索结果并将其转换为 Markdown 格式。该工具包括使用代理进行网页抓取的功能，并能高效地将 HTML 内容转换为 Markdown。现在还支持使用 AI 进行搜索结果过滤。替代方案包括 Jina.ai、FireCrawl AI、Exa AI 和 2markdown，为开发人员提供各种网页抓取和搜索引擎解决方案。

## 目录
- [使用 FastAPI、SearXNG、Browserless 和 AI 集成生成 Markdown 输出的 Jina.ai 替代搜索结果抓取器](#使用-fastapisearxngbrowserless-和-ai-集成生成-markdown-输出的-jinaai-替代搜索结果抓取器)
  - [描述](#描述)
  - [目录](#目录)
  - [替代方案：](#替代方案)
  - [功能](#功能)
  - [先决条件](#先决条件)
  - [Docker 设置](#docker-设置)
  - [手动设置](#手动设置)
  - [使用方法](#使用方法)
    - [搜索端点](#搜索端点)
    - [获取 URL 内容](#获取-url-内容)
    - [获取图片](#获取图片)
    - [获取视频](#获取视频)
  - [使用代理](#使用代理)
  - [路线图](#路线图)
  - [代码说明](#代码说明)
  - [许可证](#许可证)
  - [作者](#作者)
  - [贡献](#贡献)
  - [致谢](#致谢)
  - [Star 历史](#star-历史)

## 替代方案：

- [Jina.ai](https://jina.ai/): 为开发人员提供的强大搜索引擎。
- [FireCrawl AI](https://firecrawl.dev/): 为开发人员提供的网页抓取 API。
- [Exa AI](https://exa.ai/): 为开发人员提供的网页抓取 API。
- [2markdown](https://2markdown.com/): 将 HTML 转换为 Markdown 的网页抓取工具。

## 功能

- **FastAPI**: 用于构建 Python API 的现代、快速 Web 框架。
- **SearXNG**: 开源的互联网元搜索引擎。
- **Browserless**: 一个 Web 浏览器自动化服务。
- **Markdown 输出**: 将 HTML 内容转换为 Markdown 格式。
- **代理支持**: 使用代理进行安全和匿名抓取。
- **AI 集成（Reranker AI）**: 使用 AI 过滤搜索结果以提供最相关的内容。
- **YouTube 转录**: 获取 YouTube 视频转录。
- **图片和视频搜索**: 使用 SearXNG 获取图片和视频结果。

## 先决条件

确保已安装以下内容：

- Python 3.11
- Virtualenv
- Docker

## Docker 设置

您可以使用 Docker 简化设置过程。请按照以下步骤操作：

1. **克隆仓库**:
    ```sh
    git clone https://github.com/essamamdani/search-result-scraper-markdown.git
    cd search-result-scraper-markdown
    ```

2. **运行 Docker Compose**:
    ```sh
    docker compose up --build
    ```

通过此设置，如果更改 `.env` 或 `main.py` 文件，则不再需要重启 Docker。更改将自动重新加载。

## 手动设置

按照以下步骤进行手动设置：

1. **克隆仓库**:
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

4. **在根目录中创建一个 .env 文件**，内容如下：
    ```bash
    SEARXNG_URL=http://searxng:8080
    BROWSERLESS_URL=http://browserless:3000
    TOKEN=your_browserless_token_here  # 用您的实际令牌替换
    # PROXY_PROTOCOL=http
    # PROXY_URL=your_proxy_url
    # PROXY_USERNAME=your_proxy_username
    # PROXY_PASSWORD=your_proxy_password
    # PROXY_PORT=your_proxy_port
    REQUEST_TIMEOUT=30

    # 用于搜索结果过滤的 AI 集成
    FILTER_SEARCH_RESULT_BY_AI=true
    AI_ENGINE=groq
    # GROQ
    GROQ_API_KEY=yours_groq_api_key_here
    GROQ_MODEL=llama3-8b-8192
    # OPENAI
    # OPENAI_API_KEY=your_openai_api_key_here
    # OPENAI_MODEL=gpt-3.5-turbo-0125
    ```

5. **运行 SearXNG 和 Browserless 的 Docker 容器**:
    ```sh
    ./run-services.sh
    ```

6. **启动 FastAPI 应用程序**:
    ```sh
    uvicorn main:app --host 0.0.0.0 --port 8000
    ```

## 使用方法

### 搜索端点

要执行搜索查询，请向根端点 `/` 发送带有查询参数 `q`（搜索查询）、`num_results`（结果数量）和 `format`（以 JSON 或默认 Markdown 格式获取响应）的 GET 请求。

示例:
```sh
curl "http://localhost:8000/?q=python&num_results=5&format=json" # 获取 JSON 格式
curl "http://localhost:8000/?q=python&num_results=5" # 默认 Markdown 格式
```

### 获取 URL 内容

要获取并转换特定 URL 的内容为 Markdown，请向 `/r/{url:path}` 端点发送 GET 请求。

示例:
```sh
curl "http://localhost:8000/r/https://example.com&format=json" # 获取 JSON 格式
curl "http://localhost:8000/r/https://example.com" # 默认 Markdown 格式
```

### 获取图片

要获取图片搜索结果，请向 `/images` 端点发送带有查询参数 `q`（搜索查询）和 `num_results`（结果数量）的 GET 请求。

示例:
```sh
curl "http://localhost:8000/images?q=puppies&num_results=5"
```

### 获取视频

要获取视频搜索结果，请向 `/videos` 端点发送带有查询参数 `q`（搜索查询）和 `num_results`（结果数量）的 GET 请求。

示例:
```sh
curl "http://localhost:8000/videos?q=cooking+recipes&num_results=5"
```

## 使用代理

本项目使用 Geonode 代理进行网页抓取。您可以使用 [我的 Geonode 推荐链接](https://geonode.com/invite/47389) 开始使用他们的代理服务。

## 路线图

- [x] **FastAPI**: 用于构建 Python API 的现代、快速 Web 框架。
- [x] **SearXNG**: 开源的互联网元搜索引擎。
- [x] **Browserless**: 一个 Web 浏览器自动化服务。
- [x] **Markdown 输出**: 将 HTML 内容转换为 Markdown 格式。
- [x] **代理支持**: 使用代理进行安全和匿名抓取。
- [x] **AI 集成（Reranker AI）**: 使用 AI 过滤搜索结果以提供最相关的内容。
- [x] **YouTube 转录**: 获取 YouTube 视频转录。
- [x] **图片和视频搜索**: 使用 SearXNG 获取图片和视频结果。

## 代码说明

有关代码的详细说明，请访问 [这里](https://www.essamamdani.com/articles/search-result-scraper-markdown) 的文章。

## 许可证

本项目根据 MIT 许可证授权。有关详细信息，请参阅 [LICENSE](LICENSE) 文件。

## 作者

Essa Mamdani - [essamamdani.com](https://essamamdani.com)

## 贡献

欢迎贡献！请随时提交 Pull Request。

## 致谢

- [FastAPI](https://fastapi.tiangolo.com/)
- [SearXNG](https://github.com/searxng/searxng)
- [Browserless](https://www.browserless.io/)

## Star 历史

[![Star History Chart](https://api.star-history.com/svg?repos=essamamdani/search-result-scraper-markdown&type=Date)](https://star-history.com/#essamamdani/search-result-scraper-markdown&Date)