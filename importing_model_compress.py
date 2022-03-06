import joblib
from model import modeling_sim
import pickle


if __name__ == "__main__":
    model = modeling_sim()
    joblib.dump(model, 'similarity.pkl')