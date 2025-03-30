# import joblib
from locale import normalize
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import StandardScaler


def run_cc_pca_model(data):
    
    data = pd.DataFrame(data)
    scaler = StandardScaler() 
    scaled_ccData = scaler.fit_transform(data) 
    norm_ccData = normalize(scaled_ccData)
    
    n_components=2
    pca_final = PCA(n_components=n_components)
    pca_final.fit(norm_ccData)
    pca_ccData = pca_final.fit_transform(norm_ccData)
    c = KMeans(n_clusters = 3).fit_predict(pca_ccData),
    return c



# def save_params(filepath,model):
#   try:
#     joblib.dump(model, filepath)
#   except Exception as e:
#     print(f"An error occurred: {e}")

# def load_params(filepath):
#   try:
#     model = joblib.load(filepath)
#     return model
#   except Exception as e:
#     print(f"An error occurred: {e}")