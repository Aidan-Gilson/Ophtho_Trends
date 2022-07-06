import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import r2_score




def total_pull(condition, month, years, r, folder):
    years_all = [x for x in range(years[0], years[-1]+1)]
    months = ["0"+str(x) for x in range(1,10)] + [str(x) for x in range(10,13)]
    dates = [str(years_all[0])+"-"+months[y]+"-01" for y in range(month-1, 12)]
    if len(years_all) >=2:
        dates += [str(years_all[-1])+"-"+months[y]+"-01" for y in range(0,month)]
    if len(years_all) >2:
        for x in range(years_all[1], years_all[-1]):
            dates += [str(x)+"-"+months[y]+"-01" for y in range(0,12)]
    dates = sorted(dates)
    
    df = pd.read_csv(folder + "/"+condition+"_"+r+".csv")
    if df.empty:
        return pd.DataFrame(None, columns=[r], index=[condition])
    try:
        df = df.drop("isPartial", axis = 1)
    except:
        return None
    df = df[df["date"].isin(dates)].mean(numeric_only=True)
    df = pd.DataFrame(df, columns = [r])
    return(df)


def pull_all_regions(condition, month, years, regions, folder):
    all_data = total_pull(condition, month, years, regions[0], folder)
    for r in regions[1:]:
        data_next = total_pull(condition, month, years, r, folder)
        if data_next is not None:
            all_data[r] = data_next[r]
        else:
            all_data[r] = 0
    return all_data

def pull_all(month, years, regions, folder):
    kw_list = ["cataract", "diabetic retinopathy", "macular degeneration", "uveitis"]
    all_data = pull_all_regions("glaucoma", month, years, regions, folder)
    for x in kw_list:
        all_data = pd.concat([all_data, pull_all_regions(x, month, years, regions, folder)])
    return all_data


def plot_us(df, df_regions, state_level_col, x_data, y_data, cmap_data, plot_title, x_label, y_label, x1, y1, x2, y2, region_map = "", region_x = "", region_y = "", region_title = ""):
    
    plot_region = False
    if region_map == "":
        region_map = state_level_col + '_Region'
        plot_region = True
    if region_x == "":
        region_x = x_data + "_Region"
    if region_y == "":
        region_y = y_data + "_Region"
    if region_title == "":
        region_title = plot_title + " Region"


    # Geo Map by State
    fig, ((ax1, ax3), (ax2, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    ax1.axis('off')
    ax1.set_title(plot_title, fontdict={'fontsize': '15', 'fontweight' : '3'})
    df.plot(column=state_level_col,
            cmap=cmap_data,
            linewidth=0.9,
            ax=ax1,
            edgecolor='0',
            legend=True)

    #Geo Map by Region
    ax2.axis('off')
    ax2.set_title(region_title, fontdict={'fontsize': '15', 'fontweight' : '3'})
    df.plot(column=region_map,
            cmap=cmap_data,
            linewidth=0.3,
            ax=ax2,
            edgecolor='0',
            legend=True)

    if plot_region:
        df_regions.boundary.plot(
                linewidth=1,
                ax=ax2,
                edgecolor='0')

    #Scatter by State
    ax3.set_title('States', fontdict={'fontsize': '15', 'fontweight' : '3'})
    ax3.set_xlabel(x_label)
    ax3.set_ylabel(y_label)
    x = df[x_data]
    y = df[y_data]

    ax3.plot(x,y,"+", 
        ms=10, 
        mec="k",)

    z = np.polyfit(x, y, 1)
    y_hat = np.poly1d(z)(x)

    ax3.plot(x, y_hat, 
        "r--",
        lw=1)
    text = f"$y={z[0]:0.3f}\;x{z[1]:+0.3f}$\n$R^2 = {r2_score(y,y_hat):0.3f}$"
    ax3.text(x1, y1, text,
        fontsize=14)

    #Scatter by Region
    ax4.set_title('Region', fontdict={'fontsize': '15', 'fontweight' : '3'})
    ax4.set_xlabel(x_label)
    ax4.set_ylabel(y_label)
    x = df[region_x]
    y = df[region_y]

    ax4.plot(x,y,"+", 
        ms=10, 
        mec="k",)

    z = np.polyfit(x, y, 1)
    y_hat = np.poly1d(z)(x)

    ax4.plot(x, y_hat, 
        "r--",
        lw=1)
    text = f"$y={z[0]:0.3f}\;x{z[1]:+0.3f}$\n$R^2 = {r2_score(y,y_hat):0.3f}$"
    ax4.text(x2, y2, text,
        fontsize=14, verticalalignment='top')
    return fig, ((ax1, ax3), (ax2, ax4))


