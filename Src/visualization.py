import os
import pandas as pd
from bokeh.plotting import figure, show
from bokeh.layouts import gridplot
from bokeh.io import output_file


class Visualizer:
    def plot_all(self, train_df, ideal_df, test_df, mapping, results, output_path):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        output_file(
            output_path,
            title="Ideal Function Mapping - DLMDSPWP01",
            mode="inline"
        )

        plots = []
        colors = ['black', 'blue', 'red', 'green']

        for idx, train_col in enumerate(['y1', 'y2', 'y3', 'y4']):
            ideal_col = mapping[train_col][0]

            p = figure(
                title=f"{train_col} → {ideal_col}",
                width=600,
                height=450,
                tools="pan,wheel_zoom,box_zoom,reset,save"
            )

            p.circle(
                train_df['x'],
                train_df[train_col],
                size=8,
                color=colors[idx],
                alpha=0.8,
                legend_label="Training Data",
            )

            p.line(
                ideal_df['x'],
                ideal_df[ideal_col],
                line_width=2,
                color="red",
                legend_label="Chosen Ideal Function",
            )

            mapped = [r for r in results if r['ideal_function_no'] == ideal_col]
            if mapped:
                df_m = pd.DataFrame(mapped)
                p.triangle(
                    df_m['x'],
                    df_m['y'],
                    size=12,
                    color="green",
                    legend_label="Mapped Test Points",
                )

            p.legend.location = "top_left"
            p.legend.click_policy = "hide"

            plots.append(p)

        grid = gridplot([[plots[0], plots[1]], [plots[2], plots[3]]])
        show(grid)
