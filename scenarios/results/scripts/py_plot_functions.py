"""Plotting helpers used by the LDACS GeoOpt simulator analysis scripts."""

import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch
from matplotlib.ticker import MultipleLocator

plt.rcParams.update({
    'font.family': 'lmodern',
    'font.size': 30,
    'text.usetex': True,
    'pgf.rcfonts': False,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'text.latex.preamble': r'\usepackage{lmodern}'
})

def plot_error_bar(mean_rates, margin_errors, strategies, x_data, xlabel, ylabel, path=None, filename=None, title=None, set_ylim=1.02, width=0.1, figsize=(16, 8), style_combinations={}, enable_legend=True, capsize=5, legend_info=[], bar_spacing=0.0):
    fig, ax = plt.subplots(figsize=figsize)

    x_pos = np.arange(len(x_data))
    width = width  # Adjust width for separation
    num_strategies = len(strategies)

    colors = [plt.get_cmap('tab10', num_strategies)(i) for i in range(num_strategies)]

    for id, x_value in enumerate(x_data):
        group_start = x_pos[id] - (num_strategies - 1) * (width + bar_spacing) / 2
        for idx, strategy in enumerate(strategies):
            mean = mean_rates[strategy][id]
            moe = margin_errors[strategy][id]
            bar_position = group_start + idx * (width + bar_spacing)
            if style_combinations:
                color, hatch = style_combinations[strategy]
                ax.bar(bar_position, mean,
                    color=color, edgecolor='black', hatch=hatch,
                    yerr=moe, capsize=capsize, width=width,
                    label=strategy if id == 0 else None)  # Label only for the first set
            else:
                ax.bar(bar_position, mean,
                    color=colors[idx], edgecolor='black',
                    yerr=moe, capsize=capsize, width=width,
                    label=strategy if id == 0 else None)  # Label only for the first degree

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(x_data)
    ax.tick_params(axis='both')
    if set_ylim:
        ax.set_ylim(0, set_ylim)
    else:
        bottom, top = ax.get_ylim()  # return the current ylim
        if bottom < 0:
            ax.set_ylim((0, top))   # set the ylim to 0, top

    if title:
        ax.set_title(title)

    ax.xaxis.grid(True, which='major', linestyle=(0, (5, 10)), linewidth=0.2)
    ax.yaxis.grid(True, which='major', linestyle=(0, (5, 10)), linewidth=0.2)
    ax.yaxis.grid(True, which='minor', linestyle=(0, (5, 20)), linewidth=0.1)
    if set_ylim and set_ylim > 100:
        ax.yaxis.set_major_locator(MultipleLocator(20))
    elif set_ylim and set_ylim > 1:
        ax.yaxis.set_major_locator(MultipleLocator(0.2))

    if enable_legend and legend_info:
        legend_patches = [Patch(facecolor=color, label=label, hatch=hatch, edgecolor='black') for label, color, hatch in legend_info]
        ax.legend(handles=legend_patches, loc='best')
    elif enable_legend:
        ax.legend(loc='best')

    if path is not None and filename is not None:
        os.makedirs(path, exist_ok=True)
        plt.savefig(os.path.join(path, filename + '.pdf'), format='pdf', bbox_inches="tight")

def plot_error_lines(mean_rates, margin_errors, strategies, x_data,
                     xlabel, ylabel,
                     path=None, filename=None, title=None,
                     xlim=None, ylim=None,
                     figsize=(12, 9),
                     style_combinations=None,
                     enable_legend=True,
                     lw=3,
                     markersize=8,
                     capsize=4,
                     yMajorTick=None,
                     yMinorTick=None,
                     show_scenario_labels=True,
                     scenario_a_pos=(0.8, 0.65),
                     scenario_b_pos=(0.4, 0.65),
                     scenario_a_label="A",
                     scenario_b_label="B",
                     legend_columns=1,
                     bbox_to_anchor=None):
    """
    Plot line charts with error bars for multiple strategies.

    Arguments:
    - mean_rates: dict[strategy] -> list of mean values
    - margin_errors: dict[strategy] -> list of error-bar values
    - strategies: list of strategy keys (order determines plot order)
    - x_data: list of x-axis values
    - xlabel, ylabel: axis labels
    - path, filename: if provided, save figure to path/filename.pdf
    - title: optional plot title
    - xlim, ylim: optional tuples for x/y limits (e.g., (0,0.2) or (0,100))
    - figsize: tuple for figure size
    - style_combinations: dict[strategy] -> (color, marker, linestyle)
    - enable_legend: whether to show legend
    - lw, markersize, capsize: styling for lines/markers/error caps
    - yMajorTick, yMinorTick: set major/minor y tick spacing (float)
    - show_scenario_labels: if True, draw vertical lines & labels for scenarios A/B
    - scenario_a_pos: (x, y) for scenario A annotation; vertical line at x
    - scenario_b_pos: (x, y) for scenario B annotation; vertical line at x
    - scenario_a_label, scenario_b_label: text for the annotations
    - legend_columns: Set the number of columns in the legend
    """
    fig, ax = plt.subplots(figsize=figsize)
    num_strat = len(strategies)
    default_colors = plt.get_cmap('tab10', num_strat)
    default_markers = ['o', 's', '^', 'd', 'v', '>', '<', 'p', 'h', '*']
    default_linestyles = ['-', '--', '-.', ':'] * ((num_strat // 4) + 1)

    for idx, strategy in enumerate(strategies):
        means = mean_rates[strategy]
        errs = margin_errors.get(strategy, [None]*len(means))
        if style_combinations and strategy in style_combinations:
            color, marker, linestyle = style_combinations[strategy]
        else:
            color = default_colors(idx)
            marker = default_markers[idx % len(default_markers)]
            linestyle = default_linestyles[idx]
        ax.errorbar(x_data, means, yerr=errs,
                    label=strategy,
                    color=color,
                    marker=marker,
                    linestyle=linestyle,
                    lw=lw,
                    markersize=markersize,
                    capsize=capsize)

    if show_scenario_labels:
        bx, by = scenario_b_pos
        ax.axvline(bx, color='k', linestyle="--", linewidth=2, alpha=0.8)
        ax.annotate(
            f"{scenario_b_label}",
            xy=(bx, by),
            xytext=(bx, by),
            textcoords="data",
            ha="center",
            va="center",
            bbox=dict(facecolor="white", edgecolor='k', boxstyle="round,pad=0.3", linewidth=lw)
        )

        axx, axy = scenario_a_pos
        ax.axvline(axx, color='k', linestyle="--", linewidth=2, alpha=0.8)
        ax.annotate(
            f"{scenario_a_label}",
            xy=(axx, axy),
            xytext=(axx, axy),
            textcoords="data",
            ha="center",
            va="center",
            bbox=dict(facecolor="white", edgecolor='k', boxstyle="round,pad=0.3", linewidth=lw)
        )

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    ax.set_xticks(x_data)

    ax.xaxis.grid(True, which='major', linestyle=(0, (5, 10)), linewidth=0.2)
    ax.yaxis.grid(True, which='major', linestyle=(0, (5, 10)), linewidth=0.2)
    ax.yaxis.grid(True, which='minor', linestyle=(0, (5, 20)), linewidth=0.1)

    if yMajorTick:
        ax.yaxis.set_major_locator(MultipleLocator(yMajorTick))
    if yMinorTick:
        ax.yaxis.set_minor_locator(MultipleLocator(yMinorTick))

    if xlim:
        ax.set_xlim(xlim)
    if ylim:
        ax.set_ylim(ylim)
    if title:
        ax.set_title(title)
    if enable_legend:
        if bbox_to_anchor:
            ax.legend(ncol=legend_columns, bbox_to_anchor=bbox_to_anchor)
        else:
            ax.legend(ncol=legend_columns)
    plt.tight_layout()

    if path and filename:
        os.makedirs(path, exist_ok=True)
        savepath = os.path.join(path, filename + '.pdf')
        fig.savefig(savepath, format='pdf', bbox_inches='tight')
        print(f"Saved figure to {savepath}")

    plt.show()
