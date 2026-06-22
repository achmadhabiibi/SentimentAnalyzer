# 🧠 Sentiment Analyzer

**AI-powered Indonesian & English Sentiment Analysis** — REST API + Web UI + CLI

> Project ini cocok untuk portofolio CV sebagai bukti kemampuan membangun sistem NLP end-to-end.

---

## ✨ Fitur Utama

| Fitur | Keterangan |
|-------|------------|
| 🌐 REST API | FastAPI dengan auto-docs (`/docs`) |
| 💻 Web UI | Dashboard interaktif di browser |
| 🖥️ CLI | Antarmuka terminal berwarna |
| 🌏 Bilingual | Bahasa Indonesia & English |
| 🔁 Bulk Analysis | Analisis banyak teks sekaligus |
| 🧪 Unit Tests | Pytest siap jalan |
| 📊 Statistik | Distribusi & confidence score |

---

## 🚀 Cara Menjalankan

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Jalankan API + Web UI
```bash
python api.py
```
Buka browser: **http://localhost:8000**
API Docs: **http://localhost:8000/docs**

### 3. Jalankan CLI (terminal)
```bash
python cli.py
```

### 4. Jalankan Tests
```bash
pytest tests/ -v
```

---

## 📡 API Endpoints

| Method | Endpoint | Keterangan |
|--------|----------|------------|
| GET | `/` | Web UI |
| GET | `/health` | Status API |
| POST | `/analyze` | Analisis satu teks |
| POST | `/analyze/bulk` | Analisis banyak teks |
| GET | `/stats` | Statistik sesi |
| GET | `/history` | Riwayat analisis |

### Contoh Request
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "Saya sangat senang!", "language": "auto"}'
```

### Contoh Response
```json
{
  "text": "Saya sangat senang!",
  "language": "id",
  "label": "POSITIF",
  "emoji": "😊",
  "positive_score": 1.5,
  "negative_score": 0.0,
  "confidence": 1.0,
  "matched_positive": ["senang"],
  "matched_negative": [],
  "word_count": 4
}
```

---

## 🗂️ Struktur Project

```
sentiment-analyzer/
├── api.py                  # FastAPI server (entry point)
├── cli.py                  # Terminal interface
├── requirements.txt
├── README.md
├── app/
│   └── sentiment_engine.py # Core NLP engine
├── templates/
│   └── index.html          # Web UI
└── tests/
    └── test_sentiment.py   # Unit tests
```

---

## 🧩 Teknologi

- **FastAPI** — Modern Python web framework
- **Uvicorn** — ASGI server
- **Pydantic** — Data validation
- **Pytest** — Unit testing
- **Vanilla JS** — Frontend UI (no framework needed)

---

## 💡 Cara Explain di CV / Interview

> *"Saya membangun REST API sentiment analysis berbahasa Indonesia menggunakan FastAPI dan rule-based NLP. Project ini memiliki fitur bilingual detection, negation handling, intensifier scoring, bulk analysis endpoint, dan dilengkapi unit tests. Bisa diakses via Web UI, REST API, maupun CLI."*

---

## 🔭 Pengembangan Selanjutnya (Ideas)

- [ ] Integrasi model ML (scikit-learn / transformers)
- [ ] Database (PostgreSQL) untuk simpan history
- [ ] Docker containerization
- [ ] Deploy ke cloud (Railway / Render / VPS)
- [ ] Analisis sentimen dari file CSV/Excel upload
