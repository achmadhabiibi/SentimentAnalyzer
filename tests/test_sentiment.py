"""
Unit Tests for Sentiment Analyzer Engine
Run with: pytest tests/ -v
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.sentiment_engine import SentimentAnalyzer


def setup_function():
    global analyzer
    analyzer = SentimentAnalyzer()


# ─── Language Detection ───────────────────────────────────────────────────────

def test_detect_language_id():
    lang = analyzer.detect_language("Saya sangat senang hari ini")
    assert lang == "id"

def test_detect_language_en():
    lang = analyzer.detect_language("I am very happy today")
    assert lang == "en"


# ─── Indonesian Sentiment ─────────────────────────────────────────────────────

def test_positive_id():
    result = analyzer.analyze("Saya sangat senang dan bahagia hari ini!", "id")
    assert result["label"] == "POSITIF"
    assert result["positive_score"] > 0

def test_negative_id():
    result = analyzer.analyze("Saya merasa sedih dan kecewa sekali", "id")
    assert result["label"] == "NEGATIF"
    assert result["negative_score"] > 0

def test_neutral_id():
    result = analyzer.analyze("Hari ini cuaca cerah", "id")
    assert result["label"] == "NETRAL"

def test_negation_id():
    result = analyzer.analyze("Saya tidak senang dengan hasilnya", "id")
    # negated positive → should lean negative or neutral
    assert result["label"] in ["NEGATIF", "NETRAL"]

def test_intensifier_id():
    result1 = analyzer.analyze("Saya senang", "id")
    result2 = analyzer.analyze("Saya sangat senang", "id")
    assert result2["positive_score"] >= result1["positive_score"]


# ─── English Sentiment ────────────────────────────────────────────────────────

def test_positive_en():
    result = analyzer.analyze("I am very happy and excited!", "en")
    assert result["label"] == "POSITIVE"

def test_negative_en():
    result = analyzer.analyze("This is terrible and awful", "en")
    assert result["label"] == "NEGATIVE"


# ─── Bulk Analysis ───────────────────────────────────────────────────────────

def test_bulk_analysis():
    texts = [
        "Saya sangat senang!",
        "Hari ini sangat membosankan.",
        "Cuacanya biasa saja."
    ]
    result = analyzer.analyze_bulk(texts, "id")
    assert result["total"] == 3
    assert "results" in result
    assert "summary" in result


# ─── Edge Cases ───────────────────────────────────────────────────────────────

def test_empty_text():
    result = analyzer.analyze("")
    assert "error" in result

def test_special_chars():
    result = analyzer.analyze("!!! ???", "id")
    assert "label" in result

def test_stats():
    analyzer.analyze("Saya senang", "id")
    analyzer.analyze("Saya sedih", "id")
    stats = analyzer.get_stats()
    assert stats["total_analyzed"] >= 2
