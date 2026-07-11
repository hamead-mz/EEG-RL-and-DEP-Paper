from pickle import load

from configuration.local import directories

def load_learning_rate_gain_loss_ctrl_dep():

    with open(directories['fitted_model_dir'], "rb") as f:
    
        data = load(f)

    learning_rate = {

        'CTRL': {
            'punishment': data["ctl"]["AlphaN"],
            'reward': data["ctl"]["AlphaP"],
        },

        'DEP': {
            'punishment': data["dp"]["AlphaN"],
            'reward': data["dp"]["AlphaP"],
        }
    }

    return learning_rate