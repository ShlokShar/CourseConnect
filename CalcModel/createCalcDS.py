from packages.imports import *

openai.api_key = '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'

topics = [
    'Limits_and_Continuity',
    'Fundamentals_of_Differentiation',
    'Composite_Implicit_and_Inverse_Functions',
    'Contexual_Applications_of_Differentiation',
    'Analytical_Applications_of_Differentiation',
    'Integration_and_Accumulation_of_Change',
    'Differential_Equations',
    'Applications_of_Integration',
    'Parametric_Equations_polar coordinates_and_vector-values_functions',
    'Infinite_Sequences_and_Series'
]

for topic in topics:
      df = pd.DataFrame(columns=['question','topic'])
      for x in range(0,100):
          response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=f'''
            Write me a python list of 10 examples of a calculus question regarding {topic}
            Please only include the question and nothing else
            ''',
            max_tokens = 500
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
              entry = {'quesiton': clean_sentence, 'topic': topic}

              df = df.append(entry, ignore_index=True)

      df.to_csv(f'{topic}_data.csv')