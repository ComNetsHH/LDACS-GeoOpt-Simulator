"""Generate hop-count plots for the Scenario FR equipage-fraction study."""

import argparse
import csv
from pathlib import Path

from py_performence_evaluation import hc_read_and_process_data
from py_plot_functions import plot_error_lines


VARIABLE_SETS = [
    {
        "variable_values": ["50", "100", "150", "200", "250", "300", "350", "400", "450", "500"],
        "x_data": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
        "suffix": "0.1-1",
        "xlim": (0.095, 1.005),
    }
]
NO_SIMULATION_RUNS = 100
MAX_NO_OF_AIRCRAFT = 500
VARIABLE_NAME = "numAircrafts"
RESULTS_DIR = Path("./simresults/scenarioFR/EquipageFraction")
PLOTS_ROOT = Path("./scenarioFR_EquipageFraction")
STRATEGIES = ["Greedy-1", "GPSR", "GeoOpt", "Dijkstra"]
STYLE_COMBINATIONS = {
    "Greedy-1": ("#D62728", "o", "-"),
    "GPSR": ("#FF7F0E", "s", "-"),
    "GeoOpt": ("#2CA02C", "^", "-"),
    "Dijkstra": ("#1F77B4", "*", "-"),
}


def write_strategy_means_csv(csv_path: Path, strategies: list[str], variable_values: list[str], mean_rates: dict) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Strategy", *variable_values])
        for strategy in strategies:
            writer.writerow([strategy, *list(mean_rates[strategy])])


def analyze_hc_dijkstra_greedy_1_optimized_gpsr(communication_range_km: int, beacon_interval_s: int) -> None:
    csv_filenames_hop_count = {
        "Greedy-1": RESULTS_DIR / "greedy-forwarding-1hop" / "hop_count_vector.csv",
        "GPSR": RESULTS_DIR / "gpsr-forwarding" / "hop_count_vector.csv",
        "Dijkstra": RESULTS_DIR / "dijkstra" / "hop_count_vector.csv",
        "GeoOpt": RESULTS_DIR / "optimized-greedy" / "hop_count_vector.csv",
    }
    module_names_hop_count = [
        f"scenarioFR_forwarding.aircraft[{aircraft}].routing" for aircraft in range(MAX_NO_OF_AIRCRAFT)
    ]

    for variable_set in VARIABLE_SETS:
        mean_rates = {}
        margin_errors = {}
        for strategy in STRATEGIES:
            print(f"Currently running for strategy: {strategy}")
            mean_rates[strategy], margin_errors[strategy] = hc_read_and_process_data(
                str(csv_filenames_hop_count[strategy].resolve()),
                module_names_hop_count,
                variable_set["variable_values"],
                NO_SIMULATION_RUNS,
                VARIABLE_NAME,
            )
            print(f"HC: {mean_rates[strategy]}")

        plots_dir_path = (
            PLOTS_ROOT
            / f"range_{communication_range_km}km_beaconInterval_{beacon_interval_s}s"
            / "hop_count"
        )
        write_strategy_means_csv(
            plots_dir_path / f"mean_hc_{variable_set['suffix']}.csv",
            STRATEGIES,
            variable_set["variable_values"],
            mean_rates,
        )

        plot_error_lines(
            mean_rates,
            margin_errors,
            STRATEGIES,
            variable_set["x_data"],
            xlabel=r"Equipage Fraction $(\rho)$",
            ylabel="Hop Count (hops)",
            xlim=variable_set["xlim"],
            ylim=(-0.005, 10),
            style_combinations=STYLE_COMBINATIONS,
            enable_legend=True,
            capsize=4,
            figsize=(12, 9),
            yMajorTick=2,
            yMinorTick=1,
            scenario_a_pos=(0.8, 1),
            scenario_b_pos=(0.4, 1),
            path=str(plots_dir_path),
            filename=f"hc_{variable_set['suffix']}",
        )


def main() -> None:
    parser = argparse.ArgumentParser(description="Run hop-count analysis for Scenario FR.")
    parser.add_argument("--r", type=int, required=True, help="Communication range in km.")
    parser.add_argument("--BI", type=int, required=True, help="Beacon interval in seconds.")
    args = parser.parse_args()
    analyze_hc_dijkstra_greedy_1_optimized_gpsr(args.r, args.BI)


if __name__ == "__main__":
    main()
