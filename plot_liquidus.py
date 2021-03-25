import pandas as pd

def input_data():
    df = pd.read_csv("results.csv")
    print("Input SiO2 composition (wt%)")
    wtsi = float(input())
    print("Input oxide buffer")
    fo2 = input()
    df = df[ ( df["SiO2"] == wtsi ) & ( df["fO2"] == fo2 ) ]
    return df

def main():
    df_raw = input_data()
    
    df = df[ ( df["P (kbars)"] == 6 ) & ( df["H2O"] == 2 ) ]
    list_phase = [ "Apt", "Cpx", "Grt", "Hbl", "Olv", "Opx", "Plg", "Spl", "Wht"]
    df_temp = df["T (C)"]
    list_column = []
    for phase in list_phase:
        volphase = "vol" + phase + " (vol%)"
        list_column.append(volphase)
    df_phase = df[ list_column ]
    for idx in range(len(df_phase)):
        for i, phase in enumerate(list_column):
            value = df_phase[phase].iloc[idx]
            # nanのときは自分と比較するとFalseを返すことを利用
            if value != value:
                pass
            else:
                break
        if value != value:
            pass
        else:
            break
    print(list_phase[i], df[idx])
    
    """
    list_idx = [ "idx_apt", "idx_cpx", "idx_grt", "idx_hbl", "idx_olv", "idx_opx",
    "idx_plg", "idx_spl", "idx_wht" ]
    
    list_select = []
    for i, phase in enumerate(list_phase):
        list_idx[i] = df[ df[ phase ] > 0 ]
        if len(list_idx[i]) > 0:
            idx = list_idx[i].index[0]
            list_select.append(idx)
        else:
            pass
    idx = min(list_select)
    print(df_raw["T (C)"].iloc[idx])
    """
if __name__ == "__main__":
    main()