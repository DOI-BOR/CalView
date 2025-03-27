# -------------------------------------------------------------------
# DSS File reader 0.1
# Sam Waers, P.E.; Frankie Nuffer-Rodriguez
#
# Run this file in same directory as dssReadFuncs.py
# See the "import" statements at the top of  in dssReadFuncs.py
# for a list of dependencies which will need to be installed
# in the environment you use for this script.
# -------------------------------------------------------------------

# Import data handling functions from our local module
from csdss_readlib_fullfile import file_reader, pickler, load_pickles, get_trend_fields
from cs3_plotlib import plot_values, plot_time_group, plot_time_exceedance, plot_single_var
import time
import panel as pn
from panel.io import hold
# NOTE: need to use name/main for Pool to work outside of script
# pn.extension(template='bootstrap')
pn.extension(sizing_mode='stretch_width')
#
# def update_plots(
#     scen_selector,
#     var_selector,
#     unit_selector,
#     df_all_data_ts,
#     c_default_units,
# ):
#     ts_data = plot_values(
#         scenario_list=scen_selector,
#         var_list=var_selector,
#         unit_choice=unit_selector,
#         df_all=df_all_data_ts,
#         c_default_units_all=c_default_units
#     )
#
#     ts_diffs = plot_values(
#         scenario_list=scen_selector,
#         var_list=var_selector,
#         unit_choice=unit_selector,
#         df_all=df_all_data_ts_diffs,
#         c_default_units_all=c_default_units
#     )
#
#     return [
#         pn.pane.HoloViews(ts_data),
#         pn.pane.HoloViews(ts_diffs)
#     ]


# This is where main would go if it didn't give panel a headache

start_time = time.time()

# 'make_pickles' is switch to save time when repeatedly pulling
# the same list of variables from the same files.
# You can set this to false after the first time you read the
# specific list of variables below from the set of the specific
# set of files below.
# If you change either list, you need to make pickles again.
make_archive = False

# List of runs. If not storing DSS files in the same directory,
# provide full paths or paths relative to this file.
# structure is [["Description_1", ("File_1.dss")],
#               ["Description_2", ("File_2.dss")],
#          ...  ["Description_n", ("File_n.dss")]]
# The names can be anything though, e.g. ["Alt2v1", Alt2v1_VAs.dss"]
runs = [
    ["Baseline", ("Baseline.dss")],
    ["Alt2", ("Alt2.dss")],
    ["Alt3", ("Alt3.dss")],
    # ["Alt3", ("CS3DV_Iter1.dss")],
    # ["Alt4", ("CS3DV_Iter2.dss")],
    # ["Alt5", ("CS3DV_Iter3.dss")],
    # ["Alt6", ("CS3DV_Iter4.dss")],
    # ["Alt7", ("CS3DV_Iter5.dss")],
    # ["Alt8", ("CS3DV_Iter6.dss")],
]

l_tr_fields = get_trend_fields()

# This is a list of the variables you want to retrieve.
# These correspond to the B part in the DSS pathname.
# Variables that are not present in all runs are thrown out
# though this behavior can be changed if needed.
add_field_list: list = [
    "test",
    "WYT_SJR_",
    "WYT_SJR_STAN_",
    "S_MELON",
    "C_MELON",
    "C_STS059",
    "D_STS059_OAK001",
    "D_STS059_UFC000",
    "D_WDWRD_61_PA3",
    "D_STS059_SSJ001",
    "D_SSJ004_61_PA1",
    "D_OAK020_61_PA2",
    "C_LJC022",
    "C_LJC010",
    "D_LJC010_60S_PA2",
    "D_LJC022_WTPWDH",
    "D_LJC022_60S_PA1",
    "D_CLV026_60S_PA1",
    "D_CLV026_WTPWDH",
    "D_WTPDWS_60S_NU1",
    "D_MOK035_WTPDWS",
    "D_SJR028_WTPDWS",
    "C_MELONVA",
    "S_SHSTA"
]
s_default = 'S_SHSTA'

field_list = l_tr_fields + add_field_list

# Only do this step if we are creating pickles. Otherwise, read the data
# from existing pickles. Facilitates quickly jumping back into analysis
# without having to load from DSS files.
if make_archive == True:
    append_list, baseline_stack, c_default_units = file_reader(runs, field_list)
    pickler(append_list, baseline_stack, c_default_units)

    # This runs no matter what. The pickle files allow you to come back and
    # pull the same variables without waiting for the file reads to complete
    df_all_data, df_diffs, c_default_units = load_pickles()

    # Write to Excel.
    try:
        df_all_data.to_excel("DSS_contents.xlsx")
    except:
        print("Error writing output file. "
              "Make sure 'DSS_contents.xlsx' is not open.")


print(f'Total runtime: {(time.time()-start_time)/60} minutes')
print(f'Pulled: {len(runs)} files')

# 2.3 minutes for 9 files


# This runs no matter what. The pickle files allow you to come back and
# pull the same variables without waiting for the file reads to complete
df_all_data, df_diffs, c_default_units = load_pickles()

scenario_names = df_all_data['Scenario'].unique().tolist()
var_names = df_all_data.columns.to_list()[6:]

# Select which alts to examine
scen_selector = pn.widgets.MultiChoice(
    name='Scenario selector',
    options=scenario_names,
    value=scenario_names,
    width=400
)

# Select the variables
var_selector = pn.widgets.MultiChoice(
    name='Variable selector',
    options=var_names,
    #value=[var_names[0]],
    width=400
)

unit_selector = pn.widgets.RadioButtonGroup(
    name='Units selector',
    options=['TAF', 'CFS'],
    button_style='outline',
    button_type='primary',
    width=200
)

period_selector = pn.widgets.Select(
    name='Period selector',
    options={"Water Year":"WY", "Calendar Year":"DY", "Contract Year":"CY",
             "January":1, "February":2, "March":3, "April":4,
                   "May":5, "June":6, "July":7, "August":8,
                   "September":9, "October":10, "November":11, "December":12},
    width=200
)

# Select a single
single_var_selector = pn.widgets.Select(
    name='Single variable selector',
    options=var_names,
    value=var_names[0]
)

month_sel = pn.widgets.Select(
    name='Month selector',
    options = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"]
)

stat_sel = pn.widgets.Select(
    name='Statistic selector',
    options=['Average', 'Minimum', 'Maximum']
)

# 20241223: Create different dataframes for each function call
# Trying to fix non-independent plots issue
df_all_data_ts = df_all_data.copy(deep=True)
df_all_data_ts_diffs = df_diffs.copy(deep=True)
# Okay, so separate dfs isn't cutting it.
# Try turning off y-lim

bound_plot_ts = pn.bind(
    plot_values,
    scenario_list=scen_selector,
    var_list=var_selector,
    unit_choice=unit_selector,
    df_all=df_all_data_ts,
    c_default_units_all=c_default_units
)

bound_plot_diffs_ts = pn.bind(
    plot_values,
    scenario_list=scen_selector,
    var_list=var_selector,
    unit_choice=unit_selector,
    df_all=df_all_data_ts_diffs,
    c_default_units_all=c_default_units
)

bound_plot_grouped = pn.bind(
    plot_time_group,
    scenario_list=scen_selector,
    var_list=var_selector,
    unit_choice=unit_selector,
    df_all=df_all_data,
    c_default_units_all=c_default_units,
    period_choice=period_selector
)

bound_plot_grouped_diff = pn.bind(
    plot_time_group,
    scenario_list=scen_selector,
    var_list=var_selector,
    unit_choice=unit_selector,
    df_all=df_diffs,
    c_default_units_all=c_default_units,
    period_choice=period_selector
)

bound_plot_exceedance = pn.bind(
    plot_time_exceedance,
    scenario_list=scen_selector,
    var_list=var_selector,
    unit_choice=unit_selector,
    df_all=df_all_data,
    c_default_units_all=c_default_units,
    period_choice=period_selector
)

bound_plot_diffs_exceedance = pn.bind(
    plot_time_exceedance,
    scenario_list=scen_selector,
    var_list=var_selector,
    unit_choice=unit_selector,
    df_all=df_diffs,
    c_default_units_all=c_default_units,
    period_choice=period_selector
)

bound_single_var_plot = pn.bind(
    plot_single_var,
    df=df_all_data,
    period_choice=period_selector,
    variable=single_var_selector,
    scenario_list=scen_selector,
    units_choice=unit_selector,
    stat_choice=stat_sel,
    c_default_units=c_default_units
)

bound_single_var_diff_plot = pn.bind(
    plot_single_var,
    df=df_diffs,
    period_choice=period_selector,
    variable=single_var_selector,
    scenario_list=scen_selector,
    units_choice=unit_selector,
    stat_choice=stat_sel,
    c_default_units=c_default_units
)

logo = pn.pane.JPG(
    'site_contents/usbr_logo.jpg',
    height=75
)

title = pn.pane.Markdown("""
    # DSS Results Viewer for CalSim 3
    ### USBR Technical Service Center
    -----------------------------------
    ###  
    """,
    width=600
)

ts_title = pn.pane.Markdown("""
    # Timeseries Plot
""")

diffs_ts_title = pn.pane.Markdown("""
    # Timeseries Plot (Difference from Baseline)
""")

grouped_title = pn.pane.Markdown("""
    # Time-Aggregated Plot
""")

grouped__diff_title = pn.pane.Markdown("""
    # Time-Aggregated Plot (Difference from Baseline)
""")

exceedance_title = pn.pane.Markdown("""
    # Exceedance Plot 
""")

exceedance_diff_title = pn.pane.Markdown("""
    # Exceedance Plot (Difference from Baseline)
""")

single_var_title = pn.pane.Markdown("""
    # Single Variable Comparison
""")

single_var_diff_title = pn.pane.Markdown("""
    # Single Variable Comparison (Difference from Baseline)
""")

logo_name = pn.Row(logo, title, width=750)

header = pn.Row(scen_selector, var_selector,
                period_selector, unit_selector
                )

single_var_widgets = pn.Row(single_var_selector, stat_sel, width=750)

single_var_plots = pn.Column(single_var_widgets,
                             pn.Row(
                                 pn.Column(
                                     single_var_title,
                                     bound_single_var_plot),
                                 pn.Column(
                                     single_var_diff_title,
                                     bound_single_var_diff_plot)
                                 )
                             )

timeseries_plots = pn.Row(
    pn.Column(
        ts_title,
        bound_plot_ts),
    pn.Column(
        diffs_ts_title,
        bound_plot_diffs_ts)
)

grouped_plots = pn.Row(
    pn.Column(
        grouped_title,
        bound_plot_grouped),
    pn.Column(
        grouped__diff_title,
        bound_plot_grouped_diff)
)

exceedance_plots = pn.Row(
    pn.Column(
        exceedance_title,
        bound_plot_exceedance),
    pn.Column(
        exceedance_diff_title,
        bound_plot_diffs_exceedance)
)


template = pn.template.BootstrapTemplate(
    title="DSS Results Viewer for CalSim 3",
    logo='site_contents/usbr_logo.jpg',
    header_background='white',
    header_color='black'
)
tabs = pn.Tabs(('Single Variable', single_var_plots),
        ('Timeseries', timeseries_plots),
        ('Time-Aggregated', grouped_plots),
        ('Exceedance', exceedance_plots))

template.main.append(header)
# template.main.append(single_var_widgets)
# template.main.append(single_var_plots)
# template.main.append(timeseries_plots)
# template.main.append(grouped_plots)
# template.main.append(exceedance_plots)
template.main.append(tabs)
template.servable()
# gridbox = pn.layout.GridBox(
#     objects = pn.bind(
#         update_plots(
#             scen_selector,
#             var_selector,
#             unit_selector,
#             df_all_data_ts,
#             c_default_units
#         ),
#     ncols=2,
#     sizing_mode="stretch_both"
#     )
# )

