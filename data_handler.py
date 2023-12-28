import pandas as pd
import math
import numpy
import pathlib
from main import MyApp



#filename_srk = 'QFileDialog.text'
class DataHandler:

    filename_suz = MyApp.open_csv_file()
    countstr = 0
    stringdate = 8

    col = ['date_time', 'I1', 'I2', 'I3', 'I4', 'N']

    data_hours_suz_filth = pd.DataFrame(columns=col)

    row_in_dataframe = 0

    with open(filename_suz, 'r') as myfile:
         for line in myfile:
            countstr += 1

            if countstr == stringdate:
                date = line[13:23]
            if line.startswith(("0", "1", "2")):

                splitted_line = line.split()
                print(splitted_line)

                for id, item in enumerate(col):

                    if "E" in splitted_line[id]:
                        to_decimal = "{:.8f}".format(float(splitted_line[id].replace(",", ".")))
                        data_hours_suz_filth.at[row_in_dataframe, item] = to_decimal
                    else:
                        data_hours_suz_filth.at[row_in_dataframe, item] = date + " " + splitted_line[0][0:8]

                row_in_dataframe += 1


    Sum_N = data_hours_suz_filth['N'].astype(float).sum()
    print(Sum_N)

    JobHour = len(data_hours_suz_filth[data_hours_suz_filth['I2'].astype(float)>=float(40)])
    print(JobHour)

    data_hours_suz_filth['deltaT'] = data_hours_suz_filth['I2'].astype(float) - data_hours_suz_filth['N'].astype(float)


    data_day_suz = (data_hours_suz_filth
                    .drop(['date_time'], axis=1)
                    .astype(float)
                    .mean()
                    .to_frame()
                    .T
                    )


    data_day_suz['date_time'] = date
    col_date = data_day_suz.pop("date_time")
    data_day_suz.insert(0, col_date.name, col_date)


    #col = df.pop("Mid")
    #df.insert(0, col.name, col)

    #def move_column_inplace(df, col, pos):
    #    col = df.pop(col)
    #    df.insert(pos, col.name, col)

    print(data_hours_suz_filth.to_string())
    print(data_day_suz)

    #
    # con = sqlite3.connect("data_handler.db")
    # cur = con.cursor()
    #
    # cur.execute("CREATE TABLE IF NOT EXISTS data_hours_suz (ID integer primary key AUTOINCREMENT, date_time timestamp, I1 decimal, I2 decimal, I3 decimal, I4 decimal, N decimal, deltaT decimal")
    # cur.execute("CREATE TABLE IF NOT EXISTS data_day_suz (ID integer primary key AUTOINCREMENT , date_time date , I1 decimal, I2 decimal, I3 decimal, I4 decimal, N decimal, deltaT decimal")
    #
    # data_hours_suz_filth.to_sql(name='data_hours_suz', con=con, if_exists='append', index=False)
    # data_day_suz.to_sql(name='data_day_suz', con=con, if_exists='append', index=False)
    #
    # con.commit()
    # con.close()