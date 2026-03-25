from knowledge_base import KnowledgeBaseService
kb = KnowledgeBaseService()
kb.upload_file("Hello world, this is a test.", "test.txt")
print("Done.")
docs = kb.chorma.similarity_search("Hello world")
print("Found docs in kb:", len(docs))
