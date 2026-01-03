import aiohttp
import asyncio
from typing import Any, Dict, Optional
from import_utils import *
from config.config import load_config


class HttpUtils:
    _global_session: Optional[aiohttp.ClientSession] = None
    config_load = load_config()

    def __init__(self, timeout: int = 10, retries: int = 2, base_url=config_load["request"]["base_url"]):
        self.timeout = timeout
        self.retries = retries
        self.base_url = base_url

        # 1. 初始化代理配置
        self.proxy = None
        env = self.config_load.get("environment")
        if env == "dev":
            # 假设本地 HTTP 代理端口为 20808
            self.proxy = "http://127.0.0.1:20808"
            log.info(f"🚧 检测到 dev 环境，已启用 HTTP 代理: {self.proxy}")

        # 2. 初始化全局 Session
        if HttpUtils._global_session is None or HttpUtils._global_session.closed:
            HttpUtils._global_session = aiohttp.ClientSession(
                headers={
                    "Accept": "*/*",
                    "Accept-Encoding": "gzip, deflate, br",
                    "User-Agent": "Python/1.1.0",
                    "Connection": "keep-alive"
                }
            )
        self.session = HttpUtils._global_session

    def _full_url(self, url: str) -> str:
        return url if url.startswith("http") else f"{self.base_url}/{url.lstrip('/')}"

    async def _request(self, method: str, url: str, **kwargs) -> Optional[Dict[str, Any]]:
        full_url = self._full_url(url)
        attempt = 0

        # 3. 将代理参数加入 kwargs (如果 self.proxy 存在)
        if self.proxy:
            kwargs["proxy"] = self.proxy
        
        # 统一打印请求日志
        log.info(f"[HttpUtils] Request {method} {full_url} Args: {kwargs}")

        while attempt <= self.retries:
            try:
                async with self.session.request(
                        method=method.upper(),
                        url=full_url,
                        timeout=aiohttp.ClientTimeout(total=self.timeout),
                        **kwargs
                ) as response:
                    # response.raise_for_status()
                    result = None
                    if "application/json" in response.headers.get("Content-Type", ""):
                        result = await response.json()
                    else:
                        result = {"text": await response.text(), "status_code": response.status}
                    
                    # 统一打印响应日志
                    log.info(f"[HttpUtils] Response {method} {full_url}: {result}")
                    return result

            except Exception as e:
                attempt += 1
                log.warning(f"[HttpClient] {method.upper()} {full_url} 请求失败({attempt}/{self.retries})：{e}")
                if attempt > self.retries:
                    log.error(f"[HttpClient] {method.upper()} {full_url} 请求最终失败：{e}")
                    return None

    async def get(self, url, params=None, headers=None):
        return await self._request("GET", url, params=params, headers=headers)

    async def post(self, url, data=None, json_data=None, headers=None):
        if json_data is not None:
            headers = headers or {"Content-Type": "application/json"}
            return await self._request("POST", url, json=json_data, headers=headers)
        return await self._request("POST", url, data=data, headers=headers)

    @classmethod
    async def close_global_session(cls):
        if cls._global_session and not cls._global_session.closed:
            await cls._global_session.close()