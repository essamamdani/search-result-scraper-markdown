import os
from typing import List, Dict

from pydantic import BaseModel

from dotenv import load_dotenv
import httpx
from fastapi import FastAPI, Query, Request
from fastapi.responses import JSONResponse, PlainTextResponse

from bs4 import BeautifulSoup, Comment
import json
import html2text
from youtube_transcript_api import YouTubeTranscriptApi
import re
# Load .env file
load_dotenv()

# Retrieve environment variables
SEARXNG_URL = os.getenv('SEARXNG_URL')
BROWSERLESS_URL = os.getenv('BROWSERLESS_URL')
TOKEN = os.getenv('TOKEN')
PROXY_PROTOCOL = os.getenv('PROXY_PROTOCOL', 'http')
PROXY_URL = os.getenv('PROXY_URL')
PROXY_USERNAME = os.getenv('PROXY_USERNAME')
PROXY_PASSWORD = os.getenv('PROXY_PASSWORD')
PROXY_PORT = os.getenv('PROXY_PORT')

REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', '30'))



# AI Integration
FILTER_SEARCH_RESULT_BY_AI = os.getenv('FILTER_SEARCH_RESULT_BY_AI', 'false').lower() == 'true'
AI_ENGINE = os.getenv('AI_ENGINE', 'openai')

# Domains that should only be accessed using Browserless
domains_only_for_browserless = ["twitter", "x", "facebook", "ucarspro"]

# Create FastAPI app
app = FastAPI()

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_proxies(without=False):
    if PROXY_URL and PROXY_USERNAME and PROXY_PORT:
        if without:
            return {
                "http": f"{PROXY_PROTOCOL}://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_URL}:{PROXY_PORT}",
                "https": f"{PROXY_PROTOCOL}://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_URL}:{PROXY_PORT}"
            }
        return {
            "http://": f"{PROXY_PROTOCOL}://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_URL}:{PROXY_PORT}",
            "https://": f"{PROXY_PROTOCOL}://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_URL}:{PROXY_PORT}"
        }
    return None

def fetch_content(url):
    proxies = get_proxies()
    def fetch_normal_content(url):
        try:
            response = httpx.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT, proxies=proxies, follow_redirects=True)
            response.raise_for_status()
            return response.text
        except httpx.RequestError as e:
            print(f"An error occurred while requesting {url}: {e}")
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e}")
        return None

    def fetch_browserless_content(url):
        try:
            browserless_url = f"{BROWSERLESS_URL}/content"
            params = {
                "headless": False,
                "stealth": True,
            }
            if TOKEN:
                params['token'] = TOKEN

            proxy_url = f"{PROXY_PROTOCOL}://{PROXY_URL}:{PROXY_PORT}" if PROXY_URL and PROXY_PORT else None
            if proxy_url:
                params['--proxy-server'] = proxy_url

            browserless_data = {
                "url": url,
                "rejectResourceTypes": ["image", "stylesheet"],
                "gotoOptions": {"waitUntil": "networkidle0", "timeout": REQUEST_TIMEOUT * 1000},
                "bestAttempt": True,
                "setJavaScriptEnabled": True,
            }
            if PROXY_USERNAME and PROXY_PASSWORD:
                browserless_data["authenticate"] = {
                    "username": PROXY_USERNAME,
                    "password": PROXY_PASSWORD
                }

            headers = {
                'Cache-Control': 'no-cache',
                'Content-Type': 'application/json'
            }

            response = httpx.post(browserless_url, params=params, headers=headers, data=json.dumps(browserless_data), timeout=REQUEST_TIMEOUT * 2)
            response.raise_for_status()
            return response.text
        except httpx.RequestError as e:
            print(f"An error occurred while requesting Browserless for {url}: {e}")
        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred with Browserless: {e}")
        return None

    if any(domain in url for domain in domains_only_for_browserless):
        content = fetch_browserless_content(url)
    else:
        content = fetch_normal_content(url)
        if content is None:
            content = fetch_browserless_content(url)

    return content

def get_transcript(video_id: str, format: str = "markdown"):
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, proxies=get_proxies(without=True))
        transcript = " ".join([entry['text'] for entry in transcript_list])

        # Fetch the title from the video page
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        video_page = fetch_content(video_url)
        title = extract_title(video_page)

        if format == "json":
            return JSONResponse({"url": video_url, "title": title, "transcript": transcript})
        return PlainTextResponse(f"Title: {title}\n\nURL Source: {video_url}\n\nTranscript:\n{transcript}")
    except Exception as e:
        return PlainTextResponse(f"Failed to retrieve transcript: {str(e)}")

def extract_title(html_content):
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        title = soup.find("title")
        return title.string.replace(" - YouTube", "") if title else 'No title'
    return 'No title'

def clean_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    # Remove all script, style, and other unnecessary elements
    for script_or_style in soup(["script", "style", "header", "footer", "noscript", "form", "input", "textarea", "select", "option", "button", "svg", "iframe", "object", "embed", "applet", "nav", "navbar"]):
        script_or_style.decompose()

    # remove ids "layers"
    ids = ['layers']
    
    for id_ in ids:
        tag = soup.find(id=id_)
        if tag:
            tag.decompose()
    
    # Remove unwanted classes and ids
    for tag in soup.find_all(True):
        tag.attrs = {key: value for key, value in tag.attrs.items() if key not in ['class', 'id', 'style']}
    
    # Remove comments
    for comment in soup.find_all(string=lambda text: isinstance(text, Comment)):
        comment.extract()
    
    return str(soup)

def parse_html_to_markdown(html, url, title=None):
    cleaned_html = clean_html(html)
    title_ = title or extract_title(html)

    # Convert the extracted HTML to Markdown
    text_maker = html2text.HTML2Text()
    text_maker.ignore_links = False  # Include links
    text_maker.ignore_tables = False
    text_maker.bypass_tables = False  # Format tables in Markdown
    text_maker.ignore_images = False  # Include images
    text_maker.protect_links = True   # Protect links from line breaks
    text_maker.mark_code = True       # Mark code with [code]...[/code] blocks
    
    # Convert HTML to Markdown
    markdown_content = text_maker.handle(cleaned_html)
    
    return {
        "title": title_,
        "url": url,
        "markdown_content": markdown_content
    }

def rerenker_ai(data: Dict[str, List[dict]], max_token: int = 2000) -> List[dict]:
    client = None
    model = None
    class ResultItem(BaseModel):
        title: str
        url: str
        content: str
    class SearchResult(BaseModel):
        results: List[ResultItem]
    system_message = (
        'You will be given a JSON format of search results and a search query. '
        'Extract only "exact and most" related search `results` based on the `query`. '
        'If the "content" field is empty, use the "title" or "url" field to determine relevance. '
        f' Return the results in same JSON format as you would be given, the JSON object must use the schema: {json.dumps(SearchResult.schema())}'
    )
    
    if AI_ENGINE == "groq":
        from groq import Groq
        client = Groq()
        model = os.getenv('GROQ_MODEL', 'llama3-8b-8192')

    else:
        import openai
        client = openai
        model = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo-0125')
    
    filtered_results = []
    batch_size = 10
    query = data["query"]
    results = data["results"]
    
    for i in range(0, len(results), batch_size):
        batch = results[i:i+batch_size]
        processed_batch = [
            {
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "content": item.get("content", "")
            } 
            for item in batch
        ]

        response = client.chat.completions.create(
            model=model,
            stream=False,
            messages=[
                {
                    "role": "system",
                    "content": system_message
                },
                {
                    "role": "user",
                    "content": json.dumps({"query": query, "results": processed_batch}) + "\n\nExtract the most relevant search results based on the query and ensure each result contains \"content.\" Return them in JSON format with \"title,\" \"url,\" and \"content\" fields only."
                }
            ],
            temperature=0.5,
            max_tokens=max_token,
            response_format={"type":"json_object"}

        )
        print(response.choices[0].message.content)
        batch_filtered_results = json.loads(response.choices[0].message.content)
        if 'results' in batch_filtered_results:
            filtered_results.extend(batch_filtered_results['results'])
        else:
            print(f"Warning: 'results' key missing in batch response: {batch_filtered_results}")

    return {"results": filtered_results, "query": query}

def searxng(query: str, categories: str = "general") -> list:
    searxng_url = f"{SEARXNG_URL}/search?q={query}&categories={categories}&format=json"
    try:
        response = httpx.get(searxng_url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
    except httpx.RequestError as e:
        return [{"error": f"Search query failed with error: {e}"}]
    except httpx.HTTPStatusError as e:
        return [{"error": f"Search query failed with HTTP error: {e}"}]

    search_results = response.json()
    return search_results

def search(query: str, num_results: int, json_response: bool = False) -> list:
    search_results = searxng(query)
    if FILTER_SEARCH_RESULT_BY_AI:
        search_results = rerenker_ai(search_results)

    json_return = []
    markdown_return = ""
    for result in search_results["results"][:num_results]:
        url = result["url"]
        title = result["title"]
        if "youtube" in url:
            video_id = re.search(r"v=([^&]+)", url)
            if json_response:
                json_return.append(get_transcript(video_id.group(1), "json"))
            else:
                markdown_return += get_transcript(video_id.group(1)) + "\n\n ---------------- \n\n"
            continue
        html_content = fetch_content(url)
        if html_content:
            markdown_data = parse_html_to_markdown(html_content, url, title=title)
            if markdown_data["markdown_content"].strip():  # Check if markdown content is not empty
                if json_response:
                    json_return.append(markdown_data)
                else:
                    markdown_return += (
                    f"Title: {markdown_data['title']}\n\n"
                    f"URL Source: {markdown_data['url']}\n\n"
                    f"Markdown Content:\n{markdown_data['markdown_content']}"
                ) + "\n\n ---------------- \n\n"
                
    
    if json_response:
        return JSONResponse(json_return)
    return PlainTextResponse(markdown_return)

@app.get("/images")
def get_search_images(
    q: str = Query(..., description="Search images"),
    num_results: int = Query(5, description="Number of results")
    ):
    result_list = searxng(q, categories="images")
    return JSONResponse(result_list["results"][:num_results])

@app.get("/videos")
def get_search_videos(
    q: str = Query(..., description="Search videos"),
    num_results: int = Query(5, description="Number of results")
    ):
    result_list = searxng(q, categories="videos")
    return JSONResponse(result_list["results"][:num_results])

@app.get("/")
def get_search_results(
    q: str = Query(..., description="Search query"), 
    num_results: int = Query(5, description="Number of results"),
    format: str = Query("markdown", description="Output format (markdown or json)")):
    result_list = search(q, num_results, format == "json")
    return result_list

@app.get("/r/{url:path}")
def fetch_url(request: Request, url: str, format: str = Query("markdown", description="Output format (markdown or json)")):
    if "youtube" in url:
        return get_transcript(request.query_params.get('v'), format)
    
    html_content = fetch_content(url)
    if html_content:
        markdown_data = parse_html_to_markdown(html_content, url)
        if format == "json":
            return JSONResponse(markdown_data)
        
        response_text = (
            f"Title: {markdown_data['title']}\n\n"
            f"URL Source: {markdown_data['url']}\n\n"
            f"Markdown Content:\n{markdown_data['markdown_content']}"
        )
        return PlainTextResponse(response_text)
    return PlainTextResponse("Failed to retrieve content")

# Example usage
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
