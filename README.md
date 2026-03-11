# 🤖 AI Job Matching Agent

An **AI-powered job recommendation system** that analyzes a candidate's resume and matches it with the most relevant job descriptions using **semantic embeddings and vector similarity search**.

The system extracts skills from resumes, converts both resumes and job descriptions into **vector embeddings**, and performs **semantic search using a vector database** to recommend the most suitable jobs.

---

# 📌 Project Overview

Recruiters often manually compare resumes with job descriptions. This project automates that process using **Natural Language Processing (NLP)** and **Vector Similarity Search**.

The pipeline:

Resume → Text Extraction → Skill Extraction → Embedding Generation → Vector Search → Job Recommendations

The system identifies relevant job roles by comparing the **semantic similarity between resume embeddings and job description embeddings**.

---

# ⚙️ System Architecture

```
Resume Upload (PDF / TXT)
        │
        ▼
Resume Text Extraction
        │
        ▼
Skill Extraction (NLP)
        │
        ▼
Generate Embeddings
(Sentence Transformers)
        │
        ▼
Vector Database (Supabase)
        │
        ▼
Similarity Search
        │
        ▼
Top Job Recommendations
(Streamlit UI)
```

---

# ✨ Features

* 📄 Upload Resume (PDF or TXT)
* 🔍 Automatic Resume Text Extraction
* 🧠 NLP-based Skill Extraction
* 🔗 Embedding Generation using Sentence Transformers
* 📊 Semantic Vector Search with Supabase
* 💼 AI-powered Job Recommendations
* 🖥️ Interactive UI using Streamlit

---

# 🛠 Tech Stack

### Programming

* Python

### Machine Learning / NLP

* Sentence Transformers
* NLP-based skill extraction

### Database

* Supabase Vector Database
* pgvector similarity search

### Framework

* Streamlit (for UI)

### LLM API

* OpenRouter API

---

# 📂 Project Structure

```
ai-job-matching-agent
│
├── job_matching_agent
│   ├── agent
│   ├── api
│   ├── data
│   ├── database
│   ├── embeddings
│   ├── pipeline
│   ├── utils
│   │
│   ├── embedding_service.py
│   ├── insert_jobs.py
│   ├── job_recommender.py
│   ├── supabase_client.py
│   └── streamlit_test.py
│
├── job_dataset.csv
├── job_dataset.json
├── .gitignore
└── README.md
```

---

# 📊 Dataset

The project uses a **job descriptions dataset** containing various roles including:

* AI Engineer
* Machine Learning Engineer
* Data Scientist
* Software Developer
* Cloud Engineer
* and more.

Each job description includes:

* Job Title
* Skills
* Experience Level
* Keywords

These job descriptions are converted into **vector embeddings and stored in Supabase**.

---

# 🚀 How to Run the Project

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/ai-job-matching-agent.git
cd ai-job-matching-agent
```

---

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Add Environment Variables

Create a `.env` file:

```
OPENROUTER_API_KEY=your_api_key
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

---

### 4️⃣ Run the Application

```bash
streamlit run job_matching_agent/streamlit_test.py
```

---

# 🖥 Example Output

The system recommends jobs with similarity scores based on resume skills.

Example:

```
AI Engineer – Experienced
Similarity Score: 0.58

Machine Learning Engineer – Fresher
Similarity Score: 0.57

AI Engineer – Entry Level
Similarity Score: 0.57
```

---

# 🔐 Security Note

Sensitive information such as API keys is stored in `.env` files and excluded from Git using `.gitignore`.

---

# 🎯 Future Improvements

* Resume parsing with advanced NLP models
* Multi-resume comparison
* Job filtering by location or company
* RAG-based job insights
* Recruiter dashboard

---

# 👨‍💻 Author

**Devang Patel**

AI / Machine Learning Engineer
B.Tech Artificial Intelligence & Machine Learning

GitHub: https://github.com/22aim1031

---

# ⭐ If you found this project useful

Give the repository a ⭐ to support the project.
