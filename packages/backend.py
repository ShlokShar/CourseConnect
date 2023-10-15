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


openai.api_key = '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'


def generate_question(category):
    model_id = 'ft:davinci-002:personal::80jYAUx6'

    prompt = f"generate me an {category} math question"
    max_tokens = 100

    while True:
        response = openai.Completion.create(
            model=model_id,
            temperature=0.2,
            max_tokens=max_tokens,
            prompt=prompt
        )

        generated_text = response.choices[0].text

        split_text = generated_text.split(' ')

        try:
            express_index = split_text.index("Express")

        except:
            max_tokens += 10
            continue

        end_index = 'not defined'

        for x in range(express_index, len(split_text)):
            if split_text[x].endswith('.'):
                end_index = x


        else:
            return ' '.join(split_text[0:end_index + 1])
            break
