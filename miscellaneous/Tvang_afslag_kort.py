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


df = gpd.read_file("../map_data/KOM_MULTIPART.shp")
data = pd.read_excel("Regression_af_hver_enkelt_kommune.xlsx")
df = df.drop(54, axis = 0).reset_index()
#df = df.sort_values(by="KOMNAVN")
#data = data.sort_values(by="Kommune")
df["KOMNAVN"] = df["KOMNAVN"].replace("Aarhus","Århus")
#remove christianssø

tmp=[]
for index,row in data.iterrows():
    tmp.append((row["Kommune"],row["Afslag"]))

tmp = dict(tmp)
data_to_add=[]
for name in df["KOMNAVN"]:
    for key in tmp:
        if (name==key):
            data_to_add.append(tmp[key])
df["AFSLAG"] = pd.DataFrame(data_to_add)



df["AFSLAG"].replace(np.NaN,48.46,inplace=True)
df["AFSLAG"].replace(-6.82000,np.NaN,inplace=True)
df["AFSLAG"].replace(-2.88000,np.NaN,inplace=True)
df["AFSLAG"].replace(-18.32000,np.NaN,inplace=True)
df["AFSLAG"].replace(-3.60000,np.NaN,inplace=True)


#plot map
#"{%.2%%}"
cmap = truncate_colormap(cmap = plt.get_cmap("Reds"))
df.to_crs(epsg=4326).plot(column="AFSLAG", cmap = cmap, legend = True,
        missing_kwds={
        "color": "lightgrey",
        "edgecolor": "blue",
        "hatch": "///",
        "label": "Missing values",
    })
plt.title("Procentvis afslag i pris på tvangsauktion")
plt.xlabel("Længdegrad")
plt.ylabel("Breddegrad")


plt.show()


