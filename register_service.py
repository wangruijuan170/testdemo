import requests
import base64
import configparser
import os

# 读取配置
config = configparser.ConfigParser()
config.read("config.ini", encoding="utf-8")

# 解析 `config.ini` 参数
APP_NAME = config["app"]["name"]
APP_VERSION = config["app"]["version"]
APP_TITLE = config["app"]["title"]
APP_DESCRIPTION = config["app"]["description"]
APP_LOGO = config["app"]["logo"]
APP_BASE_URL = config["app"]["base_url"]

APP_PING_URL = config["api"]["ping_url"]
APP_DIAG_URL = config["api"]["diag_url"]
APP_REREG_URL = config["api"]["rereg_url"]

GAIS_HOST = config["gais"]["host"]
GAIS_PORT = config["gais"]["port"]
GAIS_PROTOCOL = config["gais"]["protocol"]
GAIS_TOKEN = config["gais"]["token"]

GAIS_SERVER = f"http://{GAIS_HOST}:{GAIS_PORT}"


def to_b64(file_path):
    """将图片转换为 Base64 编码"""
    if not os.path.exists(file_path):
        return None
    with open(file_path, "rb") as image:
        data = base64.b64encode(image.read())
    return f"data:image/png;base64,{data.decode('utf-8')}"


def register():
    """向 GAIS 服务器注册应用"""
    print("Registering app...")
    try:
        response = requests.post(
            f"{GAIS_SERVER}/api/apps/register",
            headers={"Authorization": f"Bearer {GAIS_TOKEN}"},
            json={
                "protocol": GAIS_PROTOCOL,
                "properties": {
                    "name": APP_NAME,
                    "version": APP_VERSION,
                    "title": APP_TITLE,
                    "description": APP_DESCRIPTION,
                    "logo": to_b64(APP_LOGO),
                    "url": APP_BASE_URL,
                    "ping": APP_PING_URL,
                    "diagnosis": APP_DIAG_URL,
                    "reregister": APP_REREG_URL,
                },
                "resources": ["ollama"],
            },
        )
        data = response.json()
        if response.status_code != 200:
            print(f"Failed to register app: {data.get('error', 'Unknown error')}")
        else:
            print("App registered successfully!")
    except Exception as e:
        print(f"Registration failed: {e}")


def unregister():
    """注销应用"""
    print("Unregistering app...")
    try:
        requests.delete(
            f"{GAIS_SERVER}/api/apps/register/{APP_NAME}",
            headers={"Authorization": f"Bearer {GAIS_TOKEN}"},
        )
        print("App unregistered successfully")
    except Exception as e:
        print(f"Unregistration failed: {e}")
