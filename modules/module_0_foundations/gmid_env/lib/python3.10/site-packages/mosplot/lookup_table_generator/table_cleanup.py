import numpy as np

class LookupTableCleaner:
    def __init__(self, lookup_table, parameters_to_save):
        self.lookup_table = lookup_table
        self.parameters_to_save = parameters_to_save

    def compress_array(self, array):
        # Check if all entries are equal.
        first_val = array.flat[0]
        if np.all(array == first_val):
            # If all are zero, return None to signal removal.
            if first_val == 0:
                return None
            # Return scalar value if constant and nonzero.
            return np.array([first_val])
        return array

    def clean_lookup_table(self):
        # Track which parameters remain after cleaning.
        parameters_found = set()
        for model in self.lookup_table:
            param_dict = self.lookup_table[model]
            keys_to_remove = []
            for param, data in param_dict.items():
                new_data = self.compress_array(data)
                # If new_data is None, mark parameter for removal.
                if new_data is None:
                    keys_to_remove.append(param)
                else:
                    param_dict[param] = new_data
                    parameters_found.add(param)
            # Remove keys with all zero values.
            for key in keys_to_remove:
                del param_dict[key]
        # Remove parameters removed from all models.
        self.parameters_to_save[:] = [p for p in self.parameters_to_save if p in parameters_found]

