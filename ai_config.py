CLAUDE_MODEL="claude-3-haiku-20240307"
SYSTEM_PROMPT="You are a helpful SEO assistant that generates blog topics and parses out the products discussed from a given transcript."


def analyze_transcript_function(id: str, blog_topics: list, products: list):
    print(f"ID: {id}")
    print(f"Blog Topics: {blog_topics}")
    print(f"Products: {products}")