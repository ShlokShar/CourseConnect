from packages.imports import *


# redirects user to launch page if they aren't logged in
def logged_in(f):
    @wraps(f)
    def validator(*args, **kwargs):
        if flask.session.get("email"):
            return f(*args, **kwargs)
        else:
            return flask.redirect("/")

    return validator


calctokenizer = AutoTokenizer.from_pretrained("tiiuae/falcon-7b-instruct")
calcModel = FalconForCausalLM.from_pretrained("tiiuae/falcon-7b-instruct")

langtokenizer = AutoTokenizer.from_pretrained('bert-base-uncased')
langmodel = AutoModelForSequenceClassification.from_pretrained(
    '/Users/aadeshsahoo/Documents/CourseConnect/LangModel/Modelv2', num_labels=30)

keys = {
    0: 'Parallelism',
    1: 'Understatement',
    2: 'Antithesis',
    3: 'Epithet',
    4: 'Aphorism',
    5: 'Hyperbole',
    6: 'Pathos',
    7: 'Ethos',
    8: 'Periodic_Sentence',
    9: 'Anaphora',
    10: 'Syllogism',
    11: 'Euphemism',
    12: 'Cumulative_Sentence',
    13: 'Paradox',
    14: 'Logos',
    15: 'Apostrophe',
    16: 'Allusion',
    17: 'Balanced_Sentence',
    18: 'Epigram'
}

sentence = "We shall not flag or fail. We shall go on to the end. We shall fight in France, we shall fight on the seas and oceans, we shall fight with growing confidence and growing strength in the air, we shall defend our island, whatever the cost may be, we shall fight on the beaches, we shall fight on the landing grounds, we shall fight in the fields and in the streets, we shall fight in the hills. We shall never surrender."


def generate_question(category):
    if category == 'AP Calculus':
        pr = random.choices(
            ["limits", "derivatives", "integrals", "differentiability", "parametric equations", "vectors",
             "infinite series"])
        input_ids = calctokenizer.encode(pr, return_tensors="pt")

        output = calcModel.generate(input_ids, max_length=500)

        generated_text = calctokenizer.decode(output[0], skip_special_tokens=True)

        return generated_text

    elif category == 'AP English and Language':
        prompt = f'''
        Generate me a well known piece of next that showcases a salient rhetoric term.
        Please only output the piece of text and nothing else
        Limit the text to three sentences maximum
        '''

        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=500
        )
        response_text = response['choices'][0]['text']

        return str(response_text)


def grade_question(category, question, user_answer):
    if category == 'AP Calculus':
        prompt = f'''
    question: {question}
    answer: {user_answer}

    please only respond with 1 if this is correct and 0 if it is incorrect. do not provide any explanation
    '''

        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=500
        )

        response_text = response['choices'][0]['text']

        return response_text

    elif category == 'AP English and Language':

        tokens = langtokenizer(question, return_tensors='pt', padding=True, truncation=True)

        outputs = langmodel(**tokens)

        logits = outputs.logits

        predicted_class = torch.argmax(logits, dim=1)

        if predicted_class.lower() == user_answer.lower():
            return "1"
        else:
            return "0"
