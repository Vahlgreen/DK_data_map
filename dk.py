import pandas as pd 
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib import colors
from shapely.geometry import Point, Polygon




def truncate_colormap(cmap, minval=0.3, maxval=1.0, n=100):
    new_cmap = colors.LinearSegmentedColormap.from_list(
        'trunc({n},{a:.2f},{b:.2f})'.format(n=cmap.name, a=minval, b=maxval),
        cmap(np.linspace(minval, maxval, n)))
    return new_cmap

kort = gpd.read_file("map_data/KOM_MULTIPART.shp")
data = pd.read_excel("map_data/ejendomspriser.xlsx")


## Clean data
colNames = [str(i) for i in range(data.shape[1])]
data = data.set_axis(colNames,axis=1)
data = data.drop([0, 1, 30],axis=0) # fjern unødvendige rækker samt bornholm
data = data.drop(["0","1"], axis=1) # fjern unødvendige kolonner
kort = kort.drop(0,axis = 0) #fjern bornholm
kort = kort.drop(54, axis = 0) #fjern christianssø
data["2"] = data["2"].replace("Århus","Aarhus")
data["2"] = data["2"].replace("Høje-Taastrup","Høje Taastrup")
data = data.reset_index(drop = True)
kort = kort.reset_index(drop = True)

# add data to geodataframe
tmp = []
data_to_add = []
for index,row in data.iterrows():
    tmp.append((row["2"],row["119"]))
tmp = dict(tmp)

for name in kort["KOMNAVN"]:
    for key in tmp:
        if(name==key):
            if(type(tmp[key]) is int):
                data_to_add.append(tmp[key])
            else:
                data_to_add.append(7500)

kort["PRISER"] = pd.DataFrame(data_to_add)
kort["FARVER"] = pd.DataFrame(np.log(data_to_add)) #take log to make color ranges more suitable

#plot map
cmap = truncate_colormap(cmap = plt.get_cmap("Reds"))
kort.to_crs(epsg=4326).plot(column="FARVER",cmap = cmap,legend = True)
plt.title("Fordeling for log af kvadratmeter pris (kr) på kommuneplan ")
plt.xlabel("Længdegrad")
plt.ylabel("Breddegrad")
plt.show()
