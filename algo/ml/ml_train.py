import pandas as pd

# Load the Excel file to examine its structure and contents
file_path = r'Composite_Peel_dataset.xlsx'

# Load the Excel file to examine its structure and contents
xls = pd.ExcelFile(file_path)

# Get the sheet names
sheet_names = xls.sheet_names

# Load each sheet into a dictionary of DataFrames to inspect them
dataframes = {sheet_name: xls.parse(sheet_name) for sheet_name in sheet_names}

# Display basic information about each sheet
data_info = {sheet_name: df.head() for sheet_name, df in dataframes.items()}
sheet_names, data_info

from sklearn.linear_model import LinearRegression, ElasticNetCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.cross_decomposition import PLSRegression
from sklearn.feature_selection import SequentialFeatureSelector
from sklearn.model_selection import LeaveOneOut, cross_val_predict
from sklearn.metrics import r2_score
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm


# Prepare the data
df = dataframes['Sheet1']
X = df.drop(columns=['sAMPLE id', 'COM-Peel'])
Y = df['COM-Peel']

# Store results
results = {}

# Leave-One-Out Cross-Validation
loo = LeaveOneOut()

# Stepwise Linear Regression
model = LinearRegression()
sfs = SequentialFeatureSelector(model, n_features_to_select="auto", direction='forward')
sfs.fit(X, Y)
selected_features = X.columns[sfs.get_support()]

# Refit using selected features
model.fit(X[selected_features], Y)
# Removed the [1:] indexing to avoid IndexError
p_values = sm.OLS(Y, sm.add_constant(X[selected_features])).fit().pvalues
y_pred = cross_val_predict(model, X[selected_features], Y, cv=loo)
r2_stepwise = r2_score(Y, y_pred)

# Regularized Linear Regression (ElasticNet)
elastic_net = ElasticNetCV(cv=loo, random_state=0)
elastic_net.fit(X, Y)
y_pred_en = cross_val_predict(elastic_net, X, Y, cv=loo)
r2_elasticnet = r2_score(Y, y_pred_en)

# Random Forest
rf = RandomForestRegressor(n_estimators=100, random_state=0)
rf.fit(X, Y)
y_pred_rf = cross_val_predict(rf, X, Y, cv=loo)
r2_rf = r2_score(Y, y_pred_rf)
rf_importance = rf.feature_importances_

# Support Vector Regression
svr = SVR()
svr.fit(X, Y)
y_pred_svr = cross_val_predict(svr, X, Y, cv=loo)
r2_svr = r2_score(Y, y_pred_svr)

# Partial Least Squares Regression (PLSR)
pls = PLSRegression(n_components=3)
pls.fit(X, Y)
y_pred_pls = cross_val_predict(pls, X, Y, cv=loo)
r2_pls = r2_score(Y, y_pred_pls)
pls_loadings = pls.x_loadings_[:, 0]

# # Store results
# results = {
#     'stepwise': {'r2': r2_stepwise, 'p_values': p_values},
#     'elastic_net': {'r2': r2_elasticnet},
#     'random_forest': {'r2': r2_rf, 'importance': rf_importance},
#     'svr': {'r2': r2_svr},
#     'pls': {'r2': r2_pls, 'loadings': pls_loadings}
# }

# Assuming variable_names is a list of feature names used in the random forest model
variable_names = ['TS', 'Mod @ 100%', 'BE', 'S029-shear', 'CC-MHP', 'Resin%']  

# Store results
results = {
    'stepwise': {'r2': r2_stepwise, 'p_values': p_values},
    'elastic_net': {'r2': r2_elasticnet},
    'random_forest': {'r2': r2_rf, 'importance': dict(zip(variable_names, rf_importance))},  # Convert to dict
    'svr': {'r2': r2_svr},
    'pls': {'r2': r2_pls, 'loadings': pls_loadings}
}

# Extract R² values for all models
r2_values = {
    'stepwise': results['stepwise']['r2'],
    'elastic_net': results['elastic_net']['r2'],
    'random_forest': results['random_forest']['r2'],
    'svr': results['svr']['r2'],
    'pls': results['pls']['r2']
}

# Extract p-values for stepwise model
stepwise_p_values = results['stepwise']['p_values']

# Extract variable importance for random forest model and sort it
# Now we can safely call items() since importance is a dictionary
rf_importance_sorted = sorted(results['random_forest']['importance'].items(), key=lambda x: x[1], reverse=True)

# Sort R² values from high to low
sorted_r2_values = sorted(r2_values.items(), key=lambda x: x[1], reverse=True)

# Print results in the specified order
print("R² values for all models (sorted from high to low):")
for model, r2 in sorted_r2_values:
    print(f"{model}: {r2}")  # Print each model's R² value on a new line

print("\nP-values for stepwise model:")
print(stepwise_p_values)

print("\nVariable importance for random forest model (sorted):")
for variable, importance in rf_importance_sorted:
    # Here we ensure that the variable names are the actual feature names
    print(f"{variable}: {importance}")



#这里有问题
# Convert pls_loadings to a dictionary if it's a numpy array
#pls_loadings_dict = {f"Component {i+1}": dict(zip(variable_names, loadings)) for i, loadings in enumerate(results['pls']['loadings'])}
pls_loadings_dict = dict(zip(variable_names, results['pls']['loadings']))
# tmp_dict = {}
# for i, loadings in enumerate(results['pls']['loadings']):
#     print("-------", dict(zip(variable_names, loadings)))
#     tmp_dict[f"Component {i+1}"] = dict(zip(variable_names, loadings))

# Print loadings for PLS model
print("\nLoadings for PLS model:")
for component, loadings in pls_loadings_dict.items():
    print(f"  {component}: {loadings}")
    # print(f"{component}:")
    # for variable, loading in loadings.items():
    #     print(f"  {variable}: {loading}")

