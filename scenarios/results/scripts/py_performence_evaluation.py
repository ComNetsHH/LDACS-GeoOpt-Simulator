"""Performance evaluation helpers for LDACS GeoOpt simulation results."""

import numpy as np
import pandas as pd

from result_analysis import confidence_interval_init
from result_analysis_init import (
    read_result_multi_modules_aggregated,
    read_result_multi_variable_multiaircraft_multi_runs,
    read_result_vector_averages_multi_modules_aggregated,
    read_result_vector_averages_multi_modules_multi_apps_aggregated,
    read_result_vector_percentiles_multi_modules_aggregated,
    read_result_vector_percentiles_multi_modules_multi_apps_aggregated_concatenated,
)

def pdr_read_and_process_data(csv_filename_packet_received,
                             csv_filename_packet_sent,
                             module_name_packet_received,
                             module_names_packet_sent,
                             variable_values,
                             no_simulation_runs,
                             variable_name):

    kpi_name_packet_received='packetReceived:count'
    kpi_name_packet_sent='packetSent:count'

    packet_sent_sum = read_result_multi_modules_aggregated(csv_filename_packet_sent,
                                                           variable_values,
                                                           variable_name,
                                                           no_simulation_runs,
                                                           module_names_packet_sent,
                                                           kpi_name_packet_sent)
    packet_received_sum = read_result_multi_variable_multiaircraft_multi_runs(csv_filename_packet_received,
                                                                              variable_values,
                                                                              variable_name,
                                                                              no_simulation_runs,
                                                                              module_name_packet_received,
                                                                              kpi_name_packet_received)
    if packet_received_sum.shape[2] == 1:
        packet_received_sum = np.squeeze(packet_received_sum, axis=2)
    else:
        packet_received_sum = np.sum(packet_received_sum, axis=2)
    pdr = np.divide(packet_received_sum, packet_sent_sum)
    mean, _, margin_of_error = confidence_interval_init(pdr, confidence=0.95)
    return mean, margin_of_error




def hc_read_and_process_data(csv_filename_hop_count,
                             module_names_hop_count,
                             variable_values,
                             no_simulation_runs,
                             variable_name):
    kpi_name_hop_count = 'hopCount:vector'

    average_hop_count = read_result_vector_averages_multi_modules_aggregated(csv_filename_hop_count,
                                                                             variable_values,
                                                                             variable_name,
                                                                             no_simulation_runs,
                                                                             module_names_hop_count,
                                                                             kpi_name_hop_count)

    mean, _, margin_of_error = confidence_interval_init(average_hop_count, confidence=0.95)
    return mean, margin_of_error


