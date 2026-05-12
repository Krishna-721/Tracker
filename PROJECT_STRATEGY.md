# Project Strategy: Job Application Tracker

## 🎯 Project Vision
A unified portal that eliminates the hassle of manually tracking job applications by automatically scanning a user's Gmail, filtering out noise, and classifying application stages.

## 🛠 Current State (The "Plumbing")
The infrastructure is currently functional and follows a "Connect $\rightarrow$ Fetch $\rightarrow$ Predict $\rightarrow$ Store" loop:
- **Auth:** Gmail OAuth2 integration is implemented.
- **Sync Engine:** Fetches recent messages and filters them via `is_spam` heuristics.
- **Classification:** Uses a TF-IDF Vectorizer and a trained model (via `joblib`) to categorize emails into: `Applied`, `Interview`, `Offer`, or `Rejected`.
- **Persistence:** Results with $\ge 0.5$ confidence are stored in a PostgreSQL database.
- **Bottleneck:** The current model is trained on a very small dataset (approx. 44 samples), leading to algorithmic fragility and low semantic understanding.

## 🚀 Future Roadmap (The "Brain" Upgrade)

### 1. Model Evolution
- **Transition to Transformers:** Replace TF-IDF with **DistilBERT** to move from keyword frequency to semantic intent understanding.
- **Data Bootstrapping:** 
    - Use LLM-generated synthetic data to expand the training set.
    - Implement Zero-Shot Classification (e.g., `facebook/bart-large-mnli`) to label larger datasets for fine-tuning.
- **Confidence Tuning:** Optimize the classification threshold to balance precision and recall.

### 2. Feature Expansion
- **Named Entity Recognition (NER):** Implement extraction of **Company Name** and **Job Role** from email bodies to replace the generic "sender" field.
- **Human-in-the-Loop:** Create a UI mechanism for users to correct classifications, using this feedback as a gold-standard dataset for model improvement.
- **Advanced Filtering:** Upgrade the `is_spam` logic into a more robust "Job-Related" filter.

### 3. Product Experience
- **Funnel Analytics:** Visualize the application lifecycle (Applied $\rightarrow$ Interview $\rightarrow$ Offer).
- **Timeline Tracking:** Track the evolution of a single application across multiple stages over time.

## 📌 Final Conclusion
The project has a solid technical foundation. The primary objective for the next phase is solving the **Data Problem** to move the intelligence from a "keyword searcher" to a "context-aware tracker."
