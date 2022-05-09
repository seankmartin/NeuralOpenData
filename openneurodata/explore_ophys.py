import pprint
from pathlib import Path
from urllib.parse import urljoin

import dtale
import matplotlib.pyplot as plt
import psutil
import requests
# Can also directly instantiate a BehaviorOphysExperiment
from allensdk.brain_observatory.behavior.behavior_ophys_experiment import \
    BehaviorOphysExperiment
from allensdk.brain_observatory.behavior.behavior_project_cache import \
    VisualBehaviorOphysProjectCache
from tqdm import tqdm

HERE = Path(__file__).parent.absolute()
MANIFEST_VERSION = "1.0.1"
DATA_STORAGE_DIRECTORY = Path(r"D:\AllenBrainObservatory\ophys_data")


def get_behavior_ophys_experiment_url(ophys_experiment_id: int) -> str:
    hostname = "https://visual-behavior-ophys-data.s3-us-west-2.amazonaws.com/"
    object_key = f"visual-behavior-ophys/behavior_ophys_experiments/behavior_ophys_experiment_{ophys_experiment_id}.nwb"
    return urljoin(hostname, object_key)


def get_path_to_nwb(session_id):
    fname = (
        DATA_STORAGE_DIRECTORY
        / f"visual-behavior-ophys-{MANIFEST_VERSION}"
        / "behavior_ophys_experiments"
        / f"behavior_ophys_experiment_{session_id}.nwb"
    )
    return fname


def manual_download(session_id):
    url = get_behavior_ophys_experiment_url(session_id)
    response = requests.get(url, stream=True)
    fname = get_path_to_nwb(session_id)

    with open(fname, "wb") as handle:
        for data in tqdm(response.iter_content()):
            handle.write(data)


def already_downloaded(session_id):
    return get_path_to_nwb(session_id).exists()


def download_all_data(cache, ophys_container_ids, filtered_experiments, manual=False):
    # Try to download some big containers
    # behaviour_table = cache.get_behavior_session_table(as_df=True)
    session_table = cache.get_ophys_session_table(as_df=True)
    experiment_table = cache.get_ophys_experiment_table(as_df=True)

    for container_id in ophys_container_ids:
        sst_container_experiments = filtered_experiments[
            filtered_experiments.ophys_container_id == container_id
        ]
        if len(sst_container_experiments) >= 5:
            print(container_id)
            print(sst_container_experiments)
            # fig, ax = plt.subplots(1, len(sst_container_experiments), figsize=(20, 5))
            print("RAM memory usage out", psutil.virtual_memory())
            for i, (experiment_id, _) in enumerate(
                sst_container_experiments.iterrows()
            ):
                if already_downloaded(experiment_id):
                    session_id = experiment_table["ophys_session_id"].loc[experiment_id]
                    behavior_id = session_table["behavior_id"].loc[session_id]
                    _ = cache.get_behavior_session(behavior_id)
                if manual:
                    manual_download(experiment_id)
                else:
                    _ = cache.get_behavior_ophys_experiment(
                        ophys_experiment_id=experiment_id
                    )


def plot_mpis(cache, ophys_container_ids, filtered_experiments):
    for container_id in ophys_container_ids:
        sst_container_experiments = filtered_experiments[
            filtered_experiments.ophys_container_id == container_id
        ]
        if len(sst_container_experiments) >= 5:
            fig, ax = plt.subplots(1, len(sst_container_experiments), figsize=(20, 5))
            for i, (experiment_id, _) in enumerate(
                sst_container_experiments.iterrows()
            ):
                try:
                    dataset = cache.get_behavior_ophys_experiment(
                        ophys_experiment_id=experiment_id
                    )
                except OSError:
                    path_to_file = get_path_to_nwb(experiment_id)
                    print("Error opening {}, redownloading...".format(path_to_file))
                    path_to_file.unlink()
                    dataset = cache.get_behavior_ophys_experiment(
                        ophys_experiment_id=experiment_id
                    )
                ax[i].imshow(dataset.max_projection.data, cmap="gray")
                ax[i].set_title(experiment_id)
                fig.savefig(HERE / "figures" / f"{container_id}_mip.png", dpi=400)
                plt.close(fig)


def main():
    Path.mkdir(HERE / "figures", exist_ok=True)

    cache = VisualBehaviorOphysProjectCache.from_s3_cache(
        cache_dir=DATA_STORAGE_DIRECTORY
    )
    behavior_ophys_experiments = cache.get_ophys_experiment_table()

    # Grab 2P experiments
    project_filter = (
        behavior_ophys_experiments.project_code == "VisualBehaviorMultiscope"
    )
    # Let us stick to the excitatory line
    genotype_filter = (
        behavior_ophys_experiments.full_genotype
        == "Slc17a7-IRES2-Cre/wt;Camk2a-tTA/wt;Ai93(TITL-GCaMP6f)/wt"
    )
    filtered_experiments = behavior_ophys_experiments[project_filter & genotype_filter]

    # dtale.show(filtered_experiments).open_browser()

    # grab the containers from this
    ophys_container_ids = filtered_experiments.ophys_container_id.unique()

    download_all_data(cache, ophys_container_ids, filtered_experiments)
    plot_mpis(cache, ophys_container_ids, filtered_experiments)


#### OTHER INFO BELOW HERE

# In this dataset, we have 3 cre_lines, 'Slc17a7-IRES2-Cre', which labels excitatory neurons across all cortical layers, 'Sst-IRES-Cre' which labels somatostatin expressing inhibitory interneurons, and 'Vip-IRES-Cre', which labels vasoactive intestinal peptide expressing inhibitory interneurons. There are also 3 reporter_lines, 'Ai93(TITL-GCaMP6f)' which expresses the genetically encoded calcium indicator GCaMP6f (f is for 'fast', this reporter has fast offset kinetics, but is only moderately sensitive to calcium relative to other sensors) in cre labeled neurons, 'Ai94(TITL-GCaMP6s)' which expresses the indicator GCaMP6s (s is for 'slow', this reporter is very sensitive to calcium but has slow offset kinetics), and 'Ai148(TIT2L-GC6f-ICL-tTA2', which expresses GCaMP6f using a self-enhancing system to achieve higher expression than other reporter lines (which proved necessary to label inhibitory neurons specifically). The specific indicator expressed by each reporter_line also has its own column in the table.

# for ophys_experiment_id, _ in behavior_ophys_experiments.iterrows():
#     try:
#         _ = cache.get_behavior_ophys_experiment(ophys_experiment_id=ophys_experiment_id)
#     except OSError:
#         path_to_file = (
#             data_storage_directory
#             / "visual-behavior-ophys-1.0.1"
#             / "behavior_ophys_experiments"
#             / f"behavior_ophys_experiment_{ophys_experiment_id}.nwb"
#         )
#         print("Error opening {}, redownloading...".format(path_to_file))
#         path_to_file.unlink()
#         _ = cache.get_behavior_ophys_experiment(ophys_experiment_id=ophys_experiment_id)

# See end of https://allensdk.readthedocs.io/en/latest/_static/examples/nb/visual_behavior_ophys_dataset_manifest.html

# import matplotlib.pyplot as plt
# # ophys_experiment_ids are the index of the ophys_experiment_table
# ophys_experiment_ids = sst_container_experiments.index.values

# # create figure axis
# fig, ax = plt.subplots(1, len(ophys_experiment_ids), figsize=(20,5))
# # enumerate over experiments in this container
# for i, ophys_experiment_id in enumerate(ophys_experiment_ids):
#     # get the dataset object
#     dataset = cache.get_behavior_ophys_experiment(ophys_experiment_id=ophys_experiment_id)
#     # get the max intensity projection and plot on the appropriate axis
#     ax[i].imshow(dataset.max_projection.data, cmap='gray')
#     ax[i].set_title(ophys_experiment_id)

# behavior_sessions.head()
# behavior_ophys_sessions.head()

# Download data like this
# behavior_session = cache.get_behavior_session(behavior_session_id=870987812)
# print(behavior_session.list_data_attributes_and_methods())

# And ophys data like this
# ophys_experiment = cache.get_behavior_ophys_experiment(ophys_experiment_id=951980471)

# Can iterate over ophys data here to keep downloading

# Filtering out only the 2P imaging, which is in VISp and VISl

# Let us visualise this
# dtale.show(behavior_ophys_experiments).open_browser()
# inp = input("Press Enter to continue after viewing dtale...")

# See imaging_depth and targeted_structure


if __name__ == "__main__":
    main()
