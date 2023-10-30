from packages.imports import *

openai.api_key = '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'

rhetoric_def = {
    'Parallelism': 'parallelism, in rhetoric, component of literary style in both prose and poetry, in which coordinate ideas are arranged in phrases, sentences, and paragraphs that balance one element with another of equal importance and similar wording',
    'Understatement': 'An understatement is a transitive verb used by writers or speakers in order to intentionally make a situation seem less important or smaller than it is.',
    'Antithesis': 'Antithesis is a figure of speech that places two completely contrasting ideas or clauses in juxtaposition',
    'Epithet': 'An epithet is a literary device that describes a person, place, or object by accompanying or replacing it with a descriptive word or phrase.',
    'Aphorism': 'An aphorism is a short, pithy statement offering instruction, truth, or opinion; like a maxim or an adage.',
    'Metaphor': 'a figure of speech that directly compares one thing to another for rhetorical effect',
    'Hyperbole': 'Hyperbole is a rhetorical and literary technique where an author or speaker intentionally uses exaggeration and overstatement for emphasis and effect',
    'Pathos': 'Pathos, or the appeal to emotion, means to persuade an audience by purposely evoking certain emotions to make them feel the way the author wants them to feel.',
    'Ethos': 'Focuses attention on the writers or speakers trustworthiness',
    'Irony': 'a literary device that uses irony to mock someone or something or convey contempt',
    'Induction': 'A process of reasoning (arguing) which infers a general conclusion based. on individual cases, examples, specific bits of evidence, and other specific types of premises.',
    'Deduction': 'A process of reasoning that starts with a general truth, applies that truth to. a specific case (resulting in a second piece of evidence), and from those two pieces of evidence (premises), draws a specific conclusion about the specific case.',
    'Periodic_Sentence': ' a sentence in which the completion of the main clause is left to the end, thus creating an effect of suspense.',
    'Anaphora': 'An anaphora is a rhetorical device in which a word or expression is repeated at the beginning of a number of sentences, clauses, or phrases.',
    'Connotation': 'Connotation is the use of a word to suggest a different association than its literal meaning',
    'Syllogism': 'a type of deductive reasoning that presents a major premise and a minor premise to guide the reader towards a valid conclusion.',
    'Euphemism': 'A euphemism is a word or phrase that softens an uncomfortable topic.',
    'Cumulative_Sentence': 'A cumulative sentence (also sometimes called a loose sentence) is an independent clause followed by one or more modifiers. Essentially, you use words, phrases, and clauses to expand on or refine the main idea of the sentence.',
    'Inversion': 'inversion, also called anastrophe, in literary style and rhetoric, the syntactic reversal of the normal order of the words and phrases in a sentence',
    'Paradox': 'A paradox is a rhetorical device that is made up of two opposite things and seems impossible or untrue but is actually possible or true',
    'Simile': 'a rhetorical device used to compare two things using the words “like,” “as,” or “than.” ',
    'Logos': 'Logos, or the appeal to logic, means to appeal to the audiences sense of reason or logic.',
    'Tone': 'In literary terms, tone typically refers to the mood implied by an authors word choice and the way that the text can make a reader feel.',
    'Alliteration': 'Alliteration is the repetition of the same sound at the start of a series of words in succession whose purpose is to provide an audible pulse that gives a piece of writing a lulling, lyrical, and/or emotive effect. This paragraph is an example of alliteration.',
    'Apostrophe': 'a rhetorical figure in which the speaker addresses a dead or absent person, or an abstraction or inanimate object',
    'Interrupted_Sentence': ' a word group (a statement, question, or exclamation) that interrupts the flow of a sentence and is usually set off by commas, dashes, or parentheses.',
    'Allusion': 'A figure of speech which makes brief, even casual reference to a historical or literary. figure, event, or object to create a resonance in the reader or to apply a symbolic meaning.',
    'Balanced_Sentence': 'A balanced sentence is one in which sentence elements (words, phrases, clauses) of equal importance are set off against each other.',
    'Onomatopoeia': 'Onomatopoeia is a literary device that uses the letter sounds of a word to imitate the natural sound emitted from an object or action.',
    'Epigram': 'An epigram is a short, pithy saying, usually in verse, often with a quick, satirical twist at the end.',

}

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

for term in rhetoric_def:
    if term in keys.values():
        df = pd.DataFrame(columns=['sentence', 'term'])
        for x in range(0, 100):
            response = openai.Completion.create(
                model="gpt-3.5-turbo-instruct",
                prompt=f'''
              Write me a python list of 10 examples of the rhetorical use of {term}
              Definition of {term}: {rhetoric_def[term]}
              Please include a variety of {term}
              Variety of the term is very important
              Please only include the sentence and nothing else
              If it is a quote, please do not name who quoted it
              ''',
                max_tokens=500
            )

            response_text = response['choices'][0]['text']

            output_list = response_text.splitlines()

            cleaned_sentences = []

            for line in output_list:
                parts = line.split(' ', 1)
                if len(parts) == 2:
                    sentence = parts[1].strip().strip('"')
                    cleaned_sentences.append(sentence)

            for clean_sentence in cleaned_sentences:
                entry = {'sentence': clean_sentence, 'term': term}

                df = df.append(entry, ignore_index=True)

        df.to_csv(f'{term}_data.csv')
