import anthropic
client = anthropic.Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key="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",
)
message = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1000,
    temperature=0.0,
    system="Respond only in Yoda-speak.",
    messages=[
        {"role": "user", "content": "How are you today?"}
    ]
)

print(message.content[0].text)
