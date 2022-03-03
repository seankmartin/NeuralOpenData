from pathlib import Path
import pprint

# Can also directly instantiate a BehaviorOphysExperiment
from allensdk.brain_observatory.behavior.behavior_ophys_experiment import (
    BehaviorOphysExperiment,
)
from allensdk.brain_observatory.behavior.behavior_project_cache import (
    VisualBehaviorOphysProjectCache,
)

data_storage_directory = Path("/local1/visual_behavior_ophys_cache_dir")
data_storage_directory = Path(r"D:\AllenBrainObservatory\ophys_data")

cache = VisualBehaviorOphysProjectCache.from_s3_cache(cache_dir=data_storage_directory)
# This class uses a 'manifest' to keep track of downloaded data and metadata.
# All downloaded files will be stored relative to the directory holding the manifest
# file.  If 'manifest_file' is a relative path (as it is below), it will be
# saved relative to your working directory.  It can also be an absolute path.

behavior_sessions = cache.get_behavior_session_table()

print(f"Total number of behavior sessions: {len(behavior_sessions)}")

behavior_sessions.head()

behavior_ophys_sessions = cache.get_ophys_session_table()

print(f"Total number of behavior + ophys sessions: {len(behavior_ophys_sessions)}")

behavior_ophys_sessions.head()

# Download data like this
behavior_session = cache.get_behavior_session(behavior_session_id=870987812)
print(behavior_session.list_data_attributes_and_methods())
behavior_ophys_experiments = cache.get_ophys_experiment_table()

# And ophys data like this
ophys_experiment = cache.get_behavior_ophys_experiment(ophys_experiment_id=951980471)

# Can iterate over ophys data here to keep downloading
for ophys_experiment_id, _ in behavior_ophys_experiments.iterrows():
    try:
        _ = cache.get_behavior_ophys_experiment(ophys_experiment_id=ophys_experiment_id)
    except OSError:
        path_to_file = (
            data_storage_directory
            / "visual-behavior-ophys-1.0.1"
            / "behavior_ophys_experiments"
            / f"behavior_ophys_experiment_{ophys_experiment_id}.nwb"
        )
        print("Error opening {}, redownloading...".format(path_to_file))
        path_to_file.unlink()
        _ = cache.get_behavior_ophys_experiment(ophys_experiment_id=ophys_experiment_id)
