from datasets import load_dataset
import pandas as pd

categories = [
    'algebra',
    'counting_and_probability',
    'geometry',
    'intermediate_algebra',
    'number_theory',
    'prealgebra',
    'precalculus',
]

combined_train_df = pd.DataFrame()
combined_test_df = pd.DataFrame()

split_train = "train"
split_test = "test"

for subject in categories:
    dataset = load_dataset('baber/hendrycks_math', subject)

    data_split_train = dataset[split_train]
    data_split_test = dataset[split_test]

    train_df = pd.DataFrame(data_split_train)
    test_df = pd.DataFrame(data_split_test)

    combined_train_df = pd.concat([combined_train_df, train_df], ignore_index=True)
    combined_test_df = pd.concat([combined_test_df, test_df], ignore_index=True)


combined_train_df.to_csv('trainData.csv')
combined_test_df.to_csv('testData.csv')





