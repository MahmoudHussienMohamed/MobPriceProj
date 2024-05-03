import pandas

TRAIN_DS = 'ML/train.csv'
TEST_DS = 'ML/test.csv'
LABEL = 'price_range'
def separate_labels_from_samples(samples):
    labels = tuple(sample.pop(LABEL) for sample in samples) 
    return samples, labels

def get_samples_as_dicts(n_samples, dataset_dir, to_write_file=None):
    ds = pandas.read_csv(dataset_dir)
    samples = ds.sample(n_samples)
    samples = tuple(samples.iloc[i].to_dict() for i in range(n_samples))
    if to_write_file is not None:
        with open(to_write_file, 'wt') as tsif:
            for sample in samples:
                tsif.write(str(sample) + '\n')
            
    return (samples if dataset_dir != TRAIN_DS 
            else separate_labels_from_samples(samples))