# Sympathy Analyzer – Book Review Sentiment Scorer

A simple yet effective web app that analyzes book reviews and generates a **sympathy score** for each review.

This project uses:
- **Flask**
- **MongoDB**
- **HTML, CSS, JavaScript**

---

## 🚀 Features
- Clean UI for submitting reviews  
- Automatic sympathy scoring  
- MongoDB storage  
- Flask API endpoints  
- Includes JSON dump of DB collections for instant setup  

---

## 📂 Project Structure
```
sympathy-analyzer/
│
├── static/
│   ├── styles.css
│   └── script.js
│
├── templates/
│   └── index.html
│
├── app.py
├── requirements.txt
├── sympathy_database.json
└── README.md
```

---

## 🗄️ Database Setup (MongoDB)

### Steps:
1. Open **MongoDB Compass**  
2. Create a database named **Book**  
3. Import:
   ```
   sympathy_database.json
   ```
4. Compass will automatically create the required collections.

---

## 🛠 Installation & Setup

### 1. Clone the Repo
```
git clone https://github.com/your-username/sympathy-analyzer.git
cd sympathy-analyzer
```

### 2. Install Dependencies
```
pip install -r requirements.txt
```

### 3. Configure MongoDB Connection
```
client = MongoClient("mongodb://localhost:27017/")
db = client["Book"]
```

### 4. Run the App
```
python app.py
```

Visit:
```
http://127.0.0.1:5000/
```

---

## 🤝 Contributing
Contributions and suggestions are welcome.

---

## 📜 License
MIT License
