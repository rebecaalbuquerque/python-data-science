import importer as imp

dfs = imp.gen_start_files(quantidade=1)

dfs[0].to_csv("merge_train.csv", index=False)
dfs[1].to_csv("merge_test.csv", index=False)
dfs[2].to_csv("merge_aux.csv", index=False)
