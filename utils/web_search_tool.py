# utils/web_search_tool.py

import requests
import json
import logging
from typing import Optional, Dict, Any, List, Type, TypedDict
from requests import Response, Session

# ... (WebSearchError, SearchResultItem, APIResponse 等定义保持不变) ...
class WebSearchError(Exception):
    """Custom exception for web search failures."""
    def __init__(self, message: str, status_code: Optional[int] = None, error_code: Optional[str] = None):
        super().__init__(message)
        self.status_code = status_code
        self.error_code = error_code
        self.message = message

    def __str__(self):
        return f"WebSearchError: {self.message} (Status: {self.status_code}, Code: {self.error_code})"

class SearchResultItem(TypedDict):
    title: str
    link: str
    content: str
    pub_date: str

class APIResponse(TypedDict, total=False):
    search_result: List[SearchResultItem]
    error: Dict[str, Any]
    request_id: str


class WebSearchTool:
    """
    一个封装了智谱AI Web Search API的强大工具类 (优化版)。
    """
    def __init__(self, api_key: str, default_engine: str = "search_pro_quark", api_url: str = "https://open.bigmodel.cn/api/paas/v4/web_search"):
        if not api_key:
            raise ValueError("API Key cannot be empty.")
        
        # 【恢复】使用标准的属性名，不再需要下划线前缀
        self.api_key = api_key
        self.api_url = api_url
        self.default_engine = default_engine
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        self.session: Session = requests.Session()
        self.session.headers.update(self.headers)
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"WebSearchTool initialized with engine: '{self.default_engine}' and URL: '{self.api_url}'")

    def search(self, query: str, **kwargs) -> Optional[str]:
        if not query:
            self.logger.warning("Search query is empty. Returning None.")
            return None
        payload = self._build_payload(query, **kwargs)
        try:
            response_json = self._make_api_call(payload)
            if response_json:
                return self._format_results(response_json)
            return None
        except WebSearchError as e:
            self.logger.error(f"A search error occurred: {e}")
            raise

    def _build_payload(self, query: str, **kwargs) -> Dict[str, Any]:
        count = kwargs.get("count", 20)
        if not isinstance(count, int) or not (1 <= count <= 50):
            raise ValueError("Parameter 'count' must be an integer between 1 and 50.")
        recency_filters = ["oneDay", "oneWeek", "oneMonth", "oneYear", "noLimit"]
        recency_filter = kwargs.get("search_recency_filter")
        if recency_filter and recency_filter not in recency_filters:
            raise ValueError(f"Invalid 'search_recency_filter'. Must be one of {recency_filters}.")
        payload = {
            "search_query": query,
            "search_engine": kwargs.get("search_engine", self.default_engine),
            "search_intent": "true",
            "count": count,
            "content_size": kwargs.get("content_size", "high"),
        }
        optional_params = ["search_recency_filter", "search_domain_filter"]
        for param in optional_params:
            if param in kwargs and kwargs[param]:
                payload[param] = kwargs[param]
        self.logger.debug(f"Payload prepared: {json.dumps(payload, indent=2)}")
        return payload

    def _make_api_call(self, payload: Dict[str, Any]) -> Optional[APIResponse]:
        try:
            self.logger.info(f"Sending request to API with query: '{payload['search_query']}'")
            response: Response = self.session.post(self.api_url, json=payload, timeout=60)
            response.raise_for_status()
            try:
                response_json: APIResponse = response.json()
            except json.JSONDecodeError as e:
                raise WebSearchError("Failed to decode JSON response from API.", response.status_code) from e
            if "error" in response_json:
                error_code = response_json["error"].get("code")
                error_message = response_json["error"].get("message", "Unknown API error.")
                self.logger.error(f"API returned a business logic error: {error_code} - {error_message}")
                if error_code == "1703" and ("search_domain_filter" in payload or "search_recency_filter" in payload):
                    self.logger.warning("Strict search returned no results. Attempting a relaxed search...")
                    return self._retry_with_relaxed_conditions(payload)
                raise WebSearchError(error_message, response.status_code, error_code)
            self.logger.info("Successfully received response from API.")
            return response_json
        except requests.exceptions.HTTPError as http_err:
            error_content = ""
            try:
                error_content = response.json()
            except json.JSONDecodeError:
                error_content = response.text
            raise WebSearchError(f"HTTP error occurred: {http_err}", response.status_code) from http_err
        except requests.exceptions.RequestException as req_err:
            raise WebSearchError(f"A network request error occurred: {req_err}") from req_err

    def _retry_with_relaxed_conditions(self, original_payload: Dict[str, Any]) -> Optional[APIResponse]:
        relaxed_payload = original_payload.copy()
        relaxed_payload.pop("search_domain_filter", None)
        relaxed_payload.pop("search_recency_filter", None)
        self.logger.info(f"Retrying with relaxed payload: {json.dumps(relaxed_payload, indent=2)}")
        try:
            response = self.session.post(self.api_url, json=relaxed_payload, timeout=60)
            response.raise_for_status()
            response_json = response.json()
            self.logger.info("Relaxed search was successful.")
            if "error" in response_json:
                error_code = response_json["error"].get("code")
                error_message = response_json["error"].get("message", "Unknown API error on retry.")
                self.logger.error(f"Relaxed search also failed: {error_code} - {error_message}")
                raise WebSearchError(error_message, response.status_code, error_code)
            return response_json
        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            self.logger.error(f"Failed during relaxed retry: {e}")
            raise WebSearchError("Relaxed search attempt failed.") from e

    def _format_results(self, response_json: APIResponse) -> Optional[str]:
        search_results = response_json.get("search_result", [])
        if not search_results:
            self.logger.warning("API returned no search results in the final response.")
            return "未找到相关信息。"
        formatted_output = []
        for item in search_results:
            title = item.get("title", "无标题")
            link = item.get("link", "无链接")
            content = item.get("content", "无内容摘要")
            formatted_output.append(f"标题: {title}\n链接: {link}\n摘要: {content}\n")
        final_output = "\n\n---\n\n".join(formatted_output)
        self.logger.info(f"Successfully formatted {len(search_results)} search results.")
        return final_output

    def close(self):
        if self.session:
            self.session.close()
            self.logger.info("Requests session closed.")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
