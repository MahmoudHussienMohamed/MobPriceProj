from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
import pandas as pd
import numpy as np

LABEL = 'price_range'

quick_dict = lambda strategy : {'missing_values': np.nan, 'strategy': strategy}

mean_args   = quick_dict("mean")
median_args = quick_dict("median")
mfreq_args  = quick_dict("most_frequent")
const_args  = quick_dict("constant")
const_args.update({"fill_value": 0})

mean_cols   = ['m_dep', 'mobile_wt', 'px_height', 'px_width', 'sc_h', 'sc_w']
median_cols = ['fc', 'pc', 'n_cores']
const_cols  = ['four_g']
mfreq_cols  = ['int_memory', 'ram']

cols_args_pair = (
    (mean_cols,   mean_args),
    (median_cols, median_args),
    (mfreq_cols,  mfreq_args),
    (const_cols,  const_args)
)

class CustomImputer(BaseEstimator, TransformerMixin):
    def __init__(self, columns_args_pairs):
        self.columns = None
        self.imputers = []
        self.imputation_columns = []
        self.columns_args_pairs = columns_args_pairs
        for cols, args in self.columns_args_pairs:
            self.imputers.append(SimpleImputer(**args))
            self.imputation_columns.append(cols)
    def fit(self, X, y=None):
        self.columns = X.columns
        for imputer, cols in zip(self.imputers, self.imputation_columns):
            imputer.fit(X[cols], y)
        return self
    def transform(self, X):
        Xtransformed = X.copy()
        for imputer, cols in zip(self.imputers, self.imputation_columns):
            Xtransformed[cols] = imputer.transform(Xtransformed[cols])
        return pd.DataFrame(columns=self.columns, data=Xtransformed)

##################################################################################################

def ADD(x, y):
    return x + y

def MUL(x, y):
    return x * y

def DIV(x, y):
    return x / (y + 1)  # +1 to avoid dividing by zero

class MakerHelper:
    def __init__(self, result_column, columns, operation, prefix='___'):
        self.res = prefix + result_column                # Add `prefix` before the result column name to distinguish it from the original data cloumns 
        self.cols = columns
        self.oper = operation
    def applyto(self, df):
        tmp = df[self.cols[0]]
        for i in range(1, len(self.cols)):
            tmp = self.oper(tmp, df[self.cols[i]])
        df[self.res] = tmp

class FeaturesMaker(BaseEstimator, TransformerMixin):
    def __init__(self, params):
        self.params = params
        self.makers = []
    def fit(self, X, y=None):
        for res_col, cols, op in self.params:
            self.makers.append(MakerHelper(result_column=res_col, columns=cols, operation=op))
        return self
    def transform(self, X):
        Xtransformed = X.copy()
        for maker in self.makers:
            maker.applyto(Xtransformed)
        return Xtransformed

combined_features = (
    ('network_compatibility', ('four_g', 'three_g', 'wifi', 'blue', 'dual_sim'), ADD),
    ('sc_aspect_ratio', ('sc_h', 'sc_w'), DIV),
    ('battery_capacity', ('battery_power', 'talk_time'), MUL),
    ('tc', ('fc', 'pc'), ADD),
    ('n_cores_over_ram', ('n_cores', 'ram'), DIV),
    ('sc_sz', ('sc_w', 'sc_h'), MUL),
    ('mob_sz', ('___sc_sz', 'm_dep'), MUL),
    ('px_density', ('px_width', 'px_height'), MUL),
    ('px_density', ('___px_density', '___sc_sz'), DIV),
    ('screen_points', ('___px_density', 'touch_screen'), MUL),
)

##################################################################################################

class FeatureSelector(BaseEstimator, TransformerMixin):
    '''
    Transformer selects top features according to their correlation to the label `'price'` column. 
    If `corr`[`feature`] >= `threshold` or `corr`[`feature`] <= `-threshold` then it will be selected.
    '''
    def __init__(self, labels, threshold=0.02):
        self.threshold = threshold
        self.labels = labels
    def most_important_features(self, X):
        X[LABEL] = self.labels 
        corr_matrix = X.corr()
        corr = corr_matrix[LABEL]
        features = corr.index
        return [
            feature for feature in features 
                if feature != LABEL and (
                    corr[feature] >= self.threshold or corr[feature] <= -self.threshold
                    ) 
        ]
    def fit(self, X, y=None):
        self.high_corr_features = self.most_important_features(X.copy())
        return self
    def transform(self, X):
        return X[self.high_corr_features]

##################################################################################################


class CustomSTDScaler(StandardScaler):
    '''
    `StandardScaler` scaling a specific columns (columns that have unique values number <= threshould) and returns pandas.DataFrame 
    instead of numpy array when transform is invoked.
    '''
    def __init__(self, values_uniqueness_threshold=10):
        self.columns = None
        self.keep_features = None
        self.values_uniqueness_threshold = values_uniqueness_threshold
        StandardScaler.__init__(self)
    def fit(self, X, y=None):
        self.keep_features = [col for col in X if X[col].nunique() <= self.values_uniqueness_threshold]
        self.columns = [col for col in X if col not in self.keep_features]
        StandardScaler.fit(self, X[self.columns])
        return self
    def transform(self, X):
        Xtransformed = X.copy()
        Xtransformed[self.columns] = StandardScaler.transform(self, X[self.columns])
        return Xtransformed
