"""Result loading and aggregation helpers for LDACS GeoOpt post-processing."""

import networkx as nx
import numpy as np
import pandas as pd

from result_analysis import confidence_interval_init

def read_result_multi_variable_multi_runs(csv_filename, variable_values, variable_name,
                                          no_simulation_runs, module_name, kpi_name):
    r"""
    Plot an error bar with the specified margin of error.

    INPUT:

    	- ``x_data`` -- A ``list of doubles`` or ``numpy.ndarray`` (preferable ``strings`` for equi-distance points).
    	- ``y_data`` -- A ``list of doubles``  or ``numpy.ndarray``.
    	- ``margin_of_error_greedy`` -- A ``list of doubles``  or ``numpy.ndarray``.
    	- ``xlabel``
    	- ``ylabel``
    	- ``rotation_xticks`` -- (``optional``)
    	- ``yaxis_minor_ticks_separation`` -- (``optional``)
    	- ``title`` -- (``optional``)
    	- ``save_to_fig`` -- (``optional``)

    OUTPUT:

        - ``The plot`` -- (optionally saved to the specified path).

    EXAMPLES::

    	from result_analysis import *
    	from plot_results import plot_error_bar
    	data = np.random.uniform(low=0.5, high=15.0, size=(6,20))
    	sample_mean, Confidence_Interval, margin_of_error_greedy = confidence_interval_init(data)
    	x_data = ['1','2','3','4','5','6']
    	y_data = sample_mean
    	xlabel = 'x-label'
    	ylabel = 'y-label'
    	plot_error_bar(x_data, y_data, margin_of_error_greedy, xlabel, ylabel)
    """
    result = pd.read_csv(csv_filename)
    iter_vars = result.loc[result.type=='itervar', ['run', 'attrname', 'attrvalue']]
    iter_vars_pivot = iter_vars.pivot(index='run', columns='attrname', values='attrvalue')
    result_merged = result.merge(iter_vars_pivot, left_on='run', right_index=True, how='outer')
    no_elements_variable_values = len(variable_values)
    result_array = np.empty(shape=[no_elements_variable_values, no_simulation_runs])
    for index, value in enumerate(variable_values):
        output_row_in_table_format = result_merged[(getattr(result_merged, variable_name) == value)
                                                & (result_merged.type == 'scalar')
                                                & (result_merged.module == module_name)
                                                & (result_merged.name == kpi_name)]
        result_array[index] = output_row_in_table_format['value'].to_numpy()
    return result_array

def read_result_multi_variable_multi_missed_runs(csv_filename, variable_values, variable_name,
                                          no_simulation_runs, module_name, kpi_name):
    result = pd.read_csv(csv_filename)
    iter_vars = result.loc[result.type=='itervar', ['run', 'attrname', 'attrvalue']]
    iter_vars_pivot = iter_vars.pivot(index='run', columns='attrname', values='attrvalue')
    result_merged = result.merge(iter_vars_pivot, left_on='run', right_index=True, how='outer')
    no_elements_variable_values = len(variable_values)
    result_array = np.empty(shape=[no_elements_variable_values, no_simulation_runs])
    output_row_in_table_format = result_merged[(getattr(result_merged, variable_name).isin(variable_values))
                                            & (result_merged.type == 'scalar')
                                            & (result_merged.module == module_name)
                                            & (result_merged.name == kpi_name)]
    uniqueId = output_row_in_table_format["run"].unique()
    results = np.array([])
    for id in uniqueId:
        result_repetition = output_row_in_table_format.loc[output_row_in_table_format["run"] == id]
        result_repetition_variables = np.unique(result_repetition[variable_name].to_numpy())
        result_repetition = result_repetition['value'].to_numpy()
        result_dict = np.hstack([result_repetition, result_repetition_variables])
        results = np.append(results, result_dict)

    results = results.reshape((results.size // 2), 2)
    results_df = pd.DataFrame(results,
                                    columns=['count',
                                             variable_name])
    results_mean = np.array([])
    results_Confidence_Interval = np.array([])
    results_margin_of_error_greedy = np.array([])
    for range in variable_values:
        results_filtered = (results_df.loc[results_df[variable_name] == range])['count'].to_numpy()

        sample_mean, Confidence_Interval, margin_of_error_greedy = confidence_interval_init(results_filtered)
        results_mean = np.append(results_mean, sample_mean)
        results_margin_of_error_greedy = np.append(results_margin_of_error_greedy, margin_of_error_greedy)
        results_Confidence_Interval = np.append(results_Confidence_Interval, Confidence_Interval)
    return results_mean, results_Confidence_Interval, results_margin_of_error_greedy

def parse_if_number(s):
    try: return float(s)
    except: return True if s=="true" else False if s=="false" else s if s else None

def parse_ndarray(s):
    return np.fromstring(s, sep=' ') if s else None

def complete_missed_elements_of_vector(ordered_vector, total_expected_number_of_elements, filling_element=np.inf):
    no_of_elements_of_ordered_vector = ordered_vector.shape[0]
    missed_elements_count = total_expected_number_of_elements - no_of_elements_of_ordered_vector
    for i in range(missed_elements_count):
        ordered_vector = np.append(ordered_vector, filling_element)
    return ordered_vector

def read_csv_into_vectors(csv_filename, kpi_name,  variable_values=[], variable_name='',module_name=''):
    r"""
    Plot an error bar with the specified margin of error.

    INPUT:

    	- ``x_data`` -- A ``list of doubles`` or ``numpy.ndarray`` (preferable ``strings`` for equi-distance points).
    	- ``y_data`` -- A ``list of doubles``  or ``numpy.ndarray``.
    	- ``margin_of_error_greedy`` -- A ``list of doubles``  or ``numpy.ndarray``.
    	- ``xlabel``
    	- ``ylabel``
    	- ``rotation_xticks`` -- (``optional``)
    	- ``yaxis_minor_ticks_separation`` -- (``optional``)
    	- ``title`` -- (``optional``)
    	- ``save_to_fig`` -- (``optional``)

    OUTPUT:

        - ``The plot`` -- (optionally saved to the specified path).

    EXAMPLES::

    	from result_analysis import *
    	from plot_results import plot_error_bar
    	data = np.random.uniform(low=0.5, high=15.0, size=(6,20))
    	sample_mean, Confidence_Interval, margin_of_error_greedy = confidence_interval_init(data)
    	x_data = ['1','2','3','4','5','6']
    	y_data = sample_mean
    	xlabel = 'x-label'
    	ylabel = 'y-label'
    	plot_error_bar(x_data, y_data, margin_of_error_greedy, xlabel, ylabel)
    """
    result = pd.read_csv(csv_filename, converters={
        'attrvalue': parse_if_number,
        'binedges': parse_ndarray,
        'binvalues': parse_ndarray,
        'vectime': parse_ndarray,
        'vecvalue': parse_ndarray})
    iter_vars = result.loc[result.type=='itervar', ['run', 'attrname', 'attrvalue']]

    iter_vars_pivot = iter_vars.pivot(index='run', columns='attrname', values='attrvalue')
    result_merged = result.merge(iter_vars_pivot, left_on='run', right_index=True, how='outer')

    no_elements_variable_values = len(variable_values)
    result_array = np.empty(shape=[no_elements_variable_values])
    vectors = result_merged[result.type == 'vector']
    selected_vectors = []
    if variable_name:
        for value in variable_values:
            vec = vectors[(vectors.name == kpi_name)
                          & (getattr(result_merged, variable_name) == value)
                          & (result_merged.module == module_name)]
            selected_vectors.append(vec)
    else:
        vec = vectors[(vectors.name == kpi_name)]
        selected_vectors.append(vec)
    return selected_vectors

def process_vectors(vector_of_vectors_df, is_complete_missing=False, total_expected_number_of_elements=0, filling_element=1000):
    list_of_vectors = []
    list_of_sorted_vectors = []
    array_of_means = []
    if is_complete_missing:
        for vec in vector_of_vectors_df:
            vector_of_means = np.array([])
            vector_of_values = np.array([])
            vector_of_values_completed = np.array([])
            for row in vec.itertuples():
                if type(row.vecvalue) is not type(None):
                    vector_of_means = np.append(vector_of_means, np.mean(row.vecvalue))
                    vector_of_values = np.append(vector_of_values, row.vecvalue)
                    vector_of_values_completed = np.append(vector_of_values_completed,
                                                           complete_missed_elements_of_vector(np.array(row.vecvalue),
                                                                                              total_expected_number_of_elements,
                                                                                              filling_element))
            array_of_means.append(vector_of_means)
            sorted_vector_of_values = np.flip(np.sort(vector_of_values_completed))
            list_of_vectors.append(vector_of_values)
            list_of_sorted_vectors.append(sorted_vector_of_values)
    else:
        for vec in vector_of_vectors_df:
            vector_of_means = np.array([])
            vector_of_values = np.array([])
            for row in vec.itertuples():
                if type(row.vecvalue) is not type(None):
                    vector_of_means = np.append(vector_of_means, np.mean(row.vecvalue))
                    vector_of_values = np.append(vector_of_values, row.vecvalue)
            array_of_means.append(vector_of_means)
            sorted_vector_of_values = np.flip(np.sort(vector_of_values))
            list_of_vectors.append(vector_of_values)
            list_of_sorted_vectors.append(sorted_vector_of_values)
    return list_of_vectors, list_of_sorted_vectors, array_of_means

def read_result_sum_multi_variable_multiaircraft_multi_runs(csv_filename, variable_values, variable_name, module_names,
                                                            kpi_name):
    result = pd.read_csv(csv_filename)
    iter_vars = result.loc[result.type == 'itervar', ['run', 'attrname', 'attrvalue']]
    iter_vars_pivot = iter_vars.pivot(index='run', columns='attrname', values='attrvalue')
    result_merged = result.merge(iter_vars_pivot, left_on='run', right_index=True, how='outer')
    results_filtered_df = result_merged[(getattr(result_merged, variable_name).isin(variable_values))
                                        & (result_merged.type == 'scalar')
                                        & (result_merged.module.isin(module_names))

                                        & (result_merged.name == kpi_name)]
    uniqueId = results_filtered_df["run"].unique()
    results_count = np.array([])
    for id in uniqueId:
        vec_repetition = results_filtered_df.loc[results_filtered_df["run"] == id]
        vec_repetition_variables = np.unique(vec_repetition[variable_name].to_numpy())
        vec_repetition = vec_repetition['value'].to_numpy()
        result_count = np.sum(vec_repetition)
        result_count_dict = np.hstack([result_count, vec_repetition_variables])
        results_count = np.append(results_count, result_count_dict)
    results_count = results_count.reshape((results_count.size // 2), 2)
    results_count_df = pd.DataFrame(results_count,
                                    columns=['count',
                                             variable_name])
    results_count_mean = np.array([])
    results_count_Confidence_Interval = np.array([])
    results_count_margin_of_error_greedy = np.array([])
    for range in variable_values:
        results_count_filtered = (results_count_df.loc[results_count_df[variable_name] == range])['count'].to_numpy()
        sample_mean, Confidence_Interval, margin_of_error_greedy = confidence_interval_init(results_count_filtered)
        results_count_mean = np.append(results_count_mean, sample_mean)
        results_count_Confidence_Interval = np.append(results_count_Confidence_Interval, Confidence_Interval)
        results_count_margin_of_error_greedy = np.append(results_count_margin_of_error_greedy, margin_of_error_greedy)
    return results_count_mean, results_count_Confidence_Interval, results_count_margin_of_error_greedy

def read_result_mean_multi_variable_multiaircraft_multi_runs(csv_filename, variable_values, variable_name, module_names,
                                                            kpi_name):
    result = pd.read_csv(csv_filename)
    iter_vars = result.loc[result.type == 'itervar', ['run', 'attrname', 'attrvalue']]
    iter_vars_pivot = iter_vars.pivot(index='run', columns='attrname', values='attrvalue')
    result_merged = result.merge(iter_vars_pivot, left_on='run', right_index=True, how='outer')

    results_filtered_df = result_merged[(getattr(result_merged, variable_name).isin(variable_values))
                                        & (result_merged.type == 'scalar')
                                        & (result_merged.module.isin(module_names))

                                        & (result_merged.name == kpi_name)]
    results_filtered_df = results_filtered_df.dropna(subset=['value'])
    uniqueId = results_filtered_df["run"].unique()
    results_count = np.array([])
    for id in uniqueId:
        vec_repetition = results_filtered_df.loc[results_filtered_df["run"] == id]
        vec_repetition_variables = np.unique(vec_repetition[variable_name].to_numpy())
        vec_repetition = vec_repetition['value'].to_numpy()
        result_count = np.mean(vec_repetition)
        result_count_dict = np.hstack([result_count, vec_repetition_variables])
        results_count = np.append(results_count, result_count_dict)
    results_count = results_count.reshape((results_count.size // 2), 2)
    results_count_df = pd.DataFrame(results_count,
                                    columns=['count',
                                             variable_name])
    results_count_mean = np.array([])
    results_count_Confidence_Interval = np.array([])
    results_count_margin_of_error_greedy = np.array([])
    for range in variable_values:
        results_count_filtered = (results_count_df.loc[results_count_df[variable_name] == range])['count'].to_numpy()
        sample_mean, Confidence_Interval, margin_of_error_greedy = confidence_interval_init(results_count_filtered)
        results_count_mean = np.append(results_count_mean, sample_mean)
        results_count_Confidence_Interval = np.append(results_count_Confidence_Interval, Confidence_Interval)
        results_count_margin_of_error_greedy = np.append(results_count_margin_of_error_greedy, margin_of_error_greedy)
    return results_count_mean, results_count_Confidence_Interval, results_count_margin_of_error_greedy

def read_result_vectors_multi_run_and_count(csv_filename, variable_values, variable_name, module_names, kpi_name,
                                            vecname):
    result = pd.read_csv(csv_filename, converters={
        'attrvalue': parse_if_number,
        'binedges': parse_ndarray,
        'binvalues': parse_ndarray,
        'vectime': parse_ndarray,
        'vecvalue': parse_ndarray})  # select the iteration variable/s
    iter_vars = result.loc[result.type == 'itervar', ['run', 'attrname', 'attrvalue']]
    iter_vars_pivot = iter_vars.pivot(index='run', columns='attrname', values='attrvalue')
    result_merged = result.merge(iter_vars_pivot, left_on='run', right_index=True, how='outer')

    no_elements_variable_values = len(variable_values)
    result_array = np.empty(shape=[no_elements_variable_values])
    vectors = result_merged[result.type == 'vector']
    if variable_name:
        vec = vectors[(vectors.name == kpi_name)
                      & (getattr(result_merged, variable_name).isin(variable_values))
                      & (result_merged.module.isin(module_names))]

    else:
        vec = vectors[(vectors.name == kpi_name)]

    vec = vec.loc[vec[variable_name].isin(variable_values)]
    uniqueId = vec["run"].unique()

    routing_failed_count = np.array([])
    np.warnings.filterwarnings('ignore', category=np.VisibleDeprecationWarning)
    for id in uniqueId:
        vec_repetition = vec.loc[vec["run"] == id]
        vec_repetition_variables = np.unique(vec_repetition[variable_name].to_numpy())
        vec_repetition = vec_repetition[vecname].to_numpy()
        result_count_dict = []
        result_count_dict = np.array([vec_repetition, vec_repetition_variables])
        routing_failed_count = np.append(routing_failed_count, result_count_dict)
    routing_failed_count = routing_failed_count.reshape((routing_failed_count.size // 2), 2)
    routing_failed_df = pd.DataFrame(routing_failed_count,
                                     columns=['result',
                                              variable_name])
    routing_failed_df['result'] = routing_failed_df['result'].apply(lambda x: np.hstack(x))

    routing_failed_df['count'] = routing_failed_df['result'].apply(lambda x: x.size)

    results_count_mean = np.array([])
    results_count_Confidence_Interval = np.array([])
    results_count_margin_of_error_greedy = np.array([])
    list_of_vectors = []
    for value in variable_values:
        results_count_filtered = (routing_failed_df.loc[routing_failed_df[variable_name] == value])['count'].to_numpy()
        sample_mean, Confidence_Interval, margin_of_error_greedy = confidence_interval_init(results_count_filtered)
        results_count_mean = np.append(results_count_mean, sample_mean)
        results_count_Confidence_Interval = np.append(results_count_Confidence_Interval, Confidence_Interval)
        results_count_margin_of_error_greedy = np.append(results_count_margin_of_error_greedy, margin_of_error_greedy)

        vec_with_value = routing_failed_df.loc[routing_failed_df[variable_name] == value]
        vec_with_value = vec_with_value['result'].to_numpy()
        vec_with_value = np.hstack(vec_with_value)
        list_of_vectors.append(vec_with_value)
    return results_count_mean, results_count_Confidence_Interval, results_count_margin_of_error_greedy, list_of_vectors

def filter_vector2_by_element_in_vector1(vector1, vector2, filtering_element):
    df = pd.DataFrame({'vector1': vector1, 'vector2': vector2})
    filtered_vector2 = (df.loc[df['vector1'] == filtering_element])['vector2'].to_numpy()
    return filtered_vector2

def read_result_multi_variable_multiaircraft_multi_runs(csv_filename, variable_values, variable_name, no_simulation_runs, module_names, kpi_name):
    result = pd.read_csv(csv_filename)
    iter_vars = result.loc[result.type == 'itervar', ['run', 'attrname', 'attrvalue']]
    iter_vars_pivot = iter_vars.pivot(index='run', columns='attrname', values='attrvalue')
    result_merged = result.merge(iter_vars_pivot, left_on='run', right_index=True, how='outer')
    output_row_in_table_format = result_merged[
        (getattr(result_merged, variable_name).isin(variable_values)) &
        (result_merged.type == 'scalar') &
        (result_merged.module.isin(module_names)) &
        (result_merged.name == kpi_name)
    ]
    no_elements_variable_values = len(variable_values)
    array_shape = (no_elements_variable_values, no_simulation_runs, len(output_row_in_table_format) // (no_elements_variable_values * no_simulation_runs))
    result_array = np.zeros(array_shape)
    for i, variable_value in enumerate(variable_values):
        variable_value_df = output_row_in_table_format[output_row_in_table_format[variable_name] == variable_value]
        unique_runs = variable_value_df['run'].unique()
        for j, run in enumerate(unique_runs):
            run_df = variable_value_df[variable_value_df['run'] == run]
            result_array[i, j, :len(run_df)] = run_df['value'].values

    return result_array

def read_result_multi_variable_multiaircraft_multiapps_multi_runs(csv_filename, variable_values, variable_name, no_of_data_applications, no_simulation_runs, module_names, kpi_name):
    result = pd.read_csv(csv_filename)
    iter_vars = result.loc[result.type == 'itervar', ['run', 'attrname', 'attrvalue']]
    iter_vars_pivot = iter_vars.pivot(index='run', columns='attrname', values='attrvalue')
    result_merged = result.merge(iter_vars_pivot, left_on='run', right_index=True, how='outer')
    output_row_in_table_format = result_merged[
        (getattr(result_merged, variable_name).isin(variable_values)) &
        (result_merged.type == 'scalar') &
        (result_merged.module.isin(module_names)) &
        (result_merged.name == kpi_name)
    ]
    no_elements_variable_values = len(variable_values)
    no_of_aircraft = len(output_row_in_table_format) // (no_elements_variable_values * no_simulation_runs * no_of_data_applications)
    array_shape = (no_elements_variable_values, no_simulation_runs, no_of_aircraft, no_of_data_applications)
    result_array = np.zeros(array_shape)

    result_df = output_row_in_table_format.copy()
    result_df['aircraft'] = result_df['module'].str.extract(r'aircraft\[(\d+)]').astype(int)
    result_df['app'] = result_df['module'].str.extract(r'app\[(\d+)]').astype(int)

    pivot_df = result_df.pivot_table(
        index=['run', variable_name, 'aircraft', 'app'],
        values='value',
        aggfunc='first'
    ).reset_index()

    variable_index = {v: i for i, v in enumerate(variable_values)}

    for variable_value, group_df in pivot_df.groupby(variable_name):
        print(f"currently running for: variable: {variable_value}")
        if variable_value not in variable_index:
            continue
        run_index = {v: i for i, v in enumerate(group_df['run'].unique())}
        variable_idx = variable_index[variable_value]
        run_idxs = group_df['run'].map(run_index).values
        aircraft_idxs = group_df['aircraft'].values
        app_idxs = group_df['app'].values
        result_array[variable_idx, run_idxs, aircraft_idxs, app_idxs] = group_df['value'].values
    return result_array

def read_result_multi_modules_aggregated(csv_filename, variable_values, variable_name, no_simulation_runs, module_names, kpi_name):
    result = pd.read_csv(csv_filename)
    iter_vars = result.loc[result.type == 'itervar', ['run', 'attrname', 'attrvalue']]
    iter_vars_pivot = iter_vars.pivot(index='run', columns='attrname', values='attrvalue')
    result_merged = result.merge(iter_vars_pivot, left_on='run', right_index=True, how='outer')
    output_row_in_table_format = result_merged[
        (getattr(result_merged, variable_name).isin(variable_values)) &
        (result_merged.type == 'scalar') &
        (result_merged.module.isin(module_names)) &
        (result_merged.name == kpi_name)
    ]
    no_elements_variable_values = len(variable_values)
    array_shape = (no_elements_variable_values, no_simulation_runs)
    result_array = np.zeros(array_shape)

    result_df = output_row_in_table_format.copy()
    result_df['aircraft'] = result_df['module'].str.extract(r'aircraft\[(\d+)]').astype(int)

    pivot_df = result_df.pivot_table(
        index=['run', variable_name],
        values='value',
        aggfunc='sum'
    ).reset_index()
    pivot_df['run_id'] = pivot_df['run'].str.extract(r'-(\d+)-')
    pivot_df['run_id'] = pivot_df['run_id'].astype(int)

    variable_index = {v: i for i, v in enumerate(variable_values)}

    for var_value in variable_values:
        filtered_df = pivot_df[pivot_df[variable_name] == var_value]

        sorted_df = filtered_df.sort_values(by='run_id')

        var_idx = variable_index[var_value]

        num_runs = min(len(sorted_df), no_simulation_runs)

        result_array[var_idx, :num_runs] = sorted_df['value'].iloc[:num_runs].to_numpy()
    return result_array

def aggregate_vectors(series):
    aggregated_list = [item for item in series if item is not None and isinstance(item, list)]
    return np.concatenate(aggregated_list) if aggregated_list else np.array([])

def read_result_vector_averages_multi_modules_aggregatedsss(csv_filename, variable_values, variable_name, no_simulation_runs, module_names, kpi_name, module='aircraft'):
    result = pd.read_csv(csv_filename)
    iter_vars = result.loc[result.type == 'itervar', ['run', 'attrname', 'attrvalue']]
    iter_vars_pivot = iter_vars.pivot(index='run', columns='attrname', values='attrvalue')
    result_merged = result.merge(iter_vars_pivot, left_on='run', right_index=True, how='outer')
    output_row_in_table_format = result_merged[
        (getattr(result_merged, variable_name).isin(variable_values)) &
        (result_merged.type == 'vector') &
        (result_merged.module.isin(module_names)) &
        (result_merged.name == kpi_name)
    ]
    no_elements_variable_values = len(variable_values)
    array_shape = (no_elements_variable_values, no_simulation_runs)
    result_array = np.zeros(array_shape)

    result_df = output_row_in_table_format.copy()

    print(result_df['module'])
    pattern = fr'{module}\[(\d+)\].app\[(\d+)\]'

    result_df[['groundStation', 'app']] = result_df['module'].str.extract(pattern).astype(int)
    print(result_df)
    result_df['vecvalue'] = result_df['vecvalue'].apply(lambda x: [int(i) for i in x.split()] if isinstance(x, str) else x)

    averages_df = pd.DataFrame(columns=['run', variable_name, 'average'])

    for (run, var), group in result_df.groupby(['run', variable_name]):
        concatenated = np.concatenate(group['vecvalue'].dropna().tolist())

        average = np.nan if concatenated.size == 0 else np.mean(concatenated)

        averages_df = averages_df.append({
            'run': run,
            variable_name: var,
            'average': average
        }, ignore_index=True)

    variable_index = {v: i for i, v in enumerate(variable_values)}

    result_array = np.full((len(variable_values), no_simulation_runs), np.nan)

    for var_value in variable_values:
        filtered_df = averages_df[averages_df[variable_name] == var_value]

        sorted_df = filtered_df.sort_values(by='run')

        var_idx = variable_index[var_value]

        num_runs = min(len(sorted_df), no_simulation_runs)

        result_array[var_idx, :num_runs] = sorted_df['average'].iloc[:num_runs].to_numpy()
    return result_array

def read_result_vector_averages_multi_modules_aggregated(csv_filename, variable_values, variable_name, no_simulation_runs, module_names, kpi_name, module_name_prefix='aircraft'):
    result = pd.read_csv(csv_filename, low_memory=False)
    iter_vars = result.loc[result.type == 'itervar', ['run', 'attrname', 'attrvalue']]
    iter_vars_pivot = iter_vars.pivot(index='run', columns='attrname', values='attrvalue')
    result_merged = result.merge(iter_vars_pivot, left_on='run', right_index=True, how='outer')
    output_row_in_table_format = result_merged[
        (getattr(result_merged, variable_name).isin(variable_values)) &
        (result_merged.type == 'vector') &
        (result_merged.module.isin(module_names)) &
        (result_merged.name == kpi_name)
    ]
    no_elements_variable_values = len(variable_values)
    array_shape = (no_elements_variable_values, no_simulation_runs)
    result_array = np.zeros(array_shape)

    result_df = output_row_in_table_format.copy()
    result_df[module_name_prefix] = result_df['module'].str.extract(fr'{module_name_prefix}\[(\d+)]').astype(int)

    result_df['vecvalue'] = result_df['vecvalue'].apply(lambda x: [float(i) for i in x.split()] if isinstance(x, str) else x)

    averages_df = pd.DataFrame(columns=['run', variable_name, 'average'])

    for (run, var), group in result_df.groupby(['run', variable_name]):
        concatenated = np.concatenate(group['vecvalue'].dropna().tolist())

        average = np.nan if concatenated.size == 0 else np.mean(concatenated)

        averages_df.loc[len(averages_df)] = {
            'run': run,
            variable_name: var,
            'average': average
        }

    variable_index = {v: i for i, v in enumerate(variable_values)}

    result_array = np.full((len(variable_values), no_simulation_runs), np.nan)

    for var_value in variable_values:
        filtered_df = averages_df[averages_df[variable_name] == var_value]

        sorted_df = filtered_df.sort_values(by='run')

        var_idx = variable_index[var_value]

        num_runs = min(len(sorted_df), no_simulation_runs)

        result_array[var_idx, :num_runs] = sorted_df['average'].iloc[:num_runs].to_numpy()
    return result_array

def read_result_vector_percentiles_multi_modules_aggregated(csv_filename, variable_values, variable_name, module_names, kpi_name, percentile, module_name_prefix='aircraft'):
    result = pd.read_csv(csv_filename)

    iter_vars = result.loc[result.type == 'itervar', ['run', 'attrname', 'attrvalue']]
    iter_vars_pivot = iter_vars.pivot(index='run', columns='attrname', values='attrvalue')

    result_merged = result.merge(iter_vars_pivot, left_on='run', right_index=True, how='outer')

    output_row_in_table_format = result_merged[
        (getattr(result_merged, variable_name).isin(variable_values)) &
        (result_merged.type == 'vector') &
        (result_merged.module.isin(module_names)) &
        (result_merged.name == kpi_name)
    ]

    result_df = output_row_in_table_format.copy()

    result_df['module_index'] = result_df['module'].str.extract(fr'{module_name_prefix}\[(\d+)\]').astype(int)

    result_df['vecvalue'] = result_df['vecvalue'].apply(lambda x: [float(i) for i in x.split()] if isinstance(x, str) else x)

    combined_results = {var: [] for var in variable_values}

    for (run, var), group in result_df.groupby(['run', variable_name]):
        concatenated = np.concatenate(group['vecvalue'].dropna().tolist())
        combined_results[var].extend(concatenated)

    percentiles = {var: np.percentile(data, percentile) if len(data) > 0 else np.nan for var, data in combined_results.items()}

    return percentiles

def calculate_percentiles(data_dict, percentiles):
    percentile_results = {}
    for var, data in data_dict.items():
        if len(data) == 0:
            percentile_results[var] = {p: np.nan for p in percentiles}
        else:
            percentile_results[var] = {p: np.percentile(data, p) for p in percentiles}
    return percentile_results

def read_result_vector_averages_multi_modules_multi_apps_aggregated(csv_filename, variable_values, variable_name, no_simulation_runs, module_names, kpi_name, module_name_prefix='groundStation', app_name_prefix='app'):
    result = pd.read_csv(csv_filename, low_memory=False)

    iter_vars = result.loc[result.type == 'itervar', ['run', 'attrname', 'attrvalue']]
    iter_vars_pivot = iter_vars.pivot(index='run', columns='attrname', values='attrvalue')

    result_merged = result.merge(iter_vars_pivot, left_on='run', right_index=True, how='outer')

    output_row_in_table_format = result_merged[
        (getattr(result_merged, variable_name).isin(variable_values)) &
        (result_merged.type == 'vector') &
        (result_merged.module.isin(module_names)) &
        (result_merged.name == kpi_name)
    ]

    no_elements_variable_values = len(variable_values)
    array_shape = (no_elements_variable_values, no_simulation_runs)
    result_array = np.zeros(array_shape)

    result_df = output_row_in_table_format.copy()

    result_df['module_index'] = result_df['module'].str.extract(fr'{module_name_prefix}\[(\d+)\]').astype(int)
    result_df['app_index'] = result_df['module'].str.extract(fr'{app_name_prefix}\[(\d+)\]').astype(int)

    result_df['vecvalue'] = result_df['vecvalue'].apply(lambda x: [float(i) for i in x.split()] if isinstance(x, str) else x)

    averages_df = pd.DataFrame(columns=['run', variable_name, 'average'])

    for (run, var), group in result_df.groupby(['run', variable_name]):
        concatenated = np.concatenate(group['vecvalue'].dropna().tolist())

        average = np.nan if concatenated.size == 0 else np.mean(concatenated)

        row = pd.DataFrame([{'run': run, variable_name: var, 'average': average}])
        averages_df = pd.concat([averages_df, row], ignore_index=True)

    variable_index = {v: i for i, v in enumerate(variable_values)}

    result_array = np.full((len(variable_values), no_simulation_runs), np.nan)

    for var_value in variable_values:
        filtered_df = averages_df[averages_df[variable_name] == var_value]

        sorted_df = filtered_df.sort_values(by='run')

        var_idx = variable_index[var_value]

        num_runs = min(len(sorted_df), no_simulation_runs)

        result_array[var_idx, :num_runs] = sorted_df['average'].iloc[:num_runs].to_numpy()

    return result_array

def read_result_vector_percentiles_multi_modules_multi_apps_aggregated_concatenated(csv_filename, variable_values, variable_name, module_names, kpi_name, percentile, module_name_prefix='groundStation', app_name_prefix='app'):
    result = pd.read_csv(csv_filename)

    iter_vars = result.loc[result.type == 'itervar', ['run', 'attrname', 'attrvalue']]
    iter_vars_pivot = iter_vars.pivot(index='run', columns='attrname', values='attrvalue')

    result_merged = result.merge(iter_vars_pivot, left_on='run', right_index=True, how='outer')

    output_row_in_table_format = result_merged[
        (getattr(result_merged, variable_name).isin(variable_values)) &
        (result_merged.type == 'vector') &
        (result_merged.module.isin(module_names)) &
        (result_merged.name == kpi_name)
    ]

    result_df = output_row_in_table_format.copy()

    result_df['module_index'] = result_df['module'].str.extract(fr'{module_name_prefix}\[(\d+)\]').astype(int)
    result_df['app_index'] = result_df['module'].str.extract(fr'{app_name_prefix}\[(\d+)\]').astype(int)

    result_df['vecvalue'] = result_df['vecvalue'].apply(lambda x: [float(i) for i in x.split()] if isinstance(x, str) else x)

    concatenated_data = {var: [] for var in variable_values}

    for (run, var), group in result_df.groupby(['run', variable_name]):
        concatenated = np.concatenate(group['vecvalue'].dropna().tolist())
        concatenated_data[var].extend(concatenated)

    percentiles = {var: np.percentile(data, percentile) if len(data) > 0 else np.nan for var, data in concatenated_data.items()}

    return percentiles

def dist(n1, n2):
    """Euclidean distance"""
    return ((n1[0] - n2[0])**2 + (n1[1] - n2[1])**2 + (n1[2] - n2[2])**2)**0.5

def create_graph(coordinates):
    """Create graph from coordinates"""
    G = nx.Graph()
    node_id = 0
    for x, y, z in coordinates:
        G.add_node((x, y, z,node_id), x=x, y=y, z=z, id=node_id, width=1)
        node_id = node_id + 1
    return G

def  graph_edges_in_range(coordinates, radius=1, a2g_range=370400, GSx =4734222.285, GSy=1381949.583,GSz=662813.2938):
    "" "Insert edges into the graph G based on commnication range" ""
    G = create_graph(coordinates)
    number_of_nodes = G.number_of_nodes()
    ground_station=(GSx,GSy,GSz,number_of_nodes-1)
    for  c1  in  G . nodes ():
        if c1 == ground_station:
            for c2 in G.nodes():
                d = dist(c1, c2)
                if d <= a2g_range:
                    G.add_edge(c1, c2)
        else:
            for  c2  in  G . nodes ():
                if c2 == ground_station:
                    d = dist(c1, c2)
                    if d <= a2g_range:
                        G.add_edge(c1, c2)
                else:
                    d  =  dist ( c1 ,  c2 )
                    if d <= radius:
                        G . add_edge ( c1 ,  c2 )
    return G

def  gg ( coordinates, radius=1 ):
    "" "Insert edges according to the GG rules into the graph G" ""
    G = create_graph(coordinates)
    for  c1  in  G . nodes ():
        for  c2  in  G . nodes ():
            d  =  dist ( c1 ,  c2 )
            for  possible_blocker  in  G . nodes ():
                midpoint = [(c1[0] + c2[0]) * 0.5, (c1[1] + c2[1]) * 0.5, (c1[2] + c2[2]) * 0.5]
                distTomidpoint = dist(possible_blocker, midpoint)
                distc1Tomidpoint = dist(c1, midpoint)
                if  distTomidpoint  <  distc1Tomidpoint:
                    break
            else :
                if d <=radius:
                    G . add_edge ( c1 ,  c2 )
    return G

def  rng ( coordinates, radius=1 ):
    "" "Insert edges according to the RNG rules into the graph G" ""
    G = create_graph(coordinates)
    for  c1  in  G . nodes ():
        for  c2  in  G . nodes ():
            d  =  dist ( c1 ,  c2 )
            for  possible_blocker  in  G . nodes ():
                distToC1  =  dist ( possible_blocker ,  c1 )
                distToC2  =  dist ( possible_blocker , c2 )
                if  distToC1  <  d  and  distToC2  <  d :
                    break
            else :
                if d <=radius:
                    G . add_edge ( c1 ,  c2 )
    return G

def flatten(t):
    return [item for sublist in t for item in sublist]
