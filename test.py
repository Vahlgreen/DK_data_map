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


df = gpd.read_file("map_data/KOM_MULTIPART.shp")
data = pd.read_excel("Regression_af_hver_enkelt_kommune.xlsx")
df = df.drop(54, axis = 0).reset_index()
df = df.sort_values(by="KOMNAVN")
data = data.sort_values(by="Kommune")
df["KOMNAVN"] = df["KOMNAVN"].replace("Aarhus","Århus")
#remove christianssø


data_neg = data[data["Afslag"]<0].reset_index()
data_pos = data[data["Afslag"]>0].reset_index()

polygons = []
neg_rows = [2,0,1,3]
for i in neg_rows:
    polygons.append(df.iloc[i]["geometry"])
data_neg["geometry"]=polygons


polygons = []
pos_rows = [num for num in range(4,df.shape[0])]

for i in range(4,df.shape[0]):
    polygons.append(df.iloc[i]["geometry"])
data_pos["geometry"] = polygons




#tmp=[]
#for index,row in data.iterrows():
#    tmp.append((row["Kommune"],row["Afslag"]))
#
#tmp = dict(tmp)
#data_to_add=[]
#for name in df["KOMNAVN"]:
#    for key in tmp:
#        if (name==key):
#            data_to_add.append(tmp[key])
#df["AFSLAG"] = pd.DataFrame(data_to_add)



#plot map
cmap = truncate_colormap(cmap = plt.get_cmap("Reds"))
df_pos = gpd.GeoDataFrame(data = data_pos, geometry="geometry",crs="EPSG:4326")
df_neg = gpd.GeoDataFrame(data = data_neg, geometry="geometry",crs="EPSG:4326")
df_pos.to_crs(epsg=4326).plot(column="Afslag", cmap = cmap, legend = True)
df_neg.to_crs(epsg=4326).plot(column="Afslag", cmap = cmap, legend = True)
plt.title("Afslag i pris på tvangsauktion")
plt.xlabel("Længdegrad")
plt.ylabel("Breddegrad")

plt.show()


