import pandas as pd
import os

# 計算用の関数
# 質量(g)と密度(g/cc)から体積(m^3)を計算する
def calc_vol(df):
    mass = df["mass (gm)"]
    density = df["rho (gm/cc)"]
    # ccからm^3に変換
    volume = 10**(-6) * mass / density
    return volume

# An組成を計算する
def calc_an(df):
    wt_caoxide = df["wt% CaO"]
    wt_naoxide = df["wt% Na2O"]
    mol_ca = wt_caoxide / 56.0774
    mol_na = 2 * wt_naoxide / 61.979
    an = 100 * mol_ca / ( mol_ca + mol_na )
    return an

# Mg#を計算する
def calc_mgnum(df):
    wt_feoxide = df["wt% FeO"]
    wt_mgoxide = df["wt% MgO"]
    mol_fe = wt_feoxide / 71.844
    mol_mg = wt_mgoxide / 40.3044
    mgnum = 100 * mol_mg / ( mol_fe + mol_mg )
    return mgnum

# Woを計算する
def calc_wo(df):
    wt_feoxide = df["wt% FeO"]
    wt_mgoxide = df["wt% MgO"]
    wt_caoxide = df["wt% CaO"]
    mol_fe = wt_feoxide / 71.844
    mol_mg = wt_mgoxide / 40.3044
    mol_ca = wt_caoxide / 56.0774
    wo = 100 *mol_ca / ( mol_fe + mol_mg + mol_ca )
    return wo

# 各相の計算
# メルトの処理
def read_df_melt(path):
    # リスト部分に出力する必要のある項目を入れておく
    list_col_melt = [ "Index", "T (C)", "P (kbars)", "log(10) f O2",
    "mass (gm)", "rho (gm/cc)", "volMelt (m^3)", "wt% SiO2", "wt% TiO2", "wt% Al2O3",
    "wt% Fe2O3", "wt% FeO", "wt% MnO", "wt% MgO", "wt% CaO", "wt% Na2O",
    "wt% K2O", "wt% P2O5", "wt% H2O" ]
    df_melt = pd.read_csv(path+"melts-liquid.csv")
    df_melt = df_melt.rename( columns={"liq mass (gm)": "mass (gm)", "liq rho (gm/cc)": "rho (gm/cc)"} )
    df_melt["volMelt (m^3)"] = calc_vol(df_melt)
    df_melt = df_melt[ list_col_melt ]
    return df_melt

# 各鉱物ごとの処理
def read_df_apt(path):
    list_col_apt = [ "Index", "volApt (m^3)" ]
    df_apt = pd.read_csv(path+"apatite.csv")
    df_apt["volApt (m^3)"] = calc_vol(df_apt)
    df_apt = df_apt[ list_col_apt ]
    return df_apt

def read_df_cpx(path):
    list_col_cpx = [ "Index", "volCpx (m^3)", "Mg#Cpx", "WoCpx" ]
    df_cpx = pd.read_csv(path+"clinopyroxene.csv")
    df_cpx["volCpx (m^3)"] = calc_vol(df_cpx)
    df_cpx["Mg#Cpx"] = calc_mgnum(df_cpx)
    df_cpx["WoCpx"] = calc_wo(df_cpx)
    df_cpx = df_cpx[ list_col_cpx ]
    return df_cpx

def read_df_grt(path):
    list_col_grt = [ "Index", "volGrt (m^3)" ]
    df_grt = pd.read_csv(path+"garnet.csv")
    df_grt["volGrt (m^3)"] = calc_vol(df_grt)
    df_grt = df_grt[ list_col_grt ]
    return df_grt

def read_df_hbl(path):
    list_col_hbl = [ "Index", "volHbl (m^3)", "SiHbl (apfu)" ]
    df_hbl = pd.read_csv(path+"hornblende.csv")
    df_hbl["volHbl (m^3)"] = calc_vol(df_hbl)
    molsi = df_hbl["wt% SiO2"] / 60.084
    molal = df_hbl["wt% Al2O3"] / 101.96
    molfe = ( df_hbl["wt% FeO"] \
    + ( 2 * 71.844 / 159.69 ) * df_hbl["wt% Fe2O3"] ) / 71.8464
    molmg = df_hbl["wt% MgO"] / 40.3044
    molca = df_hbl["wt% CaO"] / 56.0774
    oxy_factor = 23 / ( 2 * molsi + 3 * molal + molfe + molmg + molca )
    apfusi = oxy_factor * molsi
    df_hbl["SiHbl (apfu)"] = apfusi
    df_hbl = df_hbl[ list_col_hbl ]
    return df_hbl

def read_df_olv(path):
    list_col_olv = [ "Index", "volOlv (m^3)", "FoOlv" ]
    df_olv = pd.read_csv(path+"olivine.csv")
    df_olv["volOlv (m^3)"] = calc_vol(df_olv)
    df_olv["FoOlv"] = calc_mgnum(df_olv)
    df_olv = df_olv[ list_col_olv ]
    return df_olv

def read_df_opx(path):
    list_col_opx = [ "Index", "volOpx (m^3)", "Mg#Opx", "WoOpx" ]
    df_opx = pd.read_csv(path+"orthopyroxene.csv")
    df_opx["volOpx (m^3)"] = calc_vol(df_opx)
    df_opx["Mg#Opx"] = calc_mgnum(df_opx)
    df_opx["WoOpx"] = calc_wo(df_opx)
    df_opx = df_opx[ list_col_opx ]
    return df_opx

def read_df_plg(path):
    list_col_plg = [ "Index", "volPlg (m^3)", "AnPlg" ]
    df_plg = pd.read_csv(path+"feldspar.csv")
    df_plg["volPlg (m^3)"] = calc_vol(df_plg)
    df_plg["AnPlg"] = calc_an(df_plg)
    df_plg = df_plg[ list_col_plg ]
    return df_plg

def read_df_qz(path):
    list_col_qz = [ "Index", "volQz (m^3)" ]
    df_qz = pd.read_csv(path+"quartz.csv")
    df_qz["volQz (m^3)"] = calc_vol(df_qz)
    df_qz = df_qz[ list_col_qz ]
    return df_qz

def read_df_rhm(path):
    list_col_rhm = [ "Index", "volRhm (m^3)", "IlmRhm" ]
    df_rhm = pd.read_csv(path+"rhm-oxide.csv")
    df_rhm["volRhm (m^3)"] = calc_vol(df_rhm)
    df_rhm["IlmRhm"] = df_rhm["     ilmenite"]
    df_rhm = df_rhm[ list_col_rhm ]
    return df_rhm

def read_df_spl(path):
    list_col_spl = [ "Index", "volSpl (m^3)", "UspSpl", "MgtSpl" ]
    df_spl = pd.read_csv(path+"spinel.csv")
    df_spl["volSpl (m^3)"] = calc_vol(df_spl)
    df_spl["UspSpl"] = df_spl["   ulvospinel"]
    df_spl["MgtSpl"] = df_spl["    magnetite"]
    df_spl = df_spl[ list_col_spl ]
    return df_spl

def read_df_wht(path):
    list_col_wht = [ "Index", "volWht (m^3)" ]
    df_wht = pd.read_csv(path+"whitlockite.csv")
    df_wht["volWht (m^3)"] = calc_vol(df_wht)
    df_wht = df_wht[ list_col_wht ]
    return df_wht

# 体積分率を計算する
def calc_volume(df):
    # "vol"が含まれる列名をリストとして取得
    list_col_vol = [ x for x in df.columns if x[0:3] == "vol"]
    # 合計を計算
    df_sum = df[list_col_vol].sum(axis=1)
    for x in list_col_vol:
        # volPhase (m^3) から単位を"vol%"に変換する
        vol_ratio = x[:-6] + " (vol%)"
        df[vol_ratio] = 100 * df[x] / df_sum
    df["volTotalPh (vol%)"] = 100 - df["volMelt (vol%)"]
    return df

# 入力組成を抽出
def read_input(df, num):
    list_col_input = [ "SiO2", "TiO2", "Al2O3", "FeO", "MnO", "MgO", "CaO",
    "Na2O", "K2O", "P2O5", "H2O", "fO2" ]
    df_input = pd.read_csv("input.csv")
    df_input = df_input[df_input['Title']==num]
    # 先頭行を作成
    added_row = df_input.iloc[0]
    for j in range(len(df)-1):
        df_input = df_input.append(added_row)
    df_input = df_input.reset_index(drop=True)
    df_input = df_input[ list_col_input ]
    return df_input

# 各相の結果を結合
def merge_tbl(path):
    df_melt = read_df_melt(path)
    df = df_melt
    # ファイルが存在するかどうかを例外処理で振り分けている
    # もう少し良い書き方があるかも
    try:
        df_apt = read_df_apt(path)
        df = pd.merge(df, df_apt, on="Index", how="left")
    except:
        pass
    try:
        df_cpx = read_df_cpx(path)
        df = pd.merge(df, df_cpx, on="Index", how="left")
    except:
        pass
    try:
        df_grt = read_df_grt(path)
        df = pd.merge(df, df_grt, on="Index", how="left")
    except:
        pass
    try:
        df_hbl = read_df_hbl(path)
        df = pd.merge(df, df_hbl, on="Index", how="left")
    except:
        pass
    try:
        df_olv = read_df_olv(path)
        df = pd.merge(df, df_olv, on="Index", how="left")
    except:
        pass
    try:
        df_opx = read_df_opx(path)
        df = pd.merge(df, df_opx, on="Index", how="left")
    except:
        pass
    try:
        df_plg = read_df_plg(path)
        df = pd.merge(df, df_plg, on="Index", how="left")
    except:
        pass
    try:
        df_qz = read_df_qz(path)
        df = pd.merge(df, df_qz, on="Index", how="left")
    except:
        pass
    try:
        df_rhm = read_df_rhm(path)
        df = pd.merge(df, df_rhm, on="Index", how="left")
    except:
        pass
    try:
        df_spl = read_df_spl(path)
        df = pd.merge(df, df_spl, on="Index", how="left")
    except:
        pass
    try:
        df_wht = read_df_wht(path)
        df = pd.merge(df, df_wht, on="Index", how="left")
    except:
        pass
    return df

def main():
    # input.csvの番号と計算結果が格納されているディレクトリ名が対応している必要
    # ファイル名一覧を取得
    list_num = os.listdir("out//")
    for i, num in enumerate(list_num):
        path = "out//"+num+"//"
        df = merge_tbl(path)
        df = calc_volume(df)
        df_input = read_input(df, i)
        df = pd.concat([df, df_input], axis=1)
        # 結果を下に追加する
        if i == 0:
            pass
        else:
            df = pd.concat([df_out, df], axis=0)
        df_out = df
    df_out.to_csv("results.csv")

if __name__ == "__main__":
    main()