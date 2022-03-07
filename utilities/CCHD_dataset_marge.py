import pandas
import sys
import csv
import os

argv_list = sys.argv
print(argv_list)
if(len(argv_list) != 4):
    print("usage: python3 CCHD_dataset_marge.py CCHD_result.csv ExtractedFeature.py ExtractedFeature2.py")
    exit()

CCHD_result = pandas.read_csv(argv_list[1])
ExtractedFeature = pandas.read_csv(argv_list[2])
EF_id = ExtractedFeature.loc[:,'ID']

for res_i, result in CCHD_result.iterrows():
    print(result["case_name"])
    for ef_i in range(len(EF_id)):
        
        if result["case_name"] == EF_id[ef_i]:
            temp = {}

            temp['case'] = result["case_name"].split('-')[1] + '_' + result["case_name"].split('-')[0]
            temp['ID'] = result["case_name"].split('-')[1]
            temp['take'] = result["case_name"].split('-')[0]
            temp['diagnosis'] = result["result"]

            temp['Min_PAI_h'] = ExtractedFeature.loc[ef_i,'Min_PAI_h']
            temp['Max_PAI_h'] = ExtractedFeature.loc[ef_i,'Max_PAI_h']
            temp['Median_PAI_h'] = ExtractedFeature.loc[ef_i,'Median_PAI_h']
            temp['Mean_PAI_h'] = ExtractedFeature.loc[ef_i,'Mean_PAI_h']
            temp['Variance_PAI_h'] = ExtractedFeature.loc[ef_i,'Variance_PAI_h']

            temp['Min_SPO2_h'] = ExtractedFeature.loc[ef_i,'Min_SPO2_h']
            temp['Max_SPO2_h'] = ExtractedFeature.loc[ef_i,'Max_SPO2_h']
            temp['Median_SPO2_h'] = ExtractedFeature.loc[ef_i,'Median_SPO2_h']
            temp['Mean_SPO2_h'] = ExtractedFeature.loc[ef_i,'Mean_SPO2_h']
            temp['Variance_SPO2_h'] = ExtractedFeature.loc[ef_i,'Variance_SPO2_h']

            temp['Min_HR_h'] = ExtractedFeature.loc[ef_i,'Min_HR_h']
            temp['Max_HR_h'] = ExtractedFeature.loc[ef_i,'Max_HR_h']
            temp['Median_HR_h'] = ExtractedFeature.loc[ef_i,'Median_HR_h']
            temp['Mean_HR_h'] = ExtractedFeature.loc[ef_i,'Mean_HR_h']
            temp['Variance_HR_h'] = ExtractedFeature.loc[ef_i,'Variance_HR_h']

            temp['Min_PAI_f'] = ExtractedFeature.loc[ef_i,'Min_PAI_f']
            temp['Max_PAI_f'] = ExtractedFeature.loc[ef_i,'Max_PAI_f']
            temp['Median_PAI_f'] = ExtractedFeature.loc[ef_i,'Median_PAI_f']
            temp['Mean_PAI_f'] = ExtractedFeature.loc[ef_i,'Mean_PAI_f']
            temp['Variance_PAI_f'] = ExtractedFeature.loc[ef_i,'Variance_PAI_f']

            temp['Min_SPO2_f'] = ExtractedFeature.loc[ef_i,'Min_SPO2_f']
            temp['Max_SPO2_f'] = ExtractedFeature.loc[ef_i,'Max_SPO2_f']
            temp['Median_SPO2_f'] = ExtractedFeature.loc[ef_i,'Median_SPO2_f']
            temp['Mean_SPO2_f'] = ExtractedFeature.loc[ef_i,'Mean_SPO2_f']
            temp['Variance_SPO2_f'] = ExtractedFeature.loc[ef_i,'Variance_SPO2_f']

            temp['Min_HR_f'] = ExtractedFeature.loc[ef_i,'Min_HR_f']
            temp['Max_HR_f'] = ExtractedFeature.loc[ef_i,'Max_HR_f']
            temp['Median_HR_f'] = ExtractedFeature.loc[ef_i,'Median_HR_f']
            temp['Mean_HR_f'] = ExtractedFeature.loc[ef_i,'Mean_HR_f']
            temp['Variance_HR_f'] = ExtractedFeature.loc[ef_i,'Variance_HR_f']

            temp['Min_slope'] = ExtractedFeature.loc[ef_i,'Min_slope']
            temp['Max_slope'] = ExtractedFeature.loc[ef_i,'Max_slope']
            temp['Median_slope'] = ExtractedFeature.loc[ef_i,'Median_slope']
            temp['Mean_slope'] = ExtractedFeature.loc[ef_i,'Mean_slope']
            temp['Variance_slope'] = ExtractedFeature.loc[ef_i,'Variance_slope']

            temp['Min_delay'] = ExtractedFeature.loc[ef_i,'Min_delay']
            temp['Max_delay'] = ExtractedFeature.loc[ef_i,'Max_delay']
            temp['Median_delay'] = ExtractedFeature.loc[ef_i,'Median_delay']
            temp['Mean_delay'] = ExtractedFeature.loc[ef_i,'Mean_delay']
            temp['Variance_delay'] = ExtractedFeature.loc[ef_i,'Variance_delay']
            print(temp)
            
            if os.path.exists(argv_list[3]):
                save_df = pandas.read_csv(argv_list[3])
                temp_df = pandas.DataFrame(temp, index = [save_df.shape[0]])
                temp_df.to_csv(argv_list[3], mode='a', header=False)
            else:
                temp_df = pandas.DataFrame(temp, index = [0])
                temp_df.to_csv(argv_list[3], mode='a', header=True)



