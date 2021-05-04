# This file contains all the statistical calculations just to keep main nice and tidy
import time
import numpy as np
import Global_Variables as gv


def statistics(sperm_total, sim_start_time, sim_fin_time, sperm_objs):

    success_sperm_count = sperm_total - gv.failed_sperm_count

    # calculate average, fastest and slowest convergence rates
    avg_convergence = 0
    fastest_convergence = np.inf
    slowest_convergence = 0
    for sperm in sperm_objs:
        convergence_time = sperm.fin_time - sperm.start_time

        # if the sperm founnd the egg the include them in convergence statistics
        if sperm.egg_found:

            avg_convergence += convergence_time
            if convergence_time < fastest_convergence:
                fastest_convergence = convergence_time

            if convergence_time > slowest_convergence:
                slowest_convergence = convergence_time

    # calculate mean using total number of successful sperm
    if not success_sperm_count:
        avg_convergence = 0
    else:
        avg_convergence = avg_convergence/success_sperm_count

    # Formatting output
    print("Data Collected:")
    print("---------------------------------------------------------------------------------------------------------\n")
    print("Time elapsed: ", sim_fin_time, " s\n")
    print("Sperm population: ", sperm_total)
    print("Number of failed sperm: ", gv.failed_sperm_count)
    print("Number of successful sperm: ", success_sperm_count)
    print("Success percentage: ", round((success_sperm_count/sperm_total) * 100, 2), "%")
    print("\n---------------------------------------------------------------------------------------------------------"
          "\n")
    print("Fastest convergence rate: ", round(fastest_convergence, 3), " Seconds")
    print("Slowest convergence rate: ", round(slowest_convergence, 3), " Seconds")
    print("Average convergence rate: ",round(avg_convergence, 3), " Seconds")
    print("\n---------------------------------------------------------------------------------------------------------")


# prints statistics live to the
def live_stats(sperm_total, sim_start_time):
    success_sperm_count = sperm_total - gv.failed_sperm_count
    print("Current time: ", time.time() - sim_start_time)
    print("Percentage Converged: ", round((success_sperm_count/sperm_total) * 100, 2), "%\n")
