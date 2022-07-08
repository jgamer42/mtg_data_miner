import pandas as pd

data = [{"campo1": 1, "campo_comun": 2}, {"campo2": 3, "campo_comun": 2}]

data = pd.DataFrame(data)
print(data)
