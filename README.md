# Gemini_Titanic_Streamlit_App

# CSV Agent for Titanic Dataset

## Description
This Streamlit app allows users to interact with the Titanic dataset through natural language queries. The app uses Google's Generative AI (`gemini-1.5-flash`) to analyze the dataset and generate responses, including Python code for visualizations when required.

### Features:
- Accepts user questions in plain English.
- Leverages Google Generative AI to interpret queries and analyze the Titanic dataset.
- Automatically executes Python code from AI responses to generate visualizations.
- Displays generated plots and outputs in the Streamlit interface.

---

## Dataset
The app uses the **Titanic.csv** file, which contains the following columns:
- `PassengerId`: Passenger number (Unique Identifier).
- `Survived`: Survival status (0 = Dead, 1 = Alive).
- `Pclass`: Passenger class (1 = First Class, 2 = Second Class, 3 = Third Class).
- `Name`: Passenger's name.
- `Sex`: Gender (male, female).
- `Age`: Passenger's age.
- `SibSp`: Number of siblings/spouses aboard.
- `Parch`: Number of parents/children aboard.
- `Ticket`: Ticket number.
- `Fare`: Ticket fare.

---

## How to Run
### Prerequisites
1. Install Python (3.8 or later).
2. Ensure you have a Google Generative AI API key.

### Steps
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/yourrepository.git
