from .functions import calc_loads
import os
import json
from functools import partial
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np

THIS_DIR = os.path.dirname(__file__)
def compare(path_list):
    merged_loads = calc_loads(path_list[0], {})
    name_turbines = {os.path.splitext(os.path.split(path_list[0])[-1])[0]: list(merged_loads['ul'].index)}
    for p in path_list[1:]:
        filename = os.path.splitext(os.path.split(p)[-1])[0]
        loads = calc_loads(p, {})
        name_turbines[filename] = list(loads['ul'].index)
        merged_loads['ul'] = merged_loads['ul'].append(loads['ul'])
        merged_loads['fl'] = merged_loads['fl'].append(loads['fl'])

    global THIS_DIR
    color_path = os.path.abspath(os.path.join(THIS_DIR, '../../res/files/color/color.json'))

    with open(color_path, 'r') as f:
        colors = json.load(f)
    color_list = list(colors.values())
    color_list_sub = [color_list[i] for i in range(len(path_list))]

    bar_plot = partial(draw, name_turbines=name_turbines, color_list=color_list_sub)

    return {'bar_plot': bar_plot, 'loads': merged_loads}


def draw(fig, load, sub, name_turbines, color_list):

    fig.add_subplot(sub)

    load_sorted = load.sort_values(ascending=False)

    x_label, values, color_show, legend_handles = bar_config(load_sorted, name_turbines, color_list)
    fake_values = values / np.max(values)

    if len(x_label) < 5:
        plt.bar(x_label, fake_values, color=color_show, width=0.3)
    else:
        plt.bar(x_label, fake_values, color=color_show)

    y_label = {211: 'Ultimate_load', 212: 'Fatigue_load'}
    plt.ylabel(y_label[sub])

    y_ticks_min = max(round(min(fake_values), 2) - 0.2, 0)
    y_ticks_max = 1.5
    plt.ylim(y_ticks_min, y_ticks_max)
    plt.yticks(np.arange(y_ticks_min, y_ticks_max, 0.2), fontsize=8)

    plt.legend(handles=legend_handles, ncol=6, fontsize='xx-small') #len(ref_labels) + 1
    # mode="expand"（平铺， 默认向右靠拢）  loc='upper right' (默认),

    if len(x_label) > 10:
        plt.xticks(rotation=45, horizontalalignment='right', size=6)
    if len(x_label) < 40:
        for a, b in zip(x_label, fake_values):
            plt.text(a, b + 0.005, '%.3f' % b, ha='center', va='bottom',
                     fontsize=6)
    elif len(x_label) < 60:
        for a, b in zip(x_label, fake_values):
            plt.text(a, b + 0.005, '%.3f' % b, ha='center', va='bottom',
                     fontsize=6, rotation=30, horizontalalignment='center')
    else:
        for a, b in zip(x_label, fake_values):
            plt.text(a, b + 0.01, '%.3f' % b, ha='center', va='bottom',
                     fontsize=6, rotation=90, horizontalalignment='center')

def bar_config(load_sorted, name_turbines, color_list):
    values = load_sorted.values

    sorted_labels = list(load_sorted.index)
    show_labels = [lbl for lbl in sorted_labels]

    color_show = []

    for lbl in sorted_labels:
        for i, labels in enumerate(name_turbines.values()):
            if lbl in labels:
                color_show.append(color_list[i])

    handles = list()
    for i, filename in enumerate(name_turbines.keys()):
        handles.append(mpatches.Patch(color=color_list[i], label=filename))

    return show_labels, values, color_show, handles


def json_parse(ref_loads_path):
    """
    count reference labels
    :param ref_loads_path:
    :return:
    """
    ref_labels = {}
    if len(ref_loads_path) > 0:
        for path in ref_loads_path:
            with open(path, 'r') as f:
                loads = json.load(f)
                filename = os.path.splitext(os.path.split(path)[-1])[0][:-6]
                ref_labels[filename] = list(loads['ul'].keys())

    return ref_labels


if __name__ == "__main__":
    import sys
    sys.path.append(r'E:\WorkSpace\6_Programming\wind-order-gui')
    path = [r'E:\WorkSpace\6_Programming\wind-order-gui\files\wind\huaneng_140-2.5-140m_341.5t.xlsx',
            r'‪E:\WorkSpace\6_Programming\wind-order-gui\files\wind\CZ_GW140-2500-140_351t.xlsx']

    compare(path)
