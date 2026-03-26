import numpy as np

from model import IntentionSharingModel

space_size = np.array([[0,100], [0,100]])
rng = np.random.default_rng()
model = IntentionSharingModel(space_size=space_size, rng=rng)

for i in range(100):
    model.step()