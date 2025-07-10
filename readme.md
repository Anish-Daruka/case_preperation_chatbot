
# 💼 Case Interview Assistant

A smart case interview preparation assistant built on custom dataset. It combines LangChain, LangGraph, Qdrant, and Streamlit to create an interactive and memory-efficient chatbot for business case practice.

---

## ⚙️ Setup Instructions

Follow these steps to set up the Case Interview Assistant project locally on your machine:

### 1. ✅ Clone the Repository

```bash
git clone https://github.com/your-username/case-interview-assistant.git
cd case-interview-assistant
```

### 2. 🐍 Set Up a Virtual Environment (Recommended)

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. 📦 Install Required Dependencies

```bash
pip install -r requirements.txt
```

### 4. 🔐 Add Environment Variables

Create a `.env` file in the root directory with the following content:

```env
GOOGLE_API_KEY=your_google_genai_key_here
```

Get your key from https://makersuite.google.com/app/apikey

### 5. 🚀 Run Qdrant (Vector Database)

Start Qdrant locally using Docker:

```bash
docker run -p 6333:6333 qdrant/qdrant
```

### 6. 📁 Add Your Case Prep PDFs

Place all PDF resources inside the `case_prep_resources/` directory. Use filenames that include `case`, `framework`, or `guesstimate`.

### 7. 🧠 Vectorize and Upload to Qdrant

```bash
python vector_db.py
```

This script:
- Extracts and chunks text from PDFs
- Embeds them using Sentence Transformers
- Uploads them to Qdrant

### 8. 💬 Launch the Assistant

```bash
streamlit run app.py
```

Open in your browser at `http://localhost:8501`.

---

## ▶️ App Demo

### Screenshot 1: Startup and Welcome Prompt
![Screenshot 1](screenshots/screenshot1.png)

### Screenshot 2: Framework Explanation Response
![Screenshot 2](screenshots/screenshot2.png)

### Screenshot 3: Interactive Case Simulation
![Screenshot 3](screenshots/screenshot3.png)

### Screenshot 4: RAG-backed Market Insight
![Screenshot 4](screenshots/screenshot4.png)

### Screenshot 5: Follow-up Reasoning
![Screenshot 5](screenshots/screenshot5.png)

---

## 📝 Features

- ✅ Semantic Search via SentenceTransformers + Qdrant
- 🧠 Conversational Memory using summarization
- 📚 Handles frameworks, guesstimates, case books
- 💬 ChatGPT-style UI built with Streamlit
- 🪄 Intent routing and adaptive RAG

---

## 📂 Project Structure

```
├── app.py                  # Streamlit app
├── case_prep.py            # LangGraph workflow
├── vector_db.py            # PDF embedding + upload
├── case_prep_resources/    # Raw PDFs
├── requirements.txt
└── README.md
```

---

## 🧪 Coming Soon

- Feedback node for response rating
- User session saving
- Interview simulation flow

---

## 📧 Contact

Feel free to reach out via [LinkedIn](https://linkedin.com/in/yourprofile) or open an issue!

---

MIT License • Built with ❤️
