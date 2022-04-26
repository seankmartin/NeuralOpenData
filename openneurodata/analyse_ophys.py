def summarise_single_session(allen_dataset):

    ## Summary in print
    print(
        f"-----------Working on image plane {allen_dataset.ophys_experiment_id}"
        f"session {allen_dataset.ophys_session_id}------------"
    )
    print(f"\tThis experiment has metadata {allen_dataset.metadata}")
    cell_specimen_table = allen_dataset.cell_specimen_table
    print(
        f"\tThere are {len(cell_specimen_table)} cells"
        f"in this session with IDS {cell_specimen_table['cell_specimen_id']}"
    )
    methods = allen_dataset.list_data_attributes_and_methods()
    print(f"The available information is {methods}")

    ## Plotting other information
