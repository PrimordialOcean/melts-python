import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
from matplotlib.colors import Normalize

def make_plotdata(xy, comp, vol):
    # メッシュを作成
    grid_x = np.linspace(900, 1300, 400)
    grid_y = np.linspace(0.5, 6, 1000)
    plot_x, plot_y = np.meshgrid(grid_x, grid_y)
    # 線形補完する
    plot_comp = interpolate.griddata(xy, comp, (plot_x, plot_y), method='linear')
    plot_vol = interpolate.griddata(xy, vol, (plot_x, plot_y), method='linear')
    return plot_x, plot_y, plot_comp, plot_vol

def plot_3d(plot_x, plot_y, plot_comp, plot_vol, label_cbar, title):
    # プロット
    range_cbar = [ 0, 100 ]
    plt.rcParams["font.size"] = 14
    plt.rcParams["pcolor.shading"] = "gouraud"
    fig, ax = plt.subplots()
    im = ax.pcolormesh(plot_x, plot_y, plot_comp, cmap='turbo', 
    norm=Normalize(vmin=0, vmax=100)
    )
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label(label_cbar)
    # 組成コンター
    comp_cntr = ax.contour( plot_x, plot_y, plot_comp, colors='black', levels=list(np.arange(0, 100, 1)), linewidths=[0.5, 0.1, 0.1, 0.1, 0.1] )
    ax.clabel(comp_cntr, levels=list(np.arange(0,100,5)), fmt='%d', fontsize=10)
    # モード組成コンター
    vol_cntr = ax.contour(plot_x, plot_y, plot_vol, colors='white', levels=list(np.arange(0, 100, 1)), linestyles='dashed', linewidths=[0.5, 0.1, 0.1, 0.1, 0.1])
    ax.clabel(vol_cntr, levels=list(np.arange(0,100,5)), fmt='%d', fontsize=10)
    # タイトル・軸ラベル
    ax.set_title(title, fontsize=12)
    ax.set_xlabel(r'Temperature ($^\circ$C)', fontsize=16)
    ax.set_ylabel('Pressure (kbar)', fontsize=16)
    # 出力
    plt.savefig('plot_cntr//' + title + '.jpg', dpi=300, bbox_inches='tight')
    plt.close()

def select_phase():
    list_phase = [ "Plg", "Cpx", "Opx", "Olv", "Hbl"]
    list_label_cbar = [ "An (mol%)", "Mg# (mol%)", "Mg# (mol%)", "Fo (mol%)",
    "Si (apfu)"]
    list_comp_phase = [ "AnPlg", "Mg#Cpx", "Mg#Opx", "FoOlv", "SiHbl (apfu)"]
    list_vol_phase = [ "volPlg (vol%)", "volCpx (vol%)", "volOpx (vol%)",
    "volOlv (vol%)", "volHbl (vol%)" ]
    # 出力するphaseを選択
    print("Select phase name [0] plg [1] cpx [2] opx [3] olv [4] hbl")
    while True:
        num = int(input())
        if 0 <= num <=4:
            phase, label_cbar, comp_phase, vol_phase \
            = list_phase[num], list_label_cbar[num], list_comp_phase[num], list_vol_phase[num]
            break
        else:
            print("Type correct number!")
    return phase, label_cbar, comp_phase, vol_phase

def select_input():
    # 出発物質の含水量，組成を入力
    print("Input wt% SiO2 composition")
    wtsi = float(input())
    #print("Input wt% water content")
    #wtwater = float(input())
    #print("Input fO2 buffer")
    oxbuffer = "NNO"
    return wtsi

# 入力した条件をもとに計算結果からデータ抽出
def filter_input(df, wtsi, wtwater, oxbuffer, comp_phase, vol_phase):
    df = df[ ( df["SiO2"] == wtsi ) & ( df["H2O"] == wtwater ) & ( df["fO2"] == oxbuffer ) ]
    # 晶出していない部分を削除
    df = df[ df[comp_phase] > 0 ]
    # ソリダス付近の計算結果を削除
    #df.loc[ ( df["volTotalPh (vol%)"] > 80 ), vol_phase ] = np.nan
    #df.loc[ ( df["volTotalPh (vol%)"] > 80 ), comp_phase ] = np.nan
    tempc, pressure = df["T (C)"].values.tolist(), df["P (kbars)"].values.tolist()
    comp, vol = df[comp_phase].values.tolist(), df[vol_phase].values.tolist()
    xy = np.array([tempc, pressure]).T
    return xy, comp, vol

def main():
    phase, label_cbar, comp_phase, vol_phase = select_phase()
    #wtsi, wtwater, oxbuffer = select_input()
    
    oxbuffer = "NNO"
    for wtsi in np.arange(49, 65, 1):
        for wtwater in np.arange(0.5, 5.5, 0.5):
            title = phase + "(" + str(wtsi) + " wt% SiO$_2$, " + str(wtwater) + " wt% H$_2$O, " + oxbuffer + " buffer" + ")"

            df = pd.read_csv("results.csv")
            xy, comp, vol = filter_input(df, wtsi, wtwater, oxbuffer, comp_phase, vol_phase)
            plot_x, plot_y, plot_comp, plot_vol = make_plotdata(xy, comp, vol)
            plot_3d(plot_x, plot_y, plot_comp, plot_vol, label_cbar, title)

if __name__ == "__main__":
    main()