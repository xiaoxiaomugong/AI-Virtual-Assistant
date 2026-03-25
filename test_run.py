from rag import RagService
import config_data as config

print("Initializing RagService...")
rag = RagService()
print("Invoking chain...")
try:
    for chunk in rag.chain.stream({"input": "你好"}, config.session_config):
        print(chunk, end="", flush=True)
except Exception as e:
    import traceback
    traceback.print_exc()
