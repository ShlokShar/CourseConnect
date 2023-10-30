from packages.imports import *

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

df = pd.DataFrame()

for term in keys:
    df2 = pd.read_csv(f'{keys[term]}_data.csv')
    df = df.append(df2, ignore_index=True)

df['term'] = df['term'].map({v: k for k, v in keys.items()})
df = df[['term', 'sentence']]
df = df.dropna()

df.to_csv('allLangData.csv')

tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")


def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True)


local_csv = load_dataset('csv', split='train', data_files='allLangData.csv')
local_csv = local_csv.train_test_split(test_size=0.20146058927)
filteredDataset = local_csv.remove_columns(["Unnamed: 0"])
filteredDataset = filteredDataset.rename_column("sentence", "text")
filteredDataset = filteredDataset.rename_column("term", "label")
filteredDataset = filteredDataset.shuffle(seed=42)

tokenized_datasets = filteredDataset.map(tokenize_function, batched=True)

model = AutoModelForSequenceClassification.from_pretrained("bert-base-cased", num_labels=30)
training_args = TrainingArguments(output_dir="test_trainer", evaluation_strategy="epoch", num_train_epochs=4,
                                  )

metric = evaluate.load("accuracy")


def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return metric.compute(predictions=predictions, references=labels)


trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets['train'],
    eval_dataset=tokenized_datasets['test'],
    compute_metrics=compute_metrics,
)

trainer.train()

output_dir = "/model"
trainer.save_model(output_dir)
