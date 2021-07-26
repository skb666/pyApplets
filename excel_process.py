import sys
from openpyxl import load_workbook

def prcess(excel_fname, data_fname):
    wb = load_workbook(excel_fname)
    error_list = []

    with open(data_fname, 'w') as f_obj:
        for sheet in wb:
            for row in sheet:
                name, phone, cardid = row[:3]
                if name.value and phone.value and cardid.value:
                    f_obj.write(f"{name.value}-{phone.value}-{cardid.value}\n")
                else:
                    error_list.append(row)
        print(f"sucess!\nerror_line: {len(error_list)}")
        
argv_len = len(sys.argv)
if(argv_len < 2):
    print("error: no file to process\nExample: \n\texcel_process.exe data.xlsx\n\texcel_process.exe data.xlsx data.txt")
else:
    excel_fname = sys.argv[1]
    if argv_len >= 3:
        data_fname = sys.argv[2]
    else:
        data_fname = "dates.txt"
    prcess(excel_fname, data_fname)

