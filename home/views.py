from django.shortcuts import render
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import WordNetLemmatizer

# Hardcoded list of questions
questions = [
    ["Explain Alpha - Beta Tree search and cutoff procedure in deatil with example.", "April 2022", "Unit 3"],
    ["What are the issues that need to be addressed for solving esp efficiently? Explain the solutions to them.", "April 2021", "Unit 3"],
    ["Explain in detail the concepts of back tracking and constraint propagation and solve the N-queen problem using these algorithms.", "April 2022", "Unit 3"],
    ["Write a short note on Monte Carlo Tree search and list its limitations.", "April 2022", "Unit 3"],
    ["Apply constraint satisfaction method to solve following Problem SEND + MORE = MONEY.", "April 2022", "Unit 3"],
    ["Apply constraint satisfaction method to solve following Problem TWO + TWO = FOUR.", "April 2022", "Unit 3"],
    ["Apply constraint satisfaction method to solve following Problem CROSS + ROADS = DANGER.", "April 2022", "Unit 3"],
    ["List the inference rules used in first order logic? Explain them in detail with suitable example.", "April 2021", "Unit 4"],
    ["Explain syntax and semantics of First Order Logic in detail.", "April 2022", "Unit 4"],
    ["Detail the algorithm for deciding entailment in prepositional logic.", "April 2022", "Unit 4"],
    ["Explain knowledge representation structure and compare them.", "April 2022", "Unit 4"],
    ["Explain Forward and Backward chaining Algorithm. What factors justify whether reasoning is tobe done in forward or backward chaining.", "April 2022", "Unit 5"],
    ["What are the reasoning patterns in propositional logic? Explain them in detail.", "April 2022", "Unit 5"],
    ["Explain unification algorithm with an example.", "2021", "Unit 5"],
    ["Explain knowledge representation structures and compare them.", "2022", "Unit 5"],
    ["what do you mean by Ontology of situation calculus?", "2022", "Unit 5"],
    ["Analyse various planning approaches in detail.", "2021", "Unit 6"],
    ["Discuss AI and its ethical concerns. Explain limitations of AI.", "2022", "Unit 6"],
    ["Explain the terms for time and schedule from perspective of temporal planning.", "2022", "Unit 6"],
    ["Write a detailed note on AI Architecture.", "2021", "Unit 6"],
    ["Explain Min Max and Alpha Beta pruning algorithm for adversarial search with example.", "2021", "Unit 3"],
    ["Define and explain Constraints satisfaction problem.", "2021", "Unit 3"],
    ["Explain with example graph coloring problem.", "2021", "Unit 3"],
    ["How AI technique is used to solve tic-tac-toe problem.", "2021", "Unit 4"],
    ["Explain Wumpus world environment giving its PEAS description.", "2021", "Unit 4"],
    ["Explain different inference rules in FOL with suitable example.", "2021", "Unit 4"],
    ["Write an propositional logic for the statement, i) 'All birds fly' ii) 'Every man respect his parents'.", "2021", "Unit 3"],
    ["Differentiate between propositional logic and First order logic.", "2021", "Unit 4"],
    ["Explain Forward chaining algorithm with the help of example.", "2021", "Unit 5"],
    ["Write and explain the steps of knowledge engineering process.", "2021", "Unit 5"],
    ["Explain Backward chaining algorithm with the help of example.", "2022", "Unit 5"],
    ["Write a short note on : i) Resolution and ii) Unification.", "2021", "Unit 5"],
    ["Write a short note on : i) Resolution and ii) Unification.", "2021", "Unit 5"],
    ["Explain different components of planning system.", "2021", "Unit 6"],
    ["Explain the components of AI.", "2021", "Unit 6"],
    ["What are the types of planning? Explain in detail.", "2021", "Unit 6"],
    ["Explain Classical Planning and its advantages with example.", "2021", "Unit 6"],
    ["Write note on hierarchical task network planning.", "2021", "Unit 6"],
]

def index(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

def contactus(request):
    return render(request, "contactus.html")

def question_processing():
    nltk.download('stopwords') 

    # Preprocessing
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    def preprocess_text(text):
        tokens = nltk.word_tokenize(text.lower())
        tokens = [lemmatizer.lemmatize(token) for token in tokens if token.isalnum()]
        tokens = [token for token in tokens if token not in stop_words]
        return ' '.join(tokens)

    # Grouping questions with similar meaning
    preprocessed_questions = [preprocess_text(question[0]) for question in questions]
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(preprocessed_questions)
    similarities = cosine_similarity(vectors)

    groups = []
    used_indices = set()
    for i in range(len(similarities)):
        if i in used_indices:
            continue

        group_indices = [i]
        for j in range(i+1, len(similarities)):
            if similarities[i][j] > 0.45:
                group_indices.append(j)
                used_indices.add(j)

        if len(group_indices) > 1:
            group_str = []
            for idx in group_indices:
                group_str.append(questions[idx])
            groups.append(group_str)
        else:
            group_str = []
            group_str.append(questions[i])
            groups.append(group_str)
    
    return groups

def question_bank(request):
    #grouping questions with same meaning
    grouped_questions = question_processing()
    
    #send the generated questions list
    return render(request, 'questionbank.html', {'questions': grouped_questions})


def question_paper(request):
    #grouping questions with same meaning
    grouped_questions = question_processing()
    
    #sort the questions list unit-wise
    unitwise_grouped_questions = {}
    for question in grouped_questions:
        if(isinstance(question, list)):
            for unit in question[0][2:]:
                if unit not in unitwise_grouped_questions:
                    unitwise_grouped_questions[unit] = []
                unitwise_grouped_questions[unit].append(question)
        else:
            for unit in question[2:]:
                if unit not in unitwise_grouped_questions:
                    unitwise_grouped_questions[unit] = []
                unitwise_grouped_questions[unit].append(question)
    
    #sort the unit-wise questions list with mostly asked questions
    for unit in unitwise_grouped_questions:
        unitwise_grouped_questions[unit].sort(key=lambda x: len(x), reverse=True)

    #pick the mostly asked questions from each unit
    predicted_questions = []
    for unit, questions in unitwise_grouped_questions.items():
        count = 0
        for question in questions:
            if isinstance(question[0], list):
                selected_question = question[0]
            else:
                selected_question = question
            predicted_questions.append(selected_question)
            count += 1
            if count == 4:
                break
  
    return render(request, "questionpaper.html", {'questions': predicted_questions})
