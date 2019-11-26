import av3.merge.importer as imp
from av3.util.paths import path_output_data, path_input_data

dfs = imp.gen_start_files(root=path_input_data, quantidade=1)

dfs[0].to_csv(path_output_data + "merge_train.csv", index=False)
dfs[1].to_csv(path_output_data + "merge_test.csv", index=False)
dfs[2].to_csv(path_output_data + "merge_aux.csv", index=False)
