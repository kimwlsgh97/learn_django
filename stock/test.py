from matplotlib import rcParams
import matplotlib.pyplot as plt
import numpy as np


if __name__=='__main__':
    # X = [1,3,5,7,9]
    # Y = [100,200,300,400,500]
    x = np.linspace(-np.pi, np.pi, 128)
    y = np.cos(x)

    # plt.plot(X,Y)
    plt.plot(y)
    plt.show()
    # plt.savefig('/home/jinho/sample/learn/learn_django/stock/plot.png', format='png')


if __name__=='__':
    labels = ['STAD', 'LUAD', 'LIHC', 'READ', 'BRCA', 'CESC', 'Others']
    titles = ['Cancer Deaths by type, 2010']
    data = [10032, 15623, 11205, 7701, 1868, 1272, 24345]

    rcParams.update({'font.size': 10})
    fig, axes = plt.subplots(1,2,figsize=(10,5))
    plt.subplots_adjust(wspace=0.5)

    explode = (0, 0.1, 0, 0, 0, 0, 0)

    for i in range(2):
        ax = axes[i]
        wedges, texts, autotexts = ax.pie(data[i], explode=explode, labels=labels, 
        autopct='%1.1f%%', pctdistance=0.85, shadow=False, startangle=90)

        for w in wedges:
            w.set_linewidth(0)
            w.set_edgecolor('w')

        for t in texts:
            t.set_color('k')
            t.set_fontsize(12)

        for a in autotexts:
            a.set_color('w')
            a.set_fontsize(8)

        # 도넛 트릭
        centre_circle = plt.Circle((0,0), 0.70, color='black', fc='white', linewidth=0)
        ax.add_artist(centre_circle)

        ax.set_title(titles[i])
        ax.axis('equal')

    plt.savefig('/home/jinho/sample/learn/learn_django/stock/ex_pieplot.png', format='png', dpi=300)
    plt.show()