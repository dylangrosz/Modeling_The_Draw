import sys
import pandas as pd
import numpy as np

# I am a [gender] applying as [applyType]. If I apply for a [roomType] in [resName] using tier [tierNum], what are my chances of getting in?

_, gender_raw, applyType_raw, roomType_raw, resName_raw, tierNum_raw = sys.argv

gender_raw_to_gender = {
    "male":"m",
    "female":"f",
    "not applicable":"n"
}
gender = gender_raw_to_gender[gender_raw]

roomType_to_res_name = {
    "any room":"Any",
    "a 1 room single":"1 Room Single",
    "a 1 room double":"1 Room Double",
    "a 1 room double (focus)":"1 Room Double (focus)",
    "a 2 room double":"2 Room Double",
    "a 2 room double (focus)":"2 Room Double (focus)",
    "a triple":"Triple",
    "a standard room":"Standard",
    "a premium room":"Premium",
    "substance free housing":"Substance Free Housing",
    "ethnic housing":"ETHNIC"
}
roomType = roomType_to_res_name[roomType_raw]
if roomType == "ETHNIC":
    ethnic_map = {
        "Ujamaa":"B",
        "Hammarskjold":"I",
        "Muwekma":"N",
        "Zapata":"C",
        "Okada":"A",
    }
    roomType = "Ethnic " + ethnic_map[resName_raw]
resID = str(roomType) + "," + resName_raw

applyType_to_typeCol = {
    "an individual":"individual",
    "a group of 2":"group_2",
    "a group of 3":"group_3",
    "a group of 4":"group_4"
}
typeCol = applyType_to_typeCol[applyType_raw]
tierNum = int(tierNum_raw)

h_data_c_path = "housingData1718_cleaned.csv"
h_data = pd.read_csv(h_data_c_path)
yearList = list(h_data["year"].unique())

# Get chances according to just last year
print(resID)
print(h_data["res_name_edited"])
if resID in h_data["res_name_edited"].unique():
    score_ceiling = tierNum * 1000
    score_floor = score_ceiling - 999
    h_data_2018 = h_data[h_data.year == 2018]
    if gender != "n":
        h_data_sliced = h_data_2018[h_data_2018.sex == gender]
        cutoff_i = h_data_sliced.index[h_data_sliced.res_name_edited == resID].tolist()[0]
        cutoff = h_data_sliced.loc[cutoff_i, typeCol]
    else:
        h_data_sliced = h_data_2018
        cutoff_is = h_data_sliced.index[h_data_sliced.res_name_edited == resID].tolist()
        cutoff = (h_data_sliced.loc[cutoff_is[0], typeCol] + h_data_sliced.loc[cutoff_is[1], typeCol]) / 2
    output = ""
    if cutoff > score_ceiling:  output = ">99%"
    elif cutoff < score_floor:  output = "<0.1%"
    else: output = (cutoff - score_floor) / 1000
    print("Given last year's Housing Draw, you have a %s chance of getting %s in %s" % (str(round(output * 100, 3)) + "%", roomType_raw, resName_raw))
else:
    print("This room does not exist according to last year's Draw.")