def build_prompt(topic, tone):
    
    prompt = f"""
    Write a structured blog post.

    Topic: {topic}
    Tone: {tone}

    Output format:

    Title:
    Introduction:
    Key Points:
    1.
    2.
    3.

    Conclusion:
    Call To Action:
    """

    return prompt