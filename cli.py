"""
Sentiment Analyzer — Command Line Interface
Usage: python cli.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from app.sentiment_engine import SentimentAnalyzer


def print_banner():
    print("\n" + "="*55)
    print("   🧠  SENTIMENT ANALYZER  — CLI v1.0.0")
    print("="*55)
    print("   Bahasa: Indonesia & English")
    print("   Ketik 'quit' untuk keluar | 'stats' untuk statistik")
    print("="*55 + "\n")


def print_result(r: dict):
    label_colors = {
        "POSITIF": "\033[92m", "POSITIVE": "\033[92m",
        "NEGATIF": "\033[91m", "NEGATIVE": "\033[91m",
        "NETRAL":  "\033[93m", "NEUTRAL":  "\033[93m"
    }
    RESET = "\033[0m"
    BOLD  = "\033[1m"

    color = label_colors.get(r["label"], "")
    conf  = int(r["confidence"] * 100)
    lang  = "Indonesia" if r["language"] == "id" else "English"

    print(f"\n  Hasil      : {BOLD}{color}{r['emoji']} {r['label']}{RESET}")
    print(f"  Kepercayaan: {conf}%")
    print(f"  Bahasa     : {lang}")
    print(f"  Skor +/-   : {r['positive_score']:.1f} / {r['negative_score']:.1f}")

    if r["matched_positive"]:
        print(f"  Kata (+)   : {', '.join(r['matched_positive'])}")
    if r["matched_negative"]:
        print(f"  Kata (-)   : {', '.join(r['matched_negative'])}")

    # Visual bar
    total = r["positive_score"] + r["negative_score"]
    if total > 0:
        pos_w = int(r["positive_score"] / total * 30)
        neg_w = 30 - pos_w
        bar = "\033[92m" + "█" * pos_w + RESET + "\033[91m" + "█" * neg_w + RESET
        print(f"\n  [{bar}]")
    print()


def main():
    print_banner()
    analyzer = SentimentAnalyzer()

    while True:
        try:
            text = input("  Masukkan teks: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n  Sampai jumpa! 👋\n")
            break

        if not text:
            continue

        if text.lower() == "quit":
            print("\n  Sampai jumpa! 👋\n")
            break

        if text.lower() == "stats":
            stats = analyzer.get_stats()
            if "message" in stats:
                print(f"\n  {stats['message']}\n")
            else:
                print(f"\n  Total Analisis : {stats['total_analyzed']}")
                print(f"  Distribusi     : {stats['distribution']}")
                print(f"  Rata Kepercayaan: {stats['average_confidence']*100:.0f}%\n")
            continue

        result = analyzer.analyze(text)
        if "error" in result:
            print(f"\n  ⚠️  {result['error']}\n")
        else:
            print_result(result)


if __name__ == "__main__":
    main()
