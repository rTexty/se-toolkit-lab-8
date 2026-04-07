import sys
target = "qwen-code-api/src/qwen_code_api/models.py"

with open(target, "r") as f:
    content = f.read()

old_code = """
def resolve_model(model: str) -> str:
    return MODEL_ALIASES.get(model, model) or settings.default_model
"""

new_code = """
def resolve_model(model: str) -> str:
    # Force everything to use the default openrouter model
    return settings.default_model
"""

content = content.replace(old_code.strip(), new_code.strip())

with open(target, "w") as f:
    f.write(content)
