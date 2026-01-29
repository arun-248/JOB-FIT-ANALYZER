# 🎯 Job Fit Analyzer

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white&style=for-the-badge)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-FF4B4B?logo=streamlit&logoColor=white&style=for-the-badge)](https://streamlit.io/)
[![Gemini](https://img.shields.io/badge/Gemini-2.0%20Flash-4285F4?logo=google&logoColor=white&style=for-the-badge)](https://deepmind.google/technologies/gemini/)
[![spaCy](https://img.shields.io/badge/spaCy-3.0+-09A3D5?logo=spacy&logoColor=white&style=for-the-badge)](https://spacy.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

**🚀 An AI-powered recruitment intelligence platform that analyzes candidate resumes against job descriptions to provide data-driven hiring decisions**

[Live Demo](#) | [Documentation](#) | [Report Bug](https://github.com/arun-248/JOB-FIT-ANALYZER/issues)

</div>

---

## 🌟 Project Highlights

> **Transform Your Hiring Process**: Upload a resume and job description to get comprehensive AI-powered analysis including skill matching, experience evaluation, gap analysis, and hiring recommendations - all in seconds.

**🎯 What makes this special:**
- **5-Component Analysis System** - Skills, Experience, Relevance, Education, Learning Ability
- **Intelligent Skill Matching** - 300+ tech skills with difficulty-based gap analysis
- **Production-Ready UI** - Beautiful dark blue gradient design with colorful sections
- **Comprehensive Reports** - JSON exports and detailed PDF summaries
- **Built for HR Professionals** - Real-world recruitment workflows

---

## 🚀 Key Features

### 📊 **5-Component Scoring System**
Get a complete picture of candidate fit across multiple dimensions:
- **Skills Match** - Technical and soft skills alignment with job requirements
- **Experience Analysis** - Years of experience, seniority level, and role history
- **Job Relevance** - How well past experience matches the target role
- **Education Fit** - Academic background and certifications
- **Learning Ability** - Adaptability and skill acquisition potential

### 🎓 **Intelligent Skill Analysis**
* **300+ Tech Skills Database** - Comprehensive skill taxonomy with categories
* **Difficulty-Based Gap Analysis** - Easy/Medium/Hard classification for upskilling
* **Learning Time Estimates** - Days required to acquire missing skills
* **Skill Categorization** - Programming, Frameworks, Databases, Cloud, DevOps, AI/ML

### 💡 **Smart Recommendations**
* **Hiring Decision Matrix** - Clear Strong Hire / Potential Fit / Not Recommended guidance
* **Gap Analysis** - Detailed breakdown of missing skills and knowledge areas
* **Training Roadmap** - Suggested learning path for skill development
* **Confidence Scoring** - AI confidence level in the analysis

### 📁 **Flexible Input Options**
* Upload PDF or TXT files
* Paste resume and JD text directly
* Batch processing capability
* Multi-format support

### 📈 **Comprehensive Reporting**
* **Overall Match Score** - 0-100 scoring with color-coded recommendations
* **Component Breakdown** - Individual scores for all 5 dimensions
* **Strengths & Gaps** - Detailed lists of what candidate brings and lacks
* **JSON Export** - Full analysis data for integration
* **Text Summary** - Human-readable report for quick review

---

## 🖼️ Application Preview

<div align="center">

### 🏠 **Main Dashboard**
*Clean, professional interface with dark blue gradient design*

![Dashboard](#)

### 📤 **Document Upload**
*Upload or paste resumes and job descriptions with colored input boxes*

![Upload Section](#)

### 📊 **Analysis Results**
*Comprehensive scoring breakdown with visual components*

![Analysis Results](#)

### 💪 **Strengths & Gaps**
*Detailed breakdown of candidate fit and improvement areas*

![Strengths and Gaps](#)

</div>

---

## 🔬 Methodology & Architecture

### 🛠️ **System Architecture**
```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Streamlit)                      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ File Upload  │  │   Analysis   │  │   Reports    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ Python Pipeline
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              Pipeline (CandidateIntelligencePipeline)        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │Text Extract  │  │ NLP Analysis │  │   Scoring    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ API Calls
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Gemini 2.0 Flash API                      │
│          (Skill Extraction, Gap Analysis, Scoring)           │
└─────────────────────────────────────────────────────────────┘
```

### 🎯 **Analysis Pipeline**
1. **Document Parsing** → Extract text from PDF/TXT files
2. **Text Preprocessing** → Clean and normalize resume/JD content
3. **Skill Extraction** → Identify technical and soft skills using NLP
4. **Experience Analysis** → Parse work history and calculate years
5. **AI Scoring** → Gemini-powered intelligent scoring across 5 dimensions
6. **Gap Analysis** → Identify missing skills with learning estimates
7. **Report Generation** → Create comprehensive hiring recommendation

---

## ⚙️ Tech Stack

### **Frontend**
- **Streamlit** - Modern Python web framework
- **Custom CSS** - Dark blue gradient design with colorful sections
- **Responsive Design** - Mobile and desktop compatible

### **Backend & Processing**
- **Python 3.8+** - Core programming language
- **spaCy** - Advanced NLP for skill extraction
- **PyPDF2** - PDF text extraction
- **Regular Expressions** - Pattern matching for skills
- **JSON** - Data serialization

### **AI & Machine Learning**
- **Google Gemini 2.0 Flash** - Advanced language model for scoring
- **spaCy NER** - Named Entity Recognition
- **Custom Skill Database** - 300+ categorized technical skills
- **Fuzzy Matching** - Skill name variations handling

### **Development Tools**
- **Git** - Version control
- **pip** - Package management
- **dotenv** - Environment configuration

---

## 📦 Installation

### **Prerequisites**
```bash
Python 3.8 or higher
pip package manager
Google Gemini API key
```

### **Step 1: Clone the Repository**
```bash
git clone https://github.com/arun-248/JOB-FIT-ANALYZER.git
cd JOB-FIT-ANALYZER
```

### **Step 2: Create Virtual Environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### **Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 4: Download spaCy Model**
```bash
python -m spacy download en_core_web_sm
```

### **Step 5: Configure Environment Variables**
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### **Step 6: Run the Application**
```bash
streamlit run ui/streamlit_app_final.py
```

The application will open in your browser at `http://localhost:8501`

---

## 🎯 Usage Guide

### **1. Upload Documents**
1. Navigate to the **Upload Documents** section
2. **Left Box (Cyan)** - Upload resume or paste text
3. **Right Box (Green)** - Upload job description or paste text
4. Choose between file upload or text paste for each

### **2. Analyze Candidate**
1. Click the **"🚀 ANALYZE CANDIDATE"** button
2. Wait 10-15 seconds for AI processing
3. View comprehensive analysis results

### **3. Review Results**
Navigate through 4 tabs:
- **🎯 Skills Analysis** - Matched skills, missing skills, gap analysis
- **💼 Experience Profile** - Years, seniority, role history
- **💪 Strengths & Gaps** - Key strengths and hiring recommendation
- **📄 Full Report** - Complete JSON data and export options

### **4. Export Reports**
- **Download JSON** - Full analysis data for integration
- **Download Summary** - Text report for quick review
- Share with hiring team or ATS systems

---

## 📂 Project Structure

```
JOB-FIT-ANALYZER/
├── src/
│   ├── pipeline.py              # Main analysis pipeline
│   ├── extractors/
│   │   ├── resume_extractor.py  # Resume parsing logic
│   │   └── jd_extractor.py      # Job description parsing
│   ├── analyzers/
│   │   ├── skill_matcher.py     # Skill matching engine
│   │   ├── experience_analyzer.py
│   │   └── gap_analyzer.py
│   └── scorers/
│       └── gemini_scorer.py     # AI-powered scoring
├── ui/
│   └── streamlit_app_final.py   # Streamlit frontend
├── data/
│   ├── skills_database.json     # 300+ tech skills
│   └── templates/               # Report templates
├── tests/
│   └── test_pipeline.py         # Unit tests
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
├── .gitignore                   # Git ignore rules
└── README.md                    # Documentation
```

---

## 🎨 UI Features

### **Color-Coded Design**
- **Header** - Cyan to white gradient
- **Upload Section** - Yellow/orange gradient heading
- **Resume Box** - Cyan border with glow effect
- **Job Description Box** - Green border with glow effect
- **Analyze Button** - Orange/yellow gradient with shadow
- **Score Card** - Dynamic color based on score (green/orange/red)

### **Interactive Elements**
- Hover effects on all cards
- Animated score display
- Responsive tabs
- Color-coded skill pills
- Progress indicators

### **Dark Blue Theme**
- Consistently dark blue gradient background
- High contrast text for readability
- Professional appearance
- Modern glassmorphism effects

---

## ⚠️ Important Notes

### **🔐 Security**
- Never commit `.env` files with API keys
- Always use environment variables for sensitive data
- Keep your Gemini API key private
- Sanitize uploaded file content

### **🚦 Limitations**
- Gemini API has rate limits (check your quota)
- File uploads should be under 5MB for optimal performance
- Analysis accuracy depends on resume/JD quality
- Currently supports English language only

### **📊 Scoring Criteria**
- **75-100**: Strong Hire - Excellent match
- **60-74**: Potential Fit - Good candidate with some gaps
- **0-59**: Not Recommended - Significant skill/experience gaps

---

## 🛠️ Troubleshooting

### **Streamlit won't start**
```bash
# Check if port 8501 is in use
netstat -ano | findstr :8501

# Use different port
streamlit run ui/streamlit_app_final.py --server.port 8502
```

### **spaCy model not found**
```bash
# Download the model
python -m spacy download en_core_web_sm

# Verify installation
python -c "import spacy; nlp = spacy.load('en_core_web_sm'); print('OK')"
```

### **Gemini API errors**
- Verify API key is correct in `.env`
- Check API quota/billing at Google AI Studio
- Ensure internet connection is stable
- Review rate limits

### **File upload fails**
- Check file format (PDF or TXT only)
- Verify file size (< 5MB recommended)
- Ensure file is not corrupted
- Try pasting text directly instead

### **Analysis taking too long**
- Large files may take 20-30 seconds
- Check internet speed (API calls required)
- Verify Gemini API is responding
- Try with smaller documents first

---

## 📈 Future Roadmap

### **Short-term Goals (Next 3 months)**
- [ ] Support for DOCX files
- [ ] Batch candidate analysis
- [ ] Advanced visualization (radar charts, skill matrices)
- [ ] Email report generation
- [ ] Integration with ATS systems

### **Long-term Vision (6-12 months)**
- [ ] Interview question suggestions based on gaps
- [ ] Salary recommendation engine
- [ ] Cultural fit analysis
- [ ] Video resume analysis
- [ ] Multi-language support
- [ ] Mobile app version
- [ ] API for third-party integrations

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### **Reporting Bugs**
1. Check existing issues first
2. Create detailed bug report with:
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - System information

### **Suggesting Features**
1. Open a discussion on GitHub
2. Describe the feature clearly
3. Explain the business value
4. Consider implementation complexity

### **Pull Requests**
1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Follow code style guidelines
4. Add tests for new features
5. Commit changes (`git commit -m 'Add AmazingFeature'`)
6. Push to branch (`git push origin feature/AmazingFeature`)
7. Open Pull Request with detailed description

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License - Free to use, modify, and distribute
Open source and community-driven
```

---

## 🙏 Acknowledgments

- **Google Gemini Team** - For the powerful AI API
- **Streamlit Team** - For the amazing Python framework
- **spaCy Team** - For excellent NLP tools
- **HR Community** - For feedback and feature suggestions
- **Open Source Community** - For inspiration and support

---

## 👥 Author

**Arun Chinthalapally**

Built with ❤️ for HR professionals and recruiters

- **GitHub:** [arun-248](https://github.com/arun-248)
- **LinkedIn:** [Arun Chinthalapally](https://www.linkedin.com/in/arun-chinthalapally-7a254b256)
- **Email:** arunchinthalapally248@gmail.com

---

## 📞 Support

Having issues? We're here to help!

- 📧 Email: arunchinthalapally248@gmail.com
- 🐛 [Report Bug](https://github.com/arun-248/JOB-FIT-ANALYZER/issues)
- 💡 [Request Feature](https://github.com/arun-248/JOB-FIT-ANALYZER/issues)
- 📖 [Documentation](https://github.com/arun-248/JOB-FIT-ANALYZER#readme)

---

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=arun-248/JOB-FIT-ANALYZER&type=Date)](https://star-history.com/#arun-248/JOB-FIT-ANALYZER&Date)

---

<div align="center">

### 🌟 If you find this project helpful, please give it a star! ⭐

**Built for recruiters, by developers | Powered by AI 🚀**

**Hire smarter, not harder**

[⬆ Back to Top](#-job-fit-analyzer)

</div>
