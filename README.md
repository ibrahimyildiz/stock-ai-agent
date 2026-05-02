# 🚀 Stock AI Agent

An **AI-powered financial intelligence system** that uses RAG (Retrieval-Augmented Generation), vector databases, and LLM agents to analyze stock news and generate investment insights.

---

## 🧠 Overview

This project is a production-style **AI stock recommendation system** built with:

* FastAPI backend
* Ollama LLM integration
* ChromaDB vector database
* RAG pipeline (Retrieval-Augmented Generation)
* Multi-step ranking system
* Dockerized microservices architecture

The system ingests financial news, stores embeddings in a vector database, retrieves relevant context, ranks results, and generates AI-driven responses.

---

## ⚙️ Architecture

```text
User Query
   ↓
FastAPI
   ↓
Ticker Extraction (Entity Resolver)
   ↓
ChromaDB Retrieval
   ↓
Ranking Layer
   ↓
Ollama LLM (Response Generation)
   ↓
Final Answer
```

---

## 🚀 Features

* 📊 Stock news ingestion (AlphaVantage API)
* 🧠 RAG-based retrieval system
* 🔍 Metadata filtering (ticker-based search)
* ⚡ Custom ranking system (recency + relevance)
* 🤖 Ollama LLM integration
* 🧩 Modular service architecture
* 🐳 Dockerized multi-service setup
* 🧪 Debug endpoints for retrieval inspection

---

## 🧰 Tech Stack

* Python 3.10+
* FastAPI
* ChromaDB
* Ollama (LLM)
* Sentence Transformers
* Docker & Docker Compose
* REST APIs

---

## 📡 API Endpoints

### 🔹 Chat

```http
POST /chat?query=Apple earnings
```

### 🔹 Ingest News

```http
POST /ingest
```

### 🔹 Stock Recommendation

```http
GET /recommend?q=Tesla news
```

### 🔹 Debug Retrieval

```http
GET /debug/retrieval?query=Apple earnings
```

---

## 🧪 How to Run

```bash
docker compose up --build
```

Then open:

```text
http://localhost:8000/docs
```

---

## 📦 Current Status

* ✅ RAG pipeline working
* ✅ Vector DB persistence (Chroma)
* ✅ Basic ranking system implemented
* ⚠️ Entity extraction needs improvement
* ⚠️ Retrieval filtering being improved
* 🚧 Moving toward agent-based architecture

---

## 🧭 Roadmap

* Hybrid retrieval (BM25 + Vector search)
* LangGraph-based multi-agent system
* Intelligent ticker/entity resolution
* Financial reasoning layer
* Portfolio-level recommendation agent
* Evaluation & backtesting system

---

## 🧠 Goal

To build a **production-grade AI financial assistant** capable of:

* Understanding financial queries
* Retrieving relevant market data
* Reasoning over news & signals
* Generating actionable insights
