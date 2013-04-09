import numpy as np
import matplotlib.pyplot as plt
from scipy import stats as scistats

#FILENAME = "benchmark-ant-ksat_11_first.txt"
#FILENAME = "benchmark-ant-ksat_11_num_ants.txt"
#FILENAME = "benchmark_genetic_full.txt"
FILENAME = "benchmark_genetic_ksat3_all_parameters.txt"
SELECT = lambda i: i['TIME'] != -1 #True #i["FILENAME"] == "benchmark_instances/random_ksat11.dimacs"

IGNORE = ["EXP_PH", "SEED", "TIME", "EPSILON", "SOLVED_SUCCESSFULLY", "FILENAME", "MAX_ITERATIONS", "PH_REDUCE_FACTOR", "WEIGHT_ADAPTION_DURATION", "BASIC_BLUR", "BLUR_DECLINE", "CATASTROPHES_BOUNDS", "CATASTROPHES", "NUM_NEW_RANDOM"]

instances = []

for i, line in enumerate(open(FILENAME, "r").readlines()):
  inst = eval(line)
  if SELECT(inst):
    if inst['TIME'] == -2:
      inst.update({'TIME': 45})
    instances.append(inst)

buckets = {}
stats = {}
relevant_params = sorted(list(set(instances[0].keys()) - set(IGNORE)))
print "graph for", relevant_params

for param in relevant_params:
  buckets[param] = {}
  stats[param] = {}

for i in instances:
  for param in relevant_params:
    if i[param] not in buckets[param].keys():
      buckets[param][i[param]] = []
      stats[param][i[param]] = {}

    buckets[param][i[param]].append(i)

graph_values = []
graph_xlabels = []
graph_stdvalues = []
graph_pos = []
graph_params = []
current_pos = 0

for param in relevant_params:
  graph_values_for_param = []
  graph_stdvalues_for_param = []
  graph_xlabels_for_param = []
  graph_pos_for_param = []

  for value in sorted(buckets[param].keys()):
    values = [i["TIME"] for i in buckets[param][value]]
    stats[param][value]["arith_avg"] = np.mean(values)
    stats[param][value]["geo_avg"] = scistats.gmean(values)
    stats[param][value]["std_dev"] = np.std(values)
    print  np.std(values)
    print values
     
    stddev_value = stats[param][value]["std_dev"]/10.0 
    graph_values_for_param.append(stats[param][value]["geo_avg"])
    graph_stdvalues_for_param.append(stddev_value)
    graph_xlabels_for_param.append(value)
    graph_pos_for_param.append(current_pos)
    current_pos += 1

  graph_values.append(graph_values_for_param)
  graph_stdvalues.append(graph_stdvalues_for_param)
  graph_xlabels.append(graph_xlabels_for_param)
  graph_pos.append(graph_pos_for_param)
  graph_params.append(param)
  current_pos += 0.5

colors = ["#31FF9B", "#139FF7", "#FB0013", "#0E00AC", "#FDAF30", "#FC6121", "#720008", "#E8F351"]

fig = plt.figure()
ay = fig.add_subplot(1,1,1)
ay.yaxis.grid(color='gray', linestyle='dashed')
ay.set_axisbelow(True) 
ax = fig.add_subplot(111)

rects = []

for index in range(len(graph_values)):
  print graph_pos[index], graph_values[index]
  rects.append(ax.bar(graph_pos[index], graph_values[index], 0.8, color=colors[index], yerr=graph_stdvalues[index]))

#rects1 = ax.bar(bar_pos[0], vals[0], 0.8, color="#116688" )

ax.legend([r[0] for r in rects], graph_params, loc=0)  # 0: right bottom
ax.set_ylabel("runtime (seconds)")
ax.set_xlabel("parameter values")
ax.set_yticks(np.arange(5))

flat_graph_pos = [item for sublist in graph_pos for item in sublist]
print flat_graph_pos

ax.set_xlim((-0.5,22))

ax.set_xticks(np.array(flat_graph_pos)+0.4)
flat_graph_xlabels = [item for sublist in graph_xlabels for item in sublist]
ax.set_xticklabels(flat_graph_xlabels)

plt.show()


