def categorize_article(content):
    """
    Categorize the article based on keywords in its content.
    
    content: Text content of the article.
    Returns: Article category.
    """
    categories = {
        "Investing": ["stocks", "investing", "portfolio", "wealth"],
        "Savings": ["savings", "budget", "emergency fund"],
        "Loans": ["loans", "mortgage", "debt", "credit"],
    }
    
    for category, keywords in categories.items():
        if any(keyword in content.lower() for keyword in keywords):
            return category
    return "Uncategorized"


