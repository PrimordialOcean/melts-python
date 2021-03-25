import pandas as pd

def main():
    # データの読み込み
    filename = 'start.csv'
    df = pd.read_csv(filename)    
    # 選択リスト
    list_bulk = ['SiO2', 'TiO2', 'Al2O3', 'FeO', 'MnO', 'MgO', 'CaO', 'Na2O', 'K2O', 'P2O5']
    list_water = ['H2O']
    list_tempc = ['InitialTempC', 'FinalTempC']
    list_pressure = ['InitialPbar', 'FinalPbar']
    list_delta = ['dT', 'dP', 'dP/dT']
    list_oxidebuffer = ['fO2']
    # DataFrameを分割
    df_bulk = df[list_bulk].dropna(how='all')
    df_water = df[list_water].dropna(how='all')
    df_tempc = df[list_tempc].dropna(how='all')
    df_pressure = df[list_pressure].dropna(how='all')
    df_delta = df[list_delta].dropna(how='all')
    df_oxidebuffer = df[list_oxidebuffer].dropna(how='all')
    # 組み合わせを取得
    for index_bulk in range(len(df_bulk)):
        df_bulk_tmp = df_bulk.query('index == @index_bulk')
        for index_water in range(len(df_water)):
            df_water_tmp = df_water.query('index == @index_water')
            for index_tempc in range(len(df_tempc)):
                df_tempc_tmp = df_tempc.query('index == @index_tempc')
                for index_pressure in range(len(df_pressure)):
                    df_pressure_tmp = df_pressure.query('index == @index_pressure')
                    for index_delta in range(len(df_delta)):
                        df_delta_tmp = df_delta.query('index == @index_delta')
                        for index_oxidebuffer in range(len(df_oxidebuffer)):
                            df_oxidebuffer_tmp = df_oxidebuffer.query('index == @index_oxidebuffer')
                            if ( index_bulk == 0 and index_water == 0 and index_tempc == 0 \
                                and index_pressure == 0 and index_delta == 0 and index_oxidebuffer == 0 ):
                                df = pd.concat([df_bulk_tmp, df_water_tmp, df_tempc_tmp, df_pressure_tmp, \
                                df_delta_tmp, df_oxidebuffer_tmp], axis=1)
                            else:
                                df_tmp = pd.concat([df_bulk_tmp.reset_index(drop=True), \
                                df_water_tmp.reset_index(drop=True), df_tempc_tmp.reset_index(drop=True), \
                                df_pressure_tmp.reset_index(drop=True), df_delta_tmp.reset_index(drop=True), \
                                df_oxidebuffer_tmp.reset_index(drop=True)], axis=1)
                                df = df.append(df_tmp).reset_index(drop=True)
    # CSVファイルを出力
    df.to_csv('input.csv')

if __name__ == "__main__":
    main()