def calculate_parameter(shrub_cover, understory_cover):
    return shrub_cover + understory_cover


def collect_field_data(num_plots):
    field_data = []
    for plot in range(1, num_plots + 1):
        print(f"Enter data for Sample Plot {plot}:")
        shrub_cover = float(input("Shrub Cover (%): "))
        understory_cover = float(input("Understory Cover (%): "))
        field_data.append((shrub_cover, understory_cover))
    return field_data


def calculate_parameters_for_plots(field_data):
    parameters = []
    for shrub_cover, understory_cover in field_data:
        parameter = calculate_parameter(shrub_cover, understory_cover)
        parameters.append(parameter)
    return parameters


def calculate_average_parameter(parameters):
    return sum(parameters) / len(parameters)


# Main program
if __name__ == "__main__":
    num_plots = 2
    field_data = collect_field_data(num_plots)
    parameters = calculate_parameters_for_plots(field_data)
    average_parameter = calculate_average_parameter(parameters)
    print(f"Parameter values for {num_plots} sample plots: {parameters}")
    print(f"Average Parameter Value: {average_parameter}")
