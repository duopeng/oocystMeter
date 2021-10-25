import argparse
import sys
import linecache
import os
import pandas as pd
import statistics
from scipy.stats import skew

class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

def parse_args():
    parser= MyParser(description='This script does XXX')
    parser.add_argument('--dir', default="", type=str)
    config = parser.parse_args()
    if len(sys.argv)==1: # print help message if arguments are not valid
        parser.print_help()
        sys.exit(1)
    return config

config = vars(parse_args())

#####################
##      main       ##
#####################    
def main():
    try: 
        ###initialize list to store accmulated info
        data = []

        ###loop through dir
        for filename in os.listdir(config['dir']):
            if (filename.endswith("xlsx")):
                print(f"processing: {filename}")
                #get oocyst count and avg area
                df = pd.read_excel(os.path.join(config['dir'],filename), sheet_name="Oocyst_count")
                oocyst_count = df.loc[0,"Oocyst_count"]
                oocyst_avg_area = df.loc[0,"Average_oocyst_area"]
                #get oocyst area info
                df2 = pd.read_excel(os.path.join(config['dir'],filename), sheet_name="Oocyst_area")
                areas = df2.loc[:,"Oocyst_area"]

                count = len(areas)
                #calculate some statistics of the distriubtion of oocyst area
                Avg_area = 0
                Median_area = 0
                variance = 0
                std_var_area = 0
                skewness_area = 0

                if count>0:
                    Avg_area = sum(areas)/len(areas)
                    Median_area = statistics.median(areas)
                    variance = sum([((x - Avg_area) ** 2) for x in areas]) / len(areas)
                    std_var_area = variance ** 0.5
                    skewness_area = skew(areas)


                data.append([filename.rstrip(".xlsx"),oocyst_count, oocyst_avg_area, Median_area, std_var_area, skewness_area ])
        
        ###create df from list of data
        df = pd.DataFrame(data, columns=['midgut_name','oocyst_count', 'oocyst_avg_area', 'Median_area', 'std_var_area',"skewness_area"])
        print(df)

        #write df to xlsx#
        dirname = os.path.basename(os.path.normpath(config['dir']))
        df.index+=1 #make index start from 1    
        writer = pd.ExcelWriter(f"{dirname}_accumulated_data.xlsx", engine='xlsxwriter')
        df.to_excel(writer, sheet_name='accumulated_data', index_label="Gut instance")

        #format xlxs
        workbook=writer.book
        center = workbook.add_format({'align': 'center'})
        worksheet= writer.sheets['accumulated_data']
        worksheet.set_column('A:E', None, center)
        worksheet.set_column(0, 0, 12)
        worksheet.set_column(1, 1, 35)
        worksheet.set_column(2, 2, 12)
        worksheet.set_column(3, 3, 15)
        worksheet.set_column(4, 4, 12)
        worksheet.set_column(5, 5, 12)
        worksheet.set_column(6, 6, 12)
        writer.save()


    except Exception  as e:
        print("Unexpected error:", str(sys.exc_info()))
        print("additional information:", e)
        PrintException()

##########################
## function definitions ##
##########################
def PrintException():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))

    
if __name__ == "__main__": main()    
