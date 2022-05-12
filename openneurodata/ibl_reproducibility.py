"""See https://int-brain-lab.github.io/iblenv/notebooks_external/data_release_repro_ephys.html"""

from one.api import ONE

pw = "international"
one = ONE(
    base_url="https://openalyx.internationalbrainlab.org", password=pw, silent=True
)

# Find sessions that have data and are tagged for the repeated site paper
rep_site_sessions = one.alyx.rest(
    "sessions",
    "list",
    dataset_types="spikes.times",
    tag="2022_Q2_IBL_et_al_RepeatedSite",
)
# Take the first session
example_sess = rep_site_sessions[0]
# Each session has a unique experiment id
eid = example_sess["id"]

# Download all data in alf collection
files = one.load_collection(eid, "alf", download_only=True)

# Show where files have been downloaded to
print(f"Files downloaded to {files[0].parent}")

insertion = one.alyx.rest("insertions", "list", session=eid)[0]
probe_label = insertion["name"]
files = one.load_collection(eid, f"alf/{probe_label}/pykilosort", download_only=True)

# Show where files have been downloaded to
print(f"Files downloaded to {files[0].parent}")

# Load in all trials datasets
trials = one.load_object(eid, "trials", collection="alf")

# Load in a single wheel dataset
wheel_times = one.load_dataset(eid, "_ibl_wheel.timestamps.npy")
