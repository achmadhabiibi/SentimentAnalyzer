"""
Sentiment Analysis Engine
Supports Indonesian and English text analysis
"""

import re
import json
import os
from datetime import datetime
from collections import Counter


# ─── Lexicon Data ───────────────────────────────────────────────────────────────

LEXICON_ID = {
    "positive": [
        # Emosi dasar positif
        "senang", "suka", "bahagia", "gembira", "puas", "bangga", "cinta",
        "kagum", "hebat", "luar biasa", "mantap", "keren", "bagus", "indah",
        "menyenangkan", "bersyukur", "optimis", "bersemangat", "antusias",
        "percaya", "berhasil", "sukses", "memuaskan", "terbaik", "setuju",
        "mendukung", "nyaman", "aman", "stabil", "damai", "tentram",
        # Slang & gaul positif
        "gokil", "gilak", "kece", "top", "joss", "sick", "wih", "wah",
        "sip", "oke", "asik", "asyk", "seru", "lucu", "gemoy", "cute",
        "adorable", "sweet", "manis", "cakep", "cantik", "ganteng", "tampan",
        "smart", "pinter", "jenius",
        # Relasi & sosial positif
        "solid", "kompak", "akrab", "hangat", "peduli", "perhatian", "sayang",
        "setia", "tulus", "jujur", "amanah", "baik", "ramah", "sopan",
        "pengertian", "suportif", "supportif", "membantu",
        # Prestasi & kerja positif
        "produktif", "kreatif", "inovatif", "profesional", "rajin", "tekun",
        "disiplin", "gigih", "semangat", "termotivasi", "inspiratif",
        "memotivasi", "menginspirasi",
        # Situasi positif
        "membaik", "meningkat", "berkembang", "maju", "tumbuh",
        "lolos", "lulus", "diterima", "menang", "juara", "promosi", "naik",
        "rezeki", "berkah", "untung", "profit", "cuan",
        # Kesehatan & wellbeing
        "sehat", "bugar", "segar", "fit", "sembuh", "pulih", "istirahat",
        "rileks", "santai", "tenang",
    ],
    "negative": [
        # Emosi dasar negatif
        "sedih", "bosan", "benci", "marah", "kecewa", "kesal", "frustrasi",
        "lelah", "capek", "susah", "sulit", "buruk", "jelek", "gagal",
        "takut", "khawatir", "stress", "tertekan", "hancur", "rugi",
        "mengecewakan", "menyebalkan", "menyedihkan", "menyesal",
        "mengerikan", "menakutkan", "parah", "ancaman", "bahaya", "kerugian",
        # Perilaku toxic dan manipulatif
        "toxic", "manipulatif", "manipulasi", "gaslighting", "ghosting",
        "playing victim", "drama", "munafik", "bohong", "dusta",
        "khianat", "pengkhianat", "selingkuh", "tipu", "menipu", "curang",
        "egois", "narsis", "narsistik", "posesif", "mengontrol",
        "intimidasi", "mengintimidasi", "bully", "bullying",
        "pelecehan", "merendahkan", "menghina", "menghujat",
        # Slang & gaul negatif
        "nyebelin", "cringe", "lebay", "alay", "norak",
        "memalukan", "ngeselin", "bikin emosi",
        "bikin kesel", "annoying", "mengganggu", "ribet",
        "ruwet", "pusing", "mumet", "bete", "sebel", "sebal",
        # Situasi dan kondisi buruk
        "kalah", "bangkrut", "hutang", "masalah",
        "kacau", "berantakan", "amburadul",
        "menyusahkan", "mempersulit", "menghambat", "menghalangi",
        # Hubungan toxic
        "putus", "cerai", "pisah", "ditinggal", "dikhianati", "ditipu",
        "dimanfaatkan", "dipermainkan", "disakiti", "dilukai", "diremehkan",
        "diabaikan", "dikucilkan", "diisolasi", "dijauhi",
        # Kesehatan mental negatif
        "depresi", "anxiety", "cemas", "panik", "trauma",
        "insomnia", "burnout", "overwhelmed", "hopeless", "putus asa",
        "menyerah", "tidak berdaya", "worthless",
        # Kritik dan penilaian negatif
        "payah", "bodoh", "idiot", "dungu", "bego",
        "tidak kompeten", "tidak becus", "tidak bertanggung jawab",
        "pemalas", "males", "tidak disiplin",
    ],
    "negation": [
        "tidak", "bukan", "jangan", "tanpa", "belum", "tak",
        "enggak", "nggak", "gak", "ga"
    ],
    "intensifier": {
        "sangat": 1.5, "amat": 1.5, "sekali": 1.3, "banget": 1.3,
        "terlalu": 1.2, "begitu": 1.2, "sungguh": 1.4, "benar-benar": 1.5,
        "beneran": 1.3, "parah": 1.4, "gila": 1.4, "gilak": 1.4,
        "super": 1.5, "ultra": 1.5, "ekstrem": 1.4,
        "abis": 1.2, "bgt": 1.3, "poll": 1.3, "pol": 1.2
    }
}

LEXICON_EN = {
    "positive": [
        # Basic positive emotions
        "happy", "joy", "love", "great", "excellent", "good", "wonderful",
        "amazing", "fantastic", "awesome", "brilliant", "pleased", "satisfied",
        "glad", "cheerful", "delighted", "grateful", "excited", "optimistic",
        "confident", "successful", "perfect", "beautiful", "nice", "positive",
        # Social & relationship positive
        "supportive", "caring", "kind", "generous", "loyal", "honest",
        "trustworthy", "reliable", "helpful", "friendly", "warm", "genuine",
        "sincere", "compassionate", "empathetic", "respectful",
        # Achievement positive
        "productive", "creative", "innovative", "professional", "hardworking",
        "disciplined", "motivated", "inspiring", "talented", "skilled",
        # Situation positive
        "improving", "growing", "thriving", "winning", "succeeding",
        "progressing", "advancing", "recovering", "healing",
        # Slang positive
        "lit", "fire", "goat", "legend", "vibe", "vibing", "blessed",
        "slay", "slaying", "iconic", "based", "valid", "wholesome",
    ],
    "negative": [
        # Basic negative emotions
        "sad", "hate", "bad", "terrible", "awful", "horrible", "poor",
        "disgusting", "angry", "frustrated", "disappointed", "bored", "tired",
        "worried", "stressed", "failed", "loss", "painful", "miserable",
        "unhappy", "depressed", "confused", "helpless", "hopeless", "fearful",
        # Toxic behaviors
        "toxic", "manipulative", "manipulating", "gaslighting", "ghosting",
        "narcissistic", "controlling", "possessive", "abusive", "cheating",
        "lying", "deceiving", "betraying", "bullying", "harassing",
        "humiliating", "belittling", "insulting", "mocking", "degrading",
        # Negative slang
        "cringe", "trash", "garbage", "pathetic", "lame", "annoying",
        "irritating", "infuriating", "disgusting", "repulsive", "awful",
        # Mental health negative
        "anxiety", "panic", "trauma", "burnout", "overwhelmed",
        "worthless", "hopeless", "giving up", "broken",
        # Relationship negative
        "betrayed", "cheated", "abandoned", "ignored", "rejected",
        "used", "manipulated", "isolated", "excluded",
    ],
    "negation": ["not", "no", "never", "without", "cannot", "can't", "don't", "won't", "neither", "nor"],
    "intensifier": {
        "very": 1.5, "extremely": 1.8, "really": 1.3, "absolutely": 1.6,
        "totally": 1.4, "completely": 1.4, "so": 1.2, "too": 1.1,
        "insanely": 1.6, "incredibly": 1.6, "ridiculously": 1.5,
        "super": 1.4, "ultra": 1.5, "beyond": 1.4, "deeply": 1.3
    }
}


# ─── Analysis Engine ─────────────────────────────────────────────────────────

class SentimentAnalyzer:
    def __init__(self):
        self.lexicons = {"id": LEXICON_ID, "en": LEXICON_EN}
        self.history = []

    def detect_language(self, text: str) -> str:
        text_lower = text.lower()
        id_markers = ["yang", "dan", "di", "ke", "aku", "saya", "kamu", "ini", "itu", "ada", "gak", "nggak", "banget", "dong"]
        en_markers = ["the", "and", "is", "are", "you", "i", "this", "that", "it", "in", "my", "me", "was"]
        id_count = sum(1 for w in id_markers if f" {w} " in f" {text_lower} ")
        en_count = sum(1 for w in en_markers if f" {w} " in f" {text_lower} ")
        return "id" if id_count >= en_count else "en"

    def preprocess(self, text: str) -> list:
        text = text.lower()
        text = re.sub(r"[^\w\s]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text.split()

    def analyze(self, text: str, language: str = "auto") -> dict:
        if not text or not text.strip():
            return {"error": "Input teks tidak boleh kosong."}

        if language == "auto":
            language = self.detect_language(text)

        lexicon = self.lexicons.get(language, LEXICON_ID)
        tokens = self.preprocess(text)

        pos_score = 0.0
        neg_score = 0.0
        matched_positive = []
        matched_negative = []

        # Also check bigrams (2-word phrases) like "tidak becus", "playing victim"
        bigrams = [tokens[i] + " " + tokens[i+1] for i in range(len(tokens)-1)]

        for phrase in bigrams:
            if phrase in lexicon["positive"]:
                pos_score += 1.0
                matched_positive.append(phrase)
            elif phrase in lexicon["negative"]:
                neg_score += 1.0
                matched_negative.append(phrase)

        for i, token in enumerate(tokens):
            multiplier = 1.0
            if i > 0 and tokens[i - 1] in lexicon["intensifier"]:
                multiplier = lexicon["intensifier"][tokens[i - 1]]

            negated = any(
                tokens[j] in lexicon["negation"]
                for j in range(max(0, i - 2), i)
            )

            if token in lexicon["positive"]:
                score = 1.0 * multiplier
                if negated:
                    neg_score += score * 0.8
                    matched_negative.append(f"~{token}")
                else:
                    pos_score += score
                    matched_positive.append(token)

            elif token in lexicon["negative"]:
                score = 1.0 * multiplier
                if negated:
                    pos_score += score * 0.5
                    matched_positive.append(f"~{token}")
                else:
                    neg_score += score
                    matched_negative.append(token)

        total = pos_score + neg_score
        confidence = round(abs(pos_score - neg_score) / (total + 1e-9), 2)

        if pos_score > neg_score:
            label = "POSITIF" if language == "id" else "POSITIVE"
            emoji = "😊"
        elif neg_score > pos_score:
            label = "NEGATIF" if language == "id" else "NEGATIVE"
            emoji = "😔"
        else:
            label = "NETRAL" if language == "id" else "NEUTRAL"
            emoji = "😐"

        result = {
            "text": text,
            "language": language,
            "label": label,
            "emoji": emoji,
            "positive_score": round(pos_score, 2),
            "negative_score": round(neg_score, 2),
            "confidence": confidence,
            "matched_positive": list(set(matched_positive)),
            "matched_negative": list(set(matched_negative)),
            "word_count": len(tokens),
            "analyzed_at": datetime.now().isoformat()
        }

        self.history.append(result)
        return result

    def analyze_bulk(self, texts: list, language: str = "auto") -> dict:
        results = [self.analyze(t, language) for t in texts if t.strip()]
        labels = [r["label"] for r in results if "label" in r]
        counter = Counter(labels)
        return {
            "total": len(results),
            "results": results,
            "summary": dict(counter),
            "analyzed_at": datetime.now().isoformat()
        }

    def get_stats(self) -> dict:
        if not self.history:
            return {"message": "Belum ada data analisis."}
        labels = [r["label"] for r in self.history]
        counter = Counter(labels)
        avg_conf = sum(r["confidence"] for r in self.history) / len(self.history)
        return {
            "total_analyzed": len(self.history),
            "distribution": dict(counter),
            "average_confidence": round(avg_conf, 2),
            "languages_used": list(set(r["language"] for r in self.history))
        }
