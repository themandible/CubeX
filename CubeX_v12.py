# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 14:53:01 2022
@author: Mandible
"""
import scipy as scipy
from scipy.io import loadmat
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
from scipy.stats import pearsonr
import sys
import time
import statsmodels.api as sm
import seaborn as sns
from scipy import stats
class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'
print('Hello and welcome to CubeX, your source for plotting and interpreting single cube data from BiofilmQ .mat files.')
directory = str(input("To begin, please enter directory containing .mat data:"))
csv_directory = directory + '\csv_folder'
analysis_directory = directory + '\Analysis'
agg_df = pd.DataFrame()
file_list = glob.glob(directory + '**/*.mat', recursive=False)
global fig_num
fig_num = 1
# Generates list of .mat files and removes ones that do not meet criteria
while len(file_list) == 0:
    print(color.RED + "It appears no files are present in this directory." + color.END)
    directory = input("To begin, please enter directory containing .mat data files:")
    file_list = glob.glob(directory + '**/*.mat', recursive=False)
for file in file_list:
    if ('data' not in file) or ('Nz' not in file) or ('metadata' in file) or ('parameters') in file:
        file_list.remove(file)
len_file_list = list(np.arange(0, len(file_list)))
file_dict = {len_file_list[i]: file_list[i] for i in range(len(len_file_list))}
user_files = []
num_user_files = list(np.arange(0, len(user_files)))
user_files_dict = {num_user_files[i]: user_files[i] for i in range(len(num_user_files))}
missed_files = []
# import_mat function opens .mat data files, converts the data into pandas dataframes and saves the files as .csv for later use
def import_mat(file):
    print("Importing     ", file,"    please wait...")
    mat = loadmat(file, mdict=None, appendmat=True, squeeze_me=True)
    #create a series from .mat file
    pqr=pd.Series(mat)
    #convert series to dataframe containing record array subdirectories (now stored in df)
    df = pd.DataFrame({'label':pqr.index, 'list':pqr.values})
    #create dataframe from stats array within df
    data = pd.DataFrame(mat['stats'])
    #save as csv file
    data_name = str(os.path.basename(file)) + ".csv"
    try: 
        data.to_csv(csv_directory + "/" + data_name, sep=',', index=True, header=True)
    except:
        print("CSV file already exists in" + csv_directory,'/n')   
# Import_skip section allows users to pick which mat files to import, or skip the import step if files have already been converted
import_skip = input("Enter 'f' to skip import. Enter 'a' to process all files or enter any other key to continue:       ")
if import_skip in ['a','A']:
    user_files = file_list
    new_folder = directory + "\csv_folder"
    try:
        os.mkdir(new_folder)
    except OSError:
        print ("Creation of the directory %s failed or already exists" % new_folder)
    else:
        print ("Successfully created the directory %s " % new_folder)
    for x in user_files:
        import_mat(x)
    pass
if import_skip not in ['f','F','a','A']:
    print("Please choose files for import."+ "\n\n" +"Enter cooresponding number(s) seperated by a comma and press 'enter'."+ "\n\n" +"Press enter to continue.\n\n")
    for key, value in file_dict.items():
        print(key, ' : ', value)
    file_choice = [int(file_choice) for file_choice in input("Enter Desired File Index Number For Import:").split(",")]
    print("File Indicies chosen: ", file_choice)
    for x in file_choice:
        user_files.append(file_dict[x])
    for key, value in user_files_dict.items():
        print('File List:')
        print('\n')
        print(key, ' : ', value,)
        print('\n') 
    #create folder to store all csv files as they are created by the import_mat function
    new_folder = directory + "\csv_folder"
    try:
        os.mkdir(new_folder)
    except OSError:
        print ("Creation of the directory %s failed or already exists" % new_folder)
    else:
        print ("Successfully created the directory %s " % new_folder)
    for x in user_files:
        import_mat(x)
    pass
if import_skip in ['f','F']:
    print("\n\nRespect paid, please proceede with analysis. \n")
    pass
    ##creating multiple df using directory
# generate list of .csv files saved in new file from import section
csv_list = glob.glob(csv_directory + '**/*.csv', recursive=False)
num_csv_list = list(np.arange(0, len(csv_list)))
csv_dict2 = {num_csv_list[i]: csv_list[i] for i in range(len(num_csv_list))}
ffa = []
# Choice allowing user to pick files to work with in the plotting and analysis modules.
print("\n\nPlease choose from imported files:\nThese files will be concatinated into one dataframe for further analysis.")
for key, value in csv_dict2.items():
    print(key, ' : ', value)
file_choice2 = [int(file_choice2) for file_choice2 in input("Desired File(s) for analysis. Choose index Number(s) seperated by a comma: ").split(",")]
for x in file_choice2:
    ffa.append(csv_dict2[x])  
# Analysis_type is the main loop containing the available choices of analysis modules.
# Redirect here after conclution of all modules, to continue session.
# This is where new modules slot in.
def analysis_type():
    analysis_choice = {
    0:'Quit',
    1:'Univariant Histogram',
    2:'Univariant Transformation',
    3:'Bivariate Simple Scatter',
    4:'Bivariate PearsonR',
    5:'Bivariate Reggretion',
    6:'Bivariate Reg XBinning',
    7:'Paired t-test'
    }
    for key, value in analysis_choice.items():
        print(key, ' : ', value)
    input1 = int(input("Please input the number cooresponding to your desired analysis type:"))
    answer = analysis_choice.get(input1)
    print(answer)
    if answer == 'Quit':
        print("Thank you for using CubeX!")
        time.sleep(2)
        sys.exit()
    if answer == 'Univariant Histogram':
        univariant(agg_df)
    if answer == 'Univariant Transformation':
        transform(agg_df)
    if answer == 'Bivariate Simple Scatter':
        bivariant(agg_df)
    if answer == 'Bivariate PearsonR':
        bivariant_pearson(agg_df)
    if answer == 'Bivariate Reggretion':
        seaborn_reg(agg_df)
    if answer == 'Bivariate Reg XBinning':
        seaborn_reg_bin(agg_df)
    if answer == 'Paired t-test':
        ttest(agg_df)
    return answer
def stats_find(file_list):
    #Function to sort through data in chosen files and concatinate into one dataframe
    print("Data from selected files are being concatinated. Please wait. ")
    global agg_df
    global results
    dataframes = []
    for file in file_list:    
        csv_df = pd.read_csv(file)
        dataframes.append(csv_df)
    agg_df = pd.concat(dataframes)
# Stat_save creates folders and saves figures, variables and dataframes.
# Allows all raw and proccessed data to be present in one save location.
# Currently incomplete, though some features still function.
def stat_save(dataframe):
    global ffa
    global stats
    new_folder2 = directory + "\Analysis"
    try:
        os.mkdir(new_folder2)
    except OSError:
        print ("Creation of the directory %s failed or already exists" % new_folder2)
    else:
        print ("Successfully created the directory %s " % new_folder2)
    dataframe.to_csv(analysis_directory + "/" + "Agg_DataFrame.csv" , sep=',', index=True, header=True)
    textfile = open(analysis_directory + "/""Files_Used", "w")
    for element in ffa:
        textfile.write("Files within Aggregate Dataframe:\n\n" + str(element) + "\n")
    textfile2 = open(analysis_directory + "/""Statistics", "w")
    for element in stats:
        textfile2.write("Figure Statistics\nFigureNumber:" + str(element) + "\n")
stats_find(ffa)
print(agg_df)
# Data transformation, a couple of basic methods. Creates a new column in the dataframe. 
# Used well in tandem with univariant histogram
def transform(dataframe):
    global agg_df 
    global analysis_choice_input
    num_columns = list(np.arange(0, len(agg_df.columns)))
    columns = list(agg_df.columns)
    column_names = {num_columns[i]: columns[i] for i in range(len(num_columns))}
    for key, value in column_names.items():
        print(key, ' : ', value)
    param1 = input("Choose parameter for transformation:")
    column_choice1 = column_names.get(int(param1))
    print("You have chosen:", column_choice1,".")
    transf_chce = int(input("Please choose transformation type:\n1:Log\n2:Square Root\n3:Cube Root\n4:Squared\n"))
    if transf_chce == 1:
        agg_df[column_choice1,"Log Transf"] = np.log(agg_df[column_choice1])
    if transf_chce == 2:
        agg_df[column_choice1,'Sqare_rt Transf'] = np.sqrt(agg_df[column_choice1])
    if transf_chce == 3:
        agg_df[column_choice1,'Cube_rt Transf'] = np.cbrt(agg_df[column_choice1])
    if transf_chce == 4:
        agg_df[column_choice1,'Squared Transf'] = (agg_df[column_choice1])**2
    print("Your data have been transformed!\nThis will now be listed under parameter choices")
    return agg_df
    analysis_type()
# Histogram and basic statistics for a dataset chosen by user from the dataframe
def univariant(dataframe):
    print("Welcome to Univiariant Analysis Module!")
    global agg_df
    global fig_num
    global stats
    num_columns = list(np.arange(0, len(agg_df.columns)))
    columns = list(agg_df.columns)
    column_names = {num_columns[i]: columns[i] for i in range(len(num_columns))}
    for key, value in column_names.items():
        print(key, ' : ', value)
    param1 = input("Choose parameter for plotting:")
    column_choice1 = column_names.get(int(param1))
    print("You have chosen:", column_choice1,".")
    fig, ax = plt.subplots(figsize=(12,8))
    ax.hist([agg_df[column_choice1]],edgecolor='green')
    plt.title(str(column_choice1))
    plt.xlabel(str(column_choice1))
    plt.ylabel('Counts')
    ax.tick_params(axis='both', which='major', labelsize=16)
    x_bar = agg_df[column_choice1].mean()
    sd = agg_df[column_choice1].std()
    med = agg_df[column_choice1].median()
    ax.text(3,12,f"mean: {round(x_bar,2)}\ns.d.: {round(sd,2)}",ha='left',va='top', size=18)
    ax.axvline(x_bar, color='red',linestyle='--',linewidth=2)
    print("Mean:", x_bar,"\nStandard Deviation:", sd, "\nMedian:",med)
    stats = [fig_num,x_bar,sd,med]
    stat_save(agg_df)
    plt.savefig(analysis_directory + "/"+ "Figure" + str(fig_num) +'.png', bbox_inches='tight')
    plt.show()
    fig_num += 1
    analysis_type()
# simple scatter to examine relationships between variables
def bivariant(dataframe):
    global agg_df
    global analysis_choice_input
    global fig_num
    global stats
    print("welcome to the Bivariant Analysis Module!")
    num_columns = list(np.arange(0, len(agg_df.columns)))
    columns = list(agg_df.columns)
    column_names = {num_columns[i]: columns[i] for i in range(len(num_columns))}
    for key, value in column_names.items():
        print(key, ' : ', value)
    param1 = column_names[int(input("Parameter 1 choice(X-Axis):  "))]
    param2 = column_names[int(input("Parameter 2 choice(Y-Axis):  "))]
    column_choice1 = column_names.get(param1)
    column_choice2 = column_names.get(param2)
    print("You have chosen:", column_choice1, "and", column_choice2, ".")
    fig, ax = plt.subplots(figsize=(12,8))
    ax.scatter(agg_df[param1],agg_df[param2])
    plt.xlabel(param1)
    plt.ylabel(param2)
    stat_save(agg_df)
    plt.savefig(analysis_directory + "/"+ "Figure" + str(fig_num) +'.png', bbox_inches='tight')
    plt.show()    
    fig_num += 1
    analysis_type()
# Plots a scatter plot and calculates a pearson r coorelation for chosen variables
def bivariant_pearson(dataframe):
    global agg_df
    global analysis_choice_input
    global fig_num
    print("Welcome to the Bivariant Pearson R Analysis Module!")
    time.sleep(1)
    print("Asumptions:\nVariables are both linear\nVariables are both continuous\nAbsence of outliers\nMeasurments are related pairs")
    print("REMINDER: Correlations describe the linear relationship between two variables and DOES NOT describe cause and effect.")
    print("If you are unsure of linearity, please examine data in the Univariant and bivariant scatter modules first")
    time.sleep(2)
    num_columns = list(np.arange(0, len(agg_df.columns)))
    columns = list(agg_df.columns)
    column_names = {num_columns[i]: columns[i] for i in range(len(num_columns))}
    for key, value in column_names.items():
        print(key, ' : ', value)
    param1 = column_names[int(input("Parameter 1 choice(X-Axis):  "))]
    param2 = column_names[int(input("Parameter 2 choice(Y-Axis):  "))]
    print("You have chosen:", param1, "and", param2, ".")
    fig, ax = plt.subplots(figsize=(12,8))
    ax.scatter(agg_df[param1],agg_df[param2])
    plt.xlabel(param1)
    plt.ylabel(param2)
    stat_save(agg_df)
    plt.savefig(analysis_directory + "/"+ "Figure" + str(fig_num) +'.png', bbox_inches='tight')
    plt.show()
    pr,_ = pearsonr(agg_df[param1],agg_df[param2])
    print("PearsonR Correlation Coeficient= ", pr)
    fig_num += 1
    analysis_type()
# Linear Regression module based on user chosen variables. Also plots residuals at request
def seaborn_reg(dataframe):
    global agg_df
    global analysis_choice_input
    global fig_num
    print("Welcome to the Bivariant Linear Regression (via Seaborn) Analysis Module!")
    print("Asumptions:\nVariables are both linear\nVariables are both continuous\nAbsence of outliers\nMeasurments are related pairs")
    print("If you are unsure of linearity, please examine data in the Univariant and Bivariant Scatter Module first")
    num_columns = list(np.arange(0, len(agg_df.columns)))
    columns = list(agg_df.columns)
    column_names = {num_columns[i]: columns[i] for i in range(len(num_columns))}
    for key, value in column_names.items():
        print(key, ' : ', value)
    column_choice1 = int(input("Parameter 1 choice(X-Axis):  "))
    column_choice2 = int(input("Parameter 2 choice(Y-Axis):  "))
    x_var = column_names.get(column_choice1)
    y_var = column_names.get(column_choice2)
    print("You have chosen:", x_var, "and", y_var, ".")
    x = agg_df[x_var]
    y = agg_df[y_var]
    fig, ax1 = plt.figsize=(24,16)
    sns.regplot(x, y, marker='o', color='blue', scatter_kws={'s':1})
    stat_save(agg_df)
    plt.savefig(analysis_directory + "/"+ "Figure" + str(fig_num) +'.png', bbox_inches='tight')
    plt.show()
    answer = input("Would you like to view residual plot? Yes or No:    ")
    if answer in ['y', 'Y', 'yes', 'Yes', 'YES', 'yES','YeS','yeS', 'si', 'oui', 'ja', 'tak', 'da']:
        fig, ax1 = plt.figsize=(24,16)
        sns.residplot(x, y)
        plt.show()
    fig_num += 1
    analysis_type()
# Same as above, however this provides an option to binn data for visualization. Points are mean with CI bars
def seaborn_reg_bin(dataframe):
    global agg_df
    global analysis_choice_input
    global fig_num
    print("Welcome to the Bivariant Linear Regression with binning (via Seaborn) Analysis Module!")
    num_columns = list(np.arange(0, len(agg_df.columns)))
    columns = list(agg_df.columns)
    column_names = {num_columns[i]: columns[i] for i in range(len(num_columns))}
    for key, value in column_names.items():
        print(key, ' : ', value)
    column_choice1 = int(input("Parameter 1 choice(X-Axis):  "))
    column_choice2 = int(input("Parameter 2 choice(Y-Axis):  "))
    x_var = column_names.get(column_choice1)
    y_var = column_names.get(column_choice2)
    print("You have chosen:", x_var, "and", y_var, ".")
    bin_num = int(input("Please choose the number of bins:"))
    x = agg_df[x_var]
    y = agg_df[y_var]
    fig, ax1 = plt.figsize=(24,16)
    sns.regplot(x,y,x_bins=bin_num,scatter_kws={'s':8})
    stat_save(agg_df)
    plt.savefig(analysis_directory + "/"+ "Figure" + str(fig_num) +'.png', bbox_inches='tight')
    plt.show()
    answer = input("Would you like to view residual plot? Yes or No:    ")
    if answer in ['y', 'Y', 'yes', 'Yes', 'YES', 'yES','YeS','yeS', 'si', 'oui', 'ja', 'tak', 'da']:
        fig, ax1 = plt.figsize=(24,16)
        sns.residplot(x, y)
        plt.show()
    fig_num += 1
    analysis_type()
# Plots histogram of two datasets. User will create the seccond dataset from the imported files.
# Performs t-test on chosen datasets and returns the values. 
# Categorical data/plotting was difficult with the format of the datasets
def ttest(dataframe):
    global agg_df
    global analysis_choice_input
    global fig_num
    global ffa2
    global csv_dict2
    global bp_df
    ffa2 = []
    print("Welcome to the T-test module!\n")
    print("This module can perform a paired t-test .\nThis compares the sample means of two normally distributed variables, and determines if they are significantly different")
    print("This module performs a two-tailed t-test by default. Single tail support will be avialble later.")
    print("Please choose files to construct your comparative dataframe:")
    print("\n\nPlease choose from imported files:")
    for key, value in csv_dict2.items():
        print(key, ' : ', value)
    file_choice2 = [int(file_choice2) for file_choice2 in input("Desired File(s) for analysis. Choose index Number(s) seperated by a comma: ").split(",")]
    for x in file_choice2:
        ffa2.append(csv_dict2[x])
    dataframes = []
    for file in ffa2:    
        csv_df = pd.read_csv(file)
        dataframes.append(csv_df)
    # agg_df_sub = pd.concat(dataframes,axis=1)
    agg_df_2 = pd.concat(dataframes)
    num_columns = list(np.arange(0, len(agg_df.columns)))
    columns = list(agg_df.columns)
    column_names = {num_columns[i]: columns[i] for i in range(len(num_columns))}
    for key, value in column_names.items():
        print(key, ' : ', value)
    column_choice1 = int(input("Please choose variable for two-sided t-test:  "))
    num_columns2 = list(np.arange(0, len(agg_df_2.columns)))
    columns2 = list(agg_df_2.columns)
    column_names2 = {num_columns2[i]: columns2[i] for i in range(len(num_columns2))}
    for key, value in column_names2.items():
        print(key, ' : ', value)
    column_choice2 = int(input("Please choose variable (For seccond dataset):  "))
    bar1 = agg_df[column_names.get(column_choice1)]
    bar2 = agg_df_2[column_names2.get(column_choice2)]
    fig, ax = plt.subplots(figsize=(12,8))
    ax.hist([bar1],edgecolor='green')
    plt.title(str("Dataframe1 " + column_names.get(column_choice1)))
    plt.xlabel(str(column_names.get(column_choice1)))
    plt.ylabel('Counts')
    x_bar = bar1.mean()
    sd = bar1.std()
    ax.text(3,12,f"mean: {round(x_bar,2)}\ns.d.: {round(sd,2)}",ha='left',va='top', size=18)
    ax.axvline(x_bar, color='red',linestyle='--',linewidth=2)
    plt.show()
    
    fig, ax = plt.subplots(figsize=(12,8))
    ax.hist([bar2],edgecolor='green')
    plt.title(str("Dataframe2 " + column_names2.get(column_choice2)))
    plt.xlabel(str(column_names2.get(column_choice2)))
    plt.ylabel('Counts')
    x_bar2 = bar2.mean()
    sd2 = bar2.std()
    ax.text(3,12,f"mean: {round(x_bar2,2)}\ns.d.: {round(sd2,2)}",ha='left',va='top', size=18)
    ax.axvline(x_bar, color='red',linestyle='--',linewidth=2)
    plt.show()
    ttest = scipy.stats.ttest_ind(bar1,bar2, equal_var=False)
    print("t-test results:\n\n")
    print(ttest)
    analysis_type()
    
while fig_num >=1:
    analysis_type()

