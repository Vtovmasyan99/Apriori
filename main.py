import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from collections import defaultdict

THRESHOLD = 600
THRESHOLD_PAIR = 100
THRESHOLD_TRIPLE = 10

trans_df = pd.read_csv('Grouped.csv')
trans_df.drop(['Date', 'Member_number'], axis=1, inplace=True)
trans_df.index.rename('TID', inplace=True)
trans_df.rename(columns={'itemDescription': 'item_list'}, inplace=True)


def count_top10_frequent():
    data = pd.read_csv('Groceries_dataset.csv')
    top_ten = data['itemDescription'].value_counts().sort_values(ascending=False)[:10]
    print("K=1 most frequent items are: ")
    plt.rcParams["figure.figsize"] = (20, 10)
    print(top_ten)
    plt.bar(top_ten.index, top_ten.values)
    plt.width = 1
    # plt.show()
    plt.savefig('Top10items.png')


def count_top10_customers():
    data = pd.read_csv('Groceries_dataset.csv')
    top_ten = data['Member_number'].value_counts().sort_values(ascending=False)[:10]
    plt.rcParams['figure.figsize'] = (20, 10)
    print("Most loyal customer's ID: ")
    print(top_ten)
    plt.bar(top_ten.index, top_ten.values)
    plt.width = 1
    plt.savefig('Top10Customers.png')


def create_transactions_and_save():
    data = pd.read_csv('Groceries_dataset.csv')
    data = data.groupby(['Member_number', 'Date'])['itemDescription'].unique().apply(lambda x: list(x))
    data.to_csv('Grouped.csv')


def normalize_group(*args):
    return str(sorted(args))


def generate_pairs(item1, item2, item3):
    all_pairs = []
    all_pairs.append(normalize_group(item1, item2))
    all_pairs.append(normalize_group(item1, item3))
    all_pairs.append(normalize_group(item2, item3))
    return all_pairs


def main():
    item_counts = defaultdict(int)
    pair_counts = defaultdict(int)
    triple_counts = defaultdict(int)

    transactions = trans_df['item_list'].tolist()
    num_items = len(transactions)
    new_transactions = []
    for transaction in transactions:
        transaction = transaction[1:-1]
        trans_items = transaction.split(',')
        new_trans_items = []
        for item in trans_items:
            item = item.strip()
            item = item[1:-1]
            new_trans_items.append(item)
        new_transactions.append(new_trans_items)

    for transaction in new_transactions:
        for item in transaction:
            item_counts[item] += 1

    frequency_item_array = []
    frequent_items = set()
    for key in item_counts:
        if item_counts[key] > THRESHOLD:
            frequent_items.add(key)
            val = [key, item_counts[key]]
            frequency_item_array.append(val)

    print(f"WITH FREQUENCY THRESHOLD OF {THRESHOLD} THERE ARE OVERALL {len(frequency_item_array)} ITEMS.")
    print("TOP 10 FREQUENT ITEMS ARE: ")
    frequency_item_array.sort(key=lambda row: row[1], reverse=True)
    for item in frequency_item_array[0:10]:
        print(f'Item name: {item[0]}, support: {item[1]}/{num_items}')

    for transaction in new_transactions:
        for index1 in range(len(transaction) - 1):
            if transaction[index1] not in frequent_items:
                continue
            for index2 in range(index1 + 1, len(transaction)):
                if transaction[index2] not in frequent_items:
                    continue
                pair = normalize_group(transaction[index1], transaction[index2])
                pair_counts[pair] += 1

    frequent_pairs = set()
    frequent_pair_array = []
    for key in pair_counts:
        if pair_counts[key] > THRESHOLD_PAIR:
            frequent_pairs.add(key)
            item1, item2 = key.split(', ')
            item1 = item1[2:-1]
            item2 = item2[1:-2]
            confidence1 = f'{str(pair_counts[key])} / {str(item_counts[item1])}'
            confidence2 = f'{str(pair_counts[key])} / {str(item_counts[item2])}'
            val = [key, pair_counts[key], confidence1, confidence2]
            frequent_pair_array.append(val)
    print(f'\nWITH PAIR FREQUENCY THRESHOLD OF {THRESHOLD_PAIR} THERE ARE OVERALL {len(frequent_pair_array)} ITEMS.')
    print('TOP 5 FREQUENT PAIRS ARE: ')
    frequent_pair_array.sort(key=lambda row: row[1], reverse=True)
    for item in frequent_pair_array[0:5]:
        print(
            f'Pair name: {item[0]}, support: {item[1]}/{num_items}, confidence(A=>B): {item[2]}, confidence(B=>A): {item[3]}')

    for transaction in new_transactions:
        for index1 in range(len(transaction) - 2):
            if transaction[index1] not in frequent_items:
                continue
            for index2 in range(index1 + 1, len(transaction) - 1):
                if transaction[index2] not in frequent_items:
                    continue
                first_pair = normalize_group(transaction[index1], transaction[index2])
                if first_pair not in frequent_pairs:
                    continue
                for index3 in range(index2 + 1, len(transaction)):
                    if transaction[index3] not in frequent_items:
                        continue
                    pairs = generate_pairs(transaction[index1], transaction[index2], transaction[index3])
                    if any(pair not in frequent_pairs for pair in pairs):
                        continue
                    triple = normalize_group(transaction[index1], transaction[index2], transaction[index3])
                    triple_counts[triple] += 1
    frequent_triples = set()
    frequent_triple_array = []
    for key in triple_counts:
        if triple_counts[key] > THRESHOLD_TRIPLE:
            frequent_triples.add(key)
            val = [key, triple_counts[key]]
            frequent_triple_array.append(val)

    print(
        f'\nWITH TRIPLE FREQUENCY THRESHOLD OF {THRESHOLD_TRIPLE} THERE ARE OVERALL {len(frequent_triple_array)} ITEMS.')
    frequent_triple_array.sort(key=lambda row: row[1], reverse=True)
    print('TOP 5 FREQUENT TRIPLES ARE: ')
    for triple in frequent_triple_array[0:5]:
        print(f'Triple name: {triple[0]}, support: {triple[1]}/{num_items}')


if __name__ == '__main__':
    # main()
    count_top10_customers()