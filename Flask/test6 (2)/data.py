# -- coding: utf-8 --
def plotdata():
    import seaborn as sns
    from bokeh.embed import components
    from bokeh.plotting import figure
    data = sns.load_dataset('tips')
    data2 = data.groupby(['smoker']).mean().tip

    # 그래프 그리는 부분
    p = figure(x_range=['YES', 'NO'], plot_width=800, plot_height=600)
    p.vbar(x=['YES', 'NO'], width=0.5, top=data2, legend='tip')

    return components(p)