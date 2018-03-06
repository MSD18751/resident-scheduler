import pandas as pd

def format_output(inputfile, outputfile):
    with pd.ExcelFile(inputfile) as xls:
        residents = xls.parse('Sheet1').set_index('RESIDENTS')
    units = set()
    for i in range(1, 52):
        inputs = residents.iloc[:, i].unique()
        for j in inputs:
            if j not in units:
                units.add(j)
    residents.to_csv(path_or_buf=outputfile, sep=",")
    return(units)
    

format_output("sample_data/sample_resident_schedule.xlsx", "sample_data/sample_schedule.csv")