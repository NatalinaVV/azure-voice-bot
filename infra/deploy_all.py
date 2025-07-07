import os
import json
import subprocess
from pathlib import Path

from dotenv import set_key

# === Настройки по умолчанию ===
RESOURCE_GROUP = "voicebot-rg"
LOCATION = "westeurope"
SEARCH_SERVICE = "voicebotsearch"
OPENAI_NAME = "voicebotopenai"
DEPLOYMENT_NAME = "embedding-model"
INDEX_NAME = "knowledge-index"
ENV_PATH = Path(__file__).parent.parent / ".env"
LOCAL_SETTINGS_PATH = Path(__file__).parent.parent / "local.settings.json"


def run_az(command: list) -> dict:
    result = subprocess.run(["az"] + command + ["--output", "json"], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        raise Exception("Azure CLI error")
    return json.loads(result.stdout)


def create_resource_group():
    print("🔧 Creating resource group...")
    run_az(["group", "create", "--name", RESOURCE_GROUP, "--location", LOCATION])


def create_openai():
    print("🧠 Creating Azure OpenAI resource...")
    run_az([
        "cognitiveservices", "account", "create",
        "--name", OPENAI_NAME,
        "--resource-group", RESOURCE_GROUP,
        "--kind", "OpenAI",
        "--sku", "S0",
        "--location", LOCATION,
        "--yes"
    ])

    keys = run_az([
        "cognitiveservices", "account", "keys", "list",
        "--name", OPENAI_NAME,
        "--resource-group", RESOURCE_GROUP
    ])
    endpoint = run_az([
        "cognitiveservices", "account", "show",
        "--name", OPENAI_NAME,
        "--resource-group", RESOURCE_GROUP
    ])["properties"]["endpoint"]

    return keys["key1"], endpoint


def create_search():
    print("🔍 Creating Azure Cognitive Search service...")
    run_az([
        "search", "service", "create",
        "--name", SEARCH_SERVICE,
        "--resource-group", RESOURCE_GROUP,
        "--location", LOCATION,
        "--sku", "free"
    ])

    keys = run_az([
        "search", "admin-key", "show",
        "--service-name", SEARCH_SERVICE,
        "--resource-group", RESOURCE_GROUP
    ])
    endpoint = f"https://{SEARCH_SERVICE}.search.windows.net"

    return keys["primaryKey"], endpoint


def update_env_and_settings(env_vars: dict):
    print("✍️ Update .env и local.settings.json...")

    # Обновляем .env
    for key, value in env_vars.items():
        set_key(str(ENV_PATH), key, value)

    # Обновляем или создаём local.settings.json аккуратно
    local_settings = {"IsEncrypted": False, "Values": {}}
    if LOCAL_SETTINGS_PATH.exists():
        with open(LOCAL_SETTINGS_PATH) as f:
            try:
                local_settings = json.load(f)
            except json.JSONDecodeError:
                print("⚠️ Warning: file local.settings.json was broke, created the new one")

    # Объединение переменных
    local_settings["Values"] = {
        **local_settings.get("Values", {}),
        **env_vars
    }

    with open(LOCAL_SETTINGS_PATH, "w") as f:
        json.dump(local_settings, f, indent=2)



def main():
    create_resource_group()
    openai_key, openai_endpoint = create_openai()
    search_key, search_endpoint = create_search()

    env_vars = {
        "AZURE_OPENAI_KEY": openai_key,
        "AZURE_OPENAI_ENDPOINT": openai_endpoint,
        "AZURE_SEARCH_KEY": search_key,
        "AZURE_SEARCH_ENDPOINT": search_endpoint,
        "AZURE_SEARCH_INDEX": INDEX_NAME,
        "OPENAI_EMBEDDING_MODEL": "text-embedding-3-small"
    }

    update_env_and_settings(env_vars)
    print("✅ All resource were created.")


if __name__ == "__main__":
    main()
