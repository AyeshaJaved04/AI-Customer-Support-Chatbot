from app.services.sentiment_service import SentimentAnalyzer

def test_empty_text():
    """Empty text should return neutral sentiment"""
    analyzer = SentimentAnalyzer()
    result = analyzer.analyze("")
    assert result["category"] == "neutral"
    assert result["score"] == 0.5

def test_empty_spaces():
    """Whitespace only should return neutral"""
    analyzer = SentimentAnalyzer()
    result = analyzer.analyze("   ")
    assert result["category"] == "neutral"

def test_score_range():
    """Score should always be between 0 and 1"""
    analyzer = SentimentAnalyzer()
    for text in ["good", "bad", "ok", "hello"]:
        result = analyzer.analyze(text)
        assert 0 <= result["score"] <= 1

def test_result_has_all_keys():
    """Result should contain label, score, and category"""
    analyzer = SentimentAnalyzer()
    result = analyzer.analyze("test message")
    assert "label" in result
    assert "score" in result
    assert "category" in result

def test_category_values():
    """Category should be one of the valid values"""
    analyzer = SentimentAnalyzer()
    valid = ["positive", "negative", "neutral", "urgent"]
    result = analyzer.analyze("I need help")
    assert result["category"] in valid