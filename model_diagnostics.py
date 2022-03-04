import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib import colors

def truncate_colormap(cmap, minval=0.3, maxval=1.0, n=100):
    new_cmap = colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))
    return new_cmap


map_df = gpd.read_file("KOM_MULTIPART.shp")
data_to_plot_df = pd.read_csv("Alle_MSE.csv")

map_df["kommune"] = map_df["KOMNAVN"].str.lower()
data_to_plot_df["kommune"] = data_to_plot_df["kommune"].str.lower()
data_to_plot_df["err_SOU_log"]=np.log2(data_to_plot_df["err_SOU"])


### Her ændres kort dataframe
map_df = map_df.drop(54, axis = 0).reset_index(drop=True)
map_df["kommune"] = map_df["kommune"].replace("aarhus", "århus")
map_df = map_df.sort_values(by="kommune",ignore_index=True)
data_to_plot_df = data_to_plot_df.sort_values(by="kommune",ignore_index=True)
#remove christianssø


##### Her ændres dataen der skal plottes
tmp=[]
for index,row in data_to_plot_df.iterrows():
    tmp.append((row["kommune"],row["err_SOU"]))


##### Her tilføjes dataen til kort df
tmp = dict(tmp)
data_to_add=[]
for name in map_df["kommune"]:
    for key in tmp:
        if (name==key):
            data_to_add.append(tmp[key])

map_df["err"] = pd.DataFrame(data_to_add)





####Her plottes kortet
#"{%.2%%}"
cmap = truncate_colormap(cmap = plt.get_cmap("Reds"))
map_df.to_crs(epsg=4326).plot(column=data_to_plot_df["err_SOU_log"], cmap = cmap, legend = True,                              missing_kwds={
        "color": "lightgrey",
        "edgecolor": "blue",
        "hatch": "///",
        "label": "Missing values",
    })
plt.title("")
#plt.xlabel("Længdegrad")
#plt.ylabel("Breddegrad")
plt.axis('off')
#plt.xticks(color="white")

plt.show()


