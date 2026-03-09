import hmac
import hashlib
import base64
import time
import json
import requests
import os
import random
import string
from dotenv import load_dotenv

# 加载 .env 环境变量
load_dotenv()

class VetMewError(Exception):
    """VetMew API 基础异常类"""
    def __init__(self, code, message):
        self.code = code
        self.message = message
        super().__init__(f"[{code}] {message}")

class VetMewAuthError(VetMewError):
    """认证或签名错误 (6001, 6004, 6005)"""
    pass

class VetMewRateLimitError(VetMewError):
    """请求频率过快 (6002)"""
    pass

class VetMewQuotaError(VetMewError):
    """额度不足 (6003)"""
    pass

class VetMewSessionError(VetMewError):
    """会话冲突或失效 (6007, 6008)"""
    pass

class VetMewContentError(VetMewError):
    """触发敏感词过滤 (6009)"""
    pass

class VetMewImageError(VetMewError):
    """图片无法识别 (6010)"""
    pass

class VetMewServerError(VetMewError):
    """服务器内部错误 (6101)"""
    pass

class VetMewClient:
    def __init__(self, api_key=None, api_secret=None):
        self.api_key = api_key or os.getenv("VETMEW_API_KEY")
        self.api_secret = api_secret or os.getenv("VETMEW_API_SECRET")
        self.base_url = "https://platformx.vetmew.com"

        if not self.api_key or not self.api_secret:
            raise VetMewAuthError(6001, "缺少 API Key 或 API Secret。请检查 .env 文件或环境变量。")

        # 错误码到异常类的映射
        self._error_mapping = {
            6001: VetMewAuthError,
            6002: VetMewRateLimitError,
            6003: VetMewQuotaError,
            6004: VetMewAuthError,
            6005: VetMewAuthError,
            6007: VetMewSessionError,
            6008: VetMewSessionError,
            6009: VetMewContentError,
            6010: VetMewImageError,
            6101: VetMewServerError
        }

    def _handle_error_response(self, response_json):
        """解析 API 返回的 JSON 错误信息并抛出对应异常"""
        code = response_json.get("code", 0)
        msg = response_json.get("msg", "未知错误")
        
        # 处理敏感词过滤逻辑的脱敏
        if code == 6009:
            msg = "您的输入包含敏感内容，请修改后重试。"

        exc_class = self._error_mapping.get(code, VetMewError)
        raise exc_class(code, msg)

    def _generate_nonce(self, length=8):
        """生成 8 位随机字符串"""
        return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

    def _generate_signature(self, path, body_str, nonce, timestamp):
        """生成 HMAC-SHA256 签名"""
        to_sign = f"{path}{body_str}{nonce}{timestamp}"
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            to_sign.encode('utf-8'),
            hashlib.sha256
        ).digest()
        return base64.b64encode(signature).decode('utf-8')

    def request_sse(self, path, payload):
        """发起 SSE 流式请求"""
        url = f"{self.base_url}{path}"
        
        # 必须是紧凑的 JSON 字符串 (无空格)
        body_str = json.dumps(payload, separators=(',', ':'), ensure_ascii=False)
        timestamp = str(int(time.time()))
        nonce = self._generate_nonce()
        signature = self._generate_signature(path, body_str, nonce, timestamp)

        headers = {
            "X-ApiKey": self.api_key,
            "X-Timestamp": timestamp,
            "X-Nonce": nonce,
            "X-Signature": signature,
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(url, headers=headers, data=body_str.encode('utf-8'), stream=True, timeout=30)
            
            # 检查响应类型
            content_type = response.headers.get("Content-Type", "")
            if "application/json" in content_type:
                # 即使是 200，如果 Content-Type 是 JSON，也可能是同步返回的错误信息
                self._handle_error_response(response.json())
            
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            if e.response is not None and "application/json" in e.response.headers.get("Content-Type", ""):
                self._handle_error_response(e.response.json())
            raise VetMewError(0, f"网络请求失败: {e}")

    def stream_response(self, response):
        """解析 SSE 流式响应并按行产生 JSON 数据"""
        if not response:
            return

        try:
            for line in response.iter_lines():
                if not line:
                    continue
                
                line_str = line.decode('utf-8')
                if line_str.startswith("data: "):
                    data_str = line_str[6:].strip()
                    if data_str == "[DONE]":
                        break
                    try:
                        yield json.loads(data_str)
                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            raise VetMewError(0, f"流式响应解析中断: {e}")
