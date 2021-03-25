import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import interpolate
from matplotlib.colors import Normalize


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
    return tempc, pressure, comp, vol, xy

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

def make_plotdata(xy, vol):
    # メッシュを作成
    grid_x = np.linspace(900, 1300, 400)
    grid_y = np.linspace(0.1, 6, 1000)
    plot_x, plot_y = np.meshgrid(grid_x, grid_y)
    # 線形補完する
    #plot_comp = interpolate.griddata(xy, comp, (plot_x, plot_y), method='linear')
    plot_vol = interpolate.griddata(xy, vol, (plot_x, plot_y), method='cubic')
    return plot_x, plot_y, plot_vol
    
def main():
    wtsi = 60
    wtwater = 2
    oxbuffer = "NNO"
    phase, label_cbar, comp_phase, vol_phase = select_phase()
    title = phase + "(" + str(wtsi) + " wt% SiO$_2$, " + str(wtwater) + " wt% H$_2$O, " + oxbuffer + " buffer" + ")"
    df = pd.read_csv("results.csv")
    tempc, pressure, comp, vol, xy \
    = filter_input(df, wtsi, wtwater, oxbuffer, comp_phase, vol_phase)
    plot_x, plot_y, plot_vol = make_plotdata(xy, vol)
    
    fig, ax = plt.subplots()
    im = ax.scatter(
        tempc, pressure, c=comp, marker="s",
        cmap='turbo', norm=Normalize(vmin=0, vmax=100)
        )
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label(label_cbar, fontsize=16)
    vol_cntr = ax.contour(plot_x, plot_y, plot_vol, colors='k', levels=list(np.arange(0, 100, 1)), linestyles='dashed', linewidths=[0.5, 0.1, 0.1, 0.1, 0.1])
    ax.clabel(vol_cntr, levels=list(np.arange(0,100,5)), fmt='%d', fontsize=10)
    # タイトル・軸ラベル
    ax.set_title(title, fontsize=12)
    ax.set_xlim(890, 1220)
    ax.set_ylim(-0.2, 6.2)
    ax.set_xlabel(r'Temperature ($^\circ$C)', fontsize=16)
    ax.set_ylabel('Pressure (kbar)', fontsize=16)
    # 出力
    plt.savefig('img_cntr//' + title + '.jpg', dpi=300, bbox_inches='tight')
    


if __name__ == "__main__":
    main()