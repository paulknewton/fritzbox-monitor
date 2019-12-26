import pickle


def change_pickle_protocol(filepath, protocol=2):
    with open(filepath, 'rb') as f:
        obj = pickle.load(f)
    with open(filepath, 'wb') as f:
        pickle.dump(obj, f, protocol=protocol)


if __name__ == '__main__':
    pkl_filenmae = "expected_df.pkl"

    print("Converting %s from new pickle format to old pickle format")
    change_pickle_protocol("expected_df.pkl")
