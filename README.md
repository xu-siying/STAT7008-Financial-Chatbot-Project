# Financial Investment Chatbot Project

## Project Overview
The Financial Investment Chatbot Project aims to develop an intelligent conversational agent designed to assist customers with financial investment products. This chatbot leverages advanced NLP (Natural Language Processing) and deep learning techniques to provide accurate responses to customer queries, predict follow-up questions, and offer personalized recommendations.

The primary goal of this project is to automate the handling of customer inquiries about financial products, such as investment funds, stock market updates, and risk assessments, thereby improving customer satisfaction and reducing the workload on customer support teams. Moreover, the chatbot is capable of recognizing user emotions through video input, which allows it to tailor responses accordingly, making interactions more meaningful.

## Project Objectives
Accurate Query Resolution: Ensure users get precise answers to their investment-related questions through an intelligently curated knowledge base.
Emotion Recognition for Personalized Service: Utilize facial emotion analysis to enhance the quality of responses and detect underlying user emotions.
Predictive Interaction: Predict user follow-up questions and proactively suggest relevant topics or solutions.
Efficient Query Classification: Classify user queries into distinct categories such as "investment advice," "risk management," "fees and costs," etc., for quick and targeted response.

## Key Features (Tentative)
- **Keyword Extraction and Topic Identification**: Extracts and categorizes keywords to better understand user queries.
- **Query Classification**: Categorizes questions by type, such as investment advice, risk assessment, and fee structure.
- **Knowledge Base Retrieval & Similarity Analysis**: Matches user questions with the most relevant answers in the knowledge base.
- **Dialogue Prediction & Personalization**: Predicts follow-up questions based on user history and offers personalized responses.
- **Facial Emotion Analysis**: Facial Emotion Analysis: Detects customer emotions through video input (e.g., happy, sad, neutral), using this information to adjust responses and provide more empathetic service.

## Data Sources

This project utilizes a combination of open data sources and APIs to collect, analyze, and generate responses for user inquiries:

### Financial Datasets for Large Language Models:
Type: Semantic datasets for training language models on financial contexts.
Usage: Provides a comprehensive dataset for understanding and generating financial language.
Access:  [GitHub - Financial Datasets](https://github.com/viratt/financial-datasets)

### Yahoo Finance:
Type: Stock and financial data.
Usage: To fetch real-time stock prices, historical data, and company performance information.
Access: Uses Yahoo Finance](https://finance.yahoo.com)  to connect to the Yahoo Finance API.

###  [Investopedia](https://www.investopedia.com) & [Morningstar](https://www.morningstar.com):
Type: Financial articles, product information, and educational resources.
Usage: To build the knowledge base by extracting descriptions of investment products and providing detailed explanations.
Access: Data is collected by scraping or extracting relevant information to generate accurate responses to customer inquiries.

### Kaggle Financial Datasets:
Examples:
-[Complete Financial Analysis](https://www.kaggle.com/code/prayankkul/complete-financial-analysis): Provides a dataset for detailed financial analysis.
-[Bank Customer Complaints](https://www.kaggle.com/datasets/taeefnajib/bank-customer-complaints): A dataset of customer complaints for training models in understanding typical customer queries and complaints.
- [Finance Data](https://www.kaggle.com/datasets/nitindatta/finance-data): Contains various types of financial data useful for developing knowledge about different financial products.
Usage: For training classification and similarity models, extracting topics and identifying common complaints.

### SEC Database (EDGAR):
Type: Corporate filings and financial reports.
Usage: To obtain publicly available financial statements and corporate information for U.S.-based companies.
Access: Through web scraping or API integration, providing transparency and details for certain financial products.

### Commercial Bank Websites:
Type: Information on financial products, including investment options, loan products, and financial planning tools.
Usage: To expand the chatbot’s knowledge base by gathering up-to-date product information directly from banks.
Access: Data collected from publicly available pages on major commercial banks' websites (e.g., JPMorgan Chase, Bank of America).

### Video and Image Data for Emotion Analysis:
Type: Videos of financial analysts and customer service interactions.
Usage: For training and testing the emotion analysis model to recognize facial expressions indicative of emotions (e.g., excitement, sadness, neutrality).
Access: Videos can be sourced from Yahoo Money Talk or similar financial news sources, with emotional analysis performed using pre-trained models in DeepFace and OpenCV.

## Project Directory Structure (Tentative)

```
financial_chatbot_project/
│
├── data/                        
│   ├── raw/                     # Raw data
│   └── processed/               # Processed data
│
├── data_pipeline/               # Data fetching and preprocessing package
│   ├── data_fetch.py            # Data fetching
│   ├── text_preprocessing.py    # Text data preprocessing
│   ├── numerical_preprocessing.py # Numerical data preprocessing
│   ├── time_series_preprocessing.py # Time series data preprocessing
│   └── categorical_preprocessing.py # Categorical data preprocessing
│
├── models/                      
│   ├── keyword_extraction.py    # Keyword extraction and topic identification
│   ├── classification.py        # Text classification model
│   ├── similarity.py            # Knowledge base retrieval and similarity analysis
│   └── dialogue_prediction.py   # Dialogue prediction and personalization
│
├── app/                         # Backend application
│   ├── controllers/             # Controller logic for API endpoints
│   │   ├── chat_controller.py   # Main chat controller
│   │   ├── emotion_controller.py # Controller for emotion analysis
│   │   └── analytics_controller.py # Dashboard data controller
│   ├── routes.py                # API routes definitions
│   ├── chatbot.py               # Main chatbot application logic
│   ├── knowledge_base.py        # Knowledge base management
│   └── dashboard.py (Tentative)         # Dashboard logic (backend processing)
│
├── frontend/                    # Frontend application
│   ├── index.html               # Main HTML file for the chatbot interface
│   ├── style.css                # CSS styling for the interface
│   ├── app.js                   # JavaScript logic for handling user input and API calls
│   └── assets/                  # Static assets (e.g., images, icons)
│
├── server.py                    # Server setup and initialization
├── config.py                    # Configuration for database and environment variables
├── requirements.txt             # Project dependencies
└── README.md                    # Project documentation

```

## Installation and Setup

### Prerequisites
- Python 3.7+
- Git
- MongoDB (for knowledge base and logging)
- [DeepFace](https://github.com/serengil/deepface) and [OpenCV](https://opencv.org/) (for facial emotion analysis)

### Installation Steps
1. Clone the project repository
    ```bash
    git clone https://github.com/xu-siying/STAT7008-Financial-Chatbot-Project.git
    cd financial_chatbot_project
    ```

2. Install dependencies
    ```bash
    pip install -r requirements.txt
    ```

3. Configure the Database
   In `config.py`, set up MongoDB and other database connection parameters.

4. Download relevant pre-trained model files (e.g., BERT, GPT) and place them in the `models/` folder.

## Usage Instructions

### Data Fetching and Preprocessing
Before starting the project, data collection and preprocessing are essential. You can run the modules under `data_pipeline` to fetch and clean data.

Example:
```bash
python data_pipeline/data_fetch.py
python data_pipeline/text_preprocessing.py
```

### Model Training
Each module in the `models/` folder contains code for different tasks, such as keyword extraction, text classification, and similarity analysis.

Example:
```bash
python models/classification.py
python models/similarity.py
```

### Starting the Chatbot
Run `app/chatbot.py` to start the chatbot. It can be connected to the frontend via API endpoints or tested via CLI.

Example:
```bash
python app/chatbot.py
```
## 1. Backend (app/)

**controllers/**: This folder holds controller files for different API endpoints. Each controller corresponds to specific functionality (e.g., handling chat requests, emotion analysis, or analytics).
- **chat_controller.py**: Manages chat requests, handles NLP pipeline  (keyword extraction, classification, and response generation).
- ** emotion_controller.py**: Handles video input for emotion detection, passing data to the emotion analysis model.
- **analytics_controller.py**: Retrieves data required for performance metrics, such as response accuracy, latency, and sentiment distribution, to display on the dashboard..
**routes.py**: Defines all API routes and associates them with respective controllers.
**chatbot.py**: Core chatbot logic, such as loading models, querying the knowledge base, and generating responses.
**knowledge_base.py**: Manages knowledge base data, responsible for storing and retrieving FAQ-style responses.
**dashboard.py  (Tentative)**: Manages backend processing for the dashboard, including pulling relevant performance metrics. Run `app/dashboard.py` to access a dashboard that monitors the chatbot’s key performance indicators, such as accuracy, response time, and user satisfaction.


## 2. Frontend (frontend/)

-** index.html** : Main HTML file for chatbot interface, where users input questions and view responses.
-** style.css** : Contains CSS styling for chatbot interface elements.
-** app.js** : Manages JavaScript logic for handling user input, making API requests, and updating the UI.
-** assets/** : Static assets like images, icons, or any other front-facing files required by the frontend.

## 3. Server Setup (server.py)

This is the main entry point for the application server. It initializes the backend API, connects it to the frontend, and sets up the environment. 


### Facial Emotion Analysis
To use the facial emotion analysis module, run `models/emotion_detection.py` and provide the path to a video file. The system will detect and output emotion data.

Example:
```bash
python models/emotion_detection.py --video_path="path/to/video.mp4"
```

## Database Management
This project uses MongoDB to store user queries, knowledge base entries, and emotion analysis results, allowing for efficient data retrieval and analysis. Ensure MongoDB is installed and configured in `config.py`.

## Tech Stack
- **Programming Language**: Python
- **Machine Learning**: Scikit-learn, TensorFlow, PyTorch
- **NLP**: spaCy, NLTK, Hugging Face Transformers
- **Database**: MongoDB
- **Frontend**: HTML/CSS (for frontend interface and basic visualization)
- **Data Visualization (Tentative)**: Matplotlib, D3.js (used in `dashboard.py`)

## Contributions
- Liu Yuchen
- Siying Xu  
- Wang Pengyi 
- Wang Chuanyue 
- He Yongbin


