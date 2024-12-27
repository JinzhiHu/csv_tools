'''
### NOTE: In this program, DF refers to F_CSV_DF, which is  ###
######### different from the DF in pandas or numpy. ###########

This python script reads and writes the csv file and 
tries to immitate the functionalities of pandas or 
equivalent Data processing packages that runs with python.

How to use:
0) Include 
    
    from csv_tools import * 
    
    before use
    
    Also, don't forget to move csv_tools.py to the corresponding
    directory.

1) Call F_CSV_DF with 

    DF = F_CSV_DF("address", list)
    
    where the generated Data Frame is stored in the DF. 
    list can contain three forms {"Int", "Num", "Anything"} 
    ("Anything" means any possible string except for "Int", "Num")
    Here is an example
    
    DF = F_CSV_DF("test.csv", ["Int", "Num", ""])
    
    in this case, F_CSV_DF will read a file called "test.csv" and treat elements
    in the first col as integers, elements in the second col as floating point numbers, 
    and treat elements in the thrid column as general stirngs.

2) cv_ranking(DATA, rank_on, evaluate_on)
    For dectailed usage, please see the documentation of the function.
    For three of the outputs New_DATA, Returned_quartiles, Returned_Perfs
    
    New_DATA is a DF and can be exported to csv by F_CSV_DF_to_csv
    the look-up function F_CSV_DF_lookup is also applicable.
    
    Returned_quartiles and Returned_Perfs are dictionaries and are
    arranged in suit of my preference of Data processing.
'''
import csv

def F_CSV_DF(address: str, ty: list):
    '''
    Df consumes a string address containing
    the adress of the file to be processed 
    and returned. It returns a dictionary binding df.
    
    We claim that this "Data" type is efficient
    with dictionary powered running time for
    easy items look-up and easy fild names 
    mutation.
    '''
    ## Open file at address
    print('Double check before we start: \nelements of ty should be anyof("Int", "Num") if you are processing numbers')
    DATA = {"Fields": {}, "Rows": {}, "Data": {}}
    with open(address, encoding = "UTF8") as csvfile_r:
        csvreader = csv.reader(csvfile_r)
        row_ind = 0
        for row in csvreader:
            if row_ind == 0:
                field_ind = 0
                for field in row:
                    while field in DATA["Fields"]:
                        ## We use the deliminator "," to 
                        ##   markup different columns
                        ##   under the same "Field" name
                        field += ","
                    DATA["Fields"][field] = field_ind
                    field_ind += 1
            else:
                col_ind = 0
                DATA["Data"][row_ind] = {}
                for entry in row:
                    _ty = ty[col_ind]  ## RECALL: Type
                    if _ty == "Num" and entry != "":
                        entry = float(entry)
                    if _ty == "Int" and entry != "":
                        entry = int(entry)
                    DATA["Data"][row_ind][col_ind] = entry
                    col_ind += 1
                while row[0] in DATA["Rows"]:
                    row[0] += "," ## Same method as before
                DATA["Rows"][row[0]] = row_ind
                    
            row_ind += 1
    return DATA



def F_CSV_DF_to_csv(DATA, name: str):
    Returned_list = []
    L = []
    for field in DATA["Fields"]:
        L.append(field)
    Returned_list.append(L)
    
    for row in DATA["Data"]:
        data = DATA["Data"][row]
        L = []
        for field in DATA["Fields"]:
            L.append(data[DATA["Fields"][field]])
        Returned_list.append(L)
    
    with open(name, "w", encoding = "UTF8", newline = "") as csvfile_w:
        csvwriter = csv.writer(csvfile_w)
        csvwriter.writerows(Returned_list)


        
def F_CSV_DF_lookup(DATA, row, col):
    return DATA["Data"][DATA["Rows"][row]][DATA["Fields"][col]]




def cv_ranking(DATA, rank_on: str, evaluate_on: str):
    '''
    We ignore all null data.
    
    For rank_on, we sort all the data based on this field
    
    We then find the corresponding data in the evaluate_on
    column and return it within another list
    Note that: due to the data discrepancy, we and the nautre
    of ignoring Null data, we cannot gurarantee that all
    numbers in the Returned_Perfs is on-to-one to Returned_quartiles.
    
    In finance, evaluate_on is the period in the future.
    '''
    col_ind = DATA["Fields"][rank_on]
    Sort_on = {}
    count = 0
    for row_ind in DATA["Data"]:
        number = DATA["Data"][row_ind][col_ind]
        if isinstance(number, int) or isinstance(number, float):
            Sort_on[row_ind] = DATA["Data"][row_ind][col_ind]
            count += 1
    Result = dict(sorted(Sort_on.items(), key = lambda item: item[1], reverse = True))
    ################ TESTING #################
    if __name__ == "__main__":
        print(Result)
    ################## END ###################
    New_DATA = {}
    New_DATA["Fields"] = DATA["Fields"]
    New_DATA["Data"] = {}
    New_DATA["Rows"] = {}
    new_row_ind = 1
    Returned_quartiles = {"R1": [], "R2": [], "R3": [], "R4": [], "R5": []}
    Returned_Perfs = {"R1": [], "R2": [], "R3": [], "R4": [], "R5": []}
    quartile = count // 5
    for key in Result:
        New_DATA["Data"][new_row_ind] = DATA["Data"][key]
        ## For Returned_quartiles amd Returned_Perfs
        perf = DATA["Data"][key][DATA["Fields"][evaluate_on]]
        if isinstance(perf, int) or isinstance(perf, float):
            perf = float(perf)
        if 0 <= new_row_ind - 1 < quartile:
            Returned_quartiles["R1"].append(DATA["Data"][key][0])
            if evaluate_on in DATA["Fields"] and isinstance(perf, float):
                Returned_Perfs["R1"].append(perf)
        if quartile <= new_row_ind - 1 < 2 * quartile:
            Returned_quartiles["R2"].append(DATA["Data"][key][0])
            if evaluate_on in DATA["Fields"] and isinstance(perf, float):
                Returned_Perfs["R2"].append(perf)
        if 2 * quartile <= new_row_ind - 1 < 3 * quartile:
            Returned_quartiles["R3"].append(DATA["Data"][key][0])
            if evaluate_on in DATA["Fields"] and isinstance(perf, float):
                Returned_Perfs["R3"].append(perf)
        if 3 * quartile <= new_row_ind - 1 < 4 * quartile:
            Returned_quartiles["R4"].append(DATA["Data"][key][0])
            if evaluate_on in DATA["Fields"] and isinstance(perf, float):
                Returned_Perfs["R4"].append(perf)
        else:
            Returned_quartiles["R5"].append(DATA["Data"][key][0])
            if evaluate_on in DATA["Fields"] and isinstance(perf, float):
                Returned_Perfs["R5"].append(perf)
        ## For New_DATA
        New_DATA["Rows"][DATA["Data"][key][0]] = new_row_ind
        new_row_ind += 1
    return New_DATA, Returned_quartiles, Returned_Perfs


################ TESTING #################

if __name__ == "__main__":
    
    DF = F_CSV_DF("test.csv", [""] + ["Num"]*10000)  ## This is a way to shortcut things
                                                     ##  We don't care about the rest of 
                                                     ##  the list (without corresponding
                                                     ##  data)  
    F_CSV_DF_to_csv(DF, "out.csv")
    
        
    DF = F_CSV_DF("test.csv", [""] + ["Num"]*10000)
    
    print(F_CSV_DF_lookup(DF, "UPDATE_THIS", "UPDATE_THIS"))
    
    
    New_DATA, Returned_quartiles, Returned_Perfs = cv_ranking(DF, "UPDATE_THIS", "UPDATE_THIS")
    
    F_CSV_DF_to_csv(New_DATA, "New_DATA.csv")
    print(Returned_quartiles)
    print(Returned_Perfs)




