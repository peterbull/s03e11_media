# AUTOGENERATED! DO NOT EDIT! File to edit: ../media_campaign_cost.ipynb.

# %% auto 0
__all__ = ['comp', 'path', 'df_train', 'df_test', 'df_comb', 'train_idxs', 'test_idxs', 'dep_var', 'procs', 'cont', 'cat',
           'splits', 'to', 'dls', 'learn', 'xs', 'ys', 'valid_xs', 'valid_ys', 'test_dl', 'preds', 'sample_df']

# %% ../media_campaign_cost.ipynb 4
from fastai.tabular.all import *

# %% ../media_campaign_cost.ipynb 6
try: import fastkaggle
except ModuleNotFoundError:
    !pip install -Uq fastkaggle

from fastkaggle import *

# %% ../media_campaign_cost.ipynb 7
comp = 'playground-series-s3e11'
path = setup_comp(comp, install='fastai')

# %% ../media_campaign_cost.ipynb 10
df_train = pd.read_csv(path/'train.csv', low_memory=False)
df_test = pd.read_csv(path/'test.csv', low_memory=False)

# %% ../media_campaign_cost.ipynb 12
df_comb = pd.concat([df_train, df_test], ignore_index=True)

# %% ../media_campaign_cost.ipynb 14
train_idxs = np.arange(len(df_train))

# %% ../media_campaign_cost.ipynb 15
test_idxs = np.arange(len(df_train), len(df_comb))

# %% ../media_campaign_cost.ipynb 16
dep_var = 'cost'

# %% ../media_campaign_cost.ipynb 17
procs = [Categorify, FillMissing, Normalize]

# %% ../media_campaign_cost.ipynb 18
cont, cat = cont_cat_split(df_comb, max_card=1, dep_var=dep_var)

# %% ../media_campaign_cost.ipynb 19
splits = RandomSplitter(valid_pct=0.2)(range_of(df_train))

# %% ../media_campaign_cost.ipynb 20
df_train = df_comb.iloc[train_idxs]
df_test = df_comb.iloc[test_idxs]

# %% ../media_campaign_cost.ipynb 22
to = TabularPandas(df_train, procs, cat, cont, y_names=dep_var, splits=splits)

# %% ../media_campaign_cost.ipynb 25
dls = to.dataloaders(bs=1024)

# %% ../media_campaign_cost.ipynb 26
learn = tabular_learner(dls, layers=[200,100], metrics=rmse)

# %% ../media_campaign_cost.ipynb 29
xs, ys = to.train.xs, to.train.ys
valid_xs, valid_ys = to.valid.xs, to.valid.ys

# %% ../media_campaign_cost.ipynb 30
test_dl = learn.dls.test_dl(df_test)

# %% ../media_campaign_cost.ipynb 31
preds = learn.get_preds(dl=test_dl)

# %% ../media_campaign_cost.ipynb 34
sample_df = pd.read_csv(path/'sample_submission.csv')

# %% ../media_campaign_cost.ipynb 35
sample_df['cost'] = preds[0]

# %% ../media_campaign_cost.ipynb 36
sample_df.to_csv('submission.csv', index=False)
