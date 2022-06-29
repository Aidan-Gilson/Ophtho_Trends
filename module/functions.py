import pandas as pd

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