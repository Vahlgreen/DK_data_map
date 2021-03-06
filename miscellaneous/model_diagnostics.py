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


column = "lambda_SOU"

map_df = gpd.read_file("../map_data/KOM_MULTIPART.shp")
data_to_plot_df = pd.read_csv("data/Alle_lambda.csv")
#data_to_plot_df = pd.read_csv("data/Alle_MSE.csv")
map_df["kommune"] = map_df["KOMNAVN"].str.lower()
data_to_plot_df["kommune"] = data_to_plot_df["kommune"].str.lower()
data_to_plot_df[f"{column}_log"]=np.log2(data_to_plot_df[f"{column}"])
data_to_plot_df[f'{column}'] = data_to_plot_df[f'{column}'].apply(lambda x : x if x>0 else np.nan)

### Her ændres kort dataframe
map_df = map_df.drop(54, axis = 0).reset_index(drop=True)
map_df["kommune"] = map_df["kommune"].replace("aarhus", "århus")
map_df = map_df.sort_values(by="kommune",ignore_index=True)
data_to_plot_df = data_to_plot_df.sort_values(by="kommune",ignore_index=True)

#set outliers to nan (MSE)
#data_to_plot_df.at[19,"err_SOU"]=np.nan #6.004
#data_to_plot_df.at[19,"err_EOU"]=np.nan #2.26119
#data_to_plot_df.at[19,"err_system"]=np.nan #31.78
#data_to_plot_df.at[74,"err_system"]=np.nan #122.69 samsø
#data_to_plot_df.at[56,"err_system"]=np.nan #20.518 læsø
#data_to_plot_df.at[14,"err_system"]=np.nan # 5.5 fanø

##### Her ændres dataen der skal plottes
tmp=[]
for index,row in data_to_plot_df.iterrows():
    tmp.append((row["kommune"],row[f"{column}"]))


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

fig,ax = plt.subplots()

cmap = truncate_colormap(cmap = plt.get_cmap("Reds"))
map_df.to_crs(epsg=4326).plot(column=data_to_plot_df[f"{column}"],ax=ax, cmap = cmap, legend = True, missing_kwds={
        "color": "lightgrey",
        #"edgecolor": "blue",
        #"hatch": "///",
        "label": "Missing values",
    })
plt.title(f"MSE values of the {column.split('_')[1]} process")
#plt.xlabel("Længdegrad")
#plt.ylabel("Breddegrad")
plt.axis('off')

#plt.xticks(color="white")

plt.show()


