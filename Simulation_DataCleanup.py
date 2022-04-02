import pandas as pd

csv_file_one = "FAZA1_SIMULACIJA_BACKUP.csv"
csv_file_two = "FAZA2_SIMULACIJA_BACKUP.csv"

df_one = pd.read_csv(csv_file_one, sep=',', encoding='utf8', index_col='_id')
df_two = pd.read_csv(csv_file_two, sep=',', encoding='utf8', index_col='_id')

phase_one_indexes = list(df_one.index)

df_two = df_two.drop(phase_one_indexes)

def clean_data(df, phase):

    df_answers = df.filter(regex='answers')

    df.drop(list(df.filter(regex = 'answers')), axis = 1, inplace = True)

    df_answers_new = df_answers

    for column in df_answers_new.columns:
        task_name = column.split('.')[1] 
        
        split_df = df_answers_new[column].str.split(',', expand=True)
        split_df = split_df.add_prefix('{}_'.format(task_name))

        df_answers_new.drop(column, axis=1, inplace=True)
        
        df_answers_new = pd.merge(df_answers_new, split_df, on='_id')

    df_answers_new = df_answers_new.replace(r'\[|\]', '', regex=True)

    df_answers_new.columns = df_answers_new.columns.str.replace("0", "Answer")
    df_answers_new.columns = df_answers_new.columns.str.replace("1", "Time")

    df = pd.merge(df, df_answers_new, on='_id')

    df = df.rename(columns={
        'age': 'Age',
        'education': 'Education',
        'gender': 'Gender',
        'Auction_Answer': 'Answer.Auction',
        'Auction_Time': 'Time.Auction',
        'Bandits_Answer': 'Answer.Bandits',
        'Bandits_Time': 'Time.Bandits',
        'Butcher_Answer': 'Answer.Butcher',
        'Butcher_Time': 'Time.Butcher',
        'Doctor_Answer': 'Answer.Doctor', 
        'Doctor_Time': 'Time.Doctor', 
        'Guard_Answer': 'Answer.Guard',
        'Guard_Time': 'Time.Guard',
        'Mayor_Answer': 'Answer.Mayor', 
        'Mayor_Time': 'Time.Mayor',
        'Salesman_Answer': 'Answer.Salesman', 
        'Salesman_Time': 'Time.Salesman',
    })

    df = df.reset_index(drop=True)

    sorted_columns = ['Age', 'Education', 'Gender', 
       'Answer.Guard', 'Time.Guard',
       'Answer.Salesman', 'Time.Salesman',
       'Answer.Butcher', 'Time.Butcher',
       'Answer.Auction', 'Time.Auction',
       'Answer.Bandits', 'Time.Bandits', 
       'Answer.Doctor', 'Time.Doctor', 
       'Answer.Mayor', 'Time.Mayor']

    df = df.reindex(columns=sorted_columns)

    df.to_excel('faza{}_simulacija_odgovori_clean.xlsx'.format(phase), index=False, encoding='utf16')

clean_data(df_one, '1')
clean_data(df_two, '2')