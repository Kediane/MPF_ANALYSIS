import pandas as pd


def clean_dataset(input_path: str, output_path: str):
    data = pd.read_json(input_path)

    data['Annual Returns'].apply(pd.Series)

    new_data = pd.concat(
        [
            data.drop(['Annual Returns'], axis=1),
            data['Annual Returns'].apply(pd.Series)
        ],
        axis=1
    )
    new_data.columns = [
        'Scheme',
        'Name',
        'Fund Type',
        'Launch Date',
        'Fund Size (HKD m)',
        'Risk Class',
        'Latest FER (%)',
        'Annualized Return: 1 Year (% p.a.)',
        'Annualized Return: 5 Year (% p.a.)',
        '10 Year',
        'Since Launch'
    ]

    del new_data['10 Year']

    new_data['Annualized Return: 1 Year (% p.a.)'].fillna(
        new_data['Annualized Return: 1 Year (% p.a.)'].mean(),
        inplace=True
    )
    new_data['Since Launch'].fillna(
        new_data['Since Launch'].mean(),
        inplace=True
    )
    new_data['Annualized Return: 5 Year (% p.a.)'].fillna(
        new_data['Annualized Return: 5 Year (% p.a.)'].mean(),
        inplace=True
    )
    new_data.to_json(output_path)


if __name__ == '__main__':
    clean_dataset('../dataset/funds.json', "../dataset/cleaned_funds.json")
