import shutil
from pathlib import Path

import numpy as np
import pandas as pd
from allensdk.brain_observatory.ecephys.ecephys_project_cache import EcephysProjectCache

data_directory = Path(r"D:\AllenBrainObservatory\ephys_data")

manifest_path = data_directory / "manifest.json"

cache = EcephysProjectCache.from_warehouse(manifest=manifest_path)

sessions = cache.get_session_table()
arr = np.concatenate(list(sessions["ecephys_structure_acronyms"]))
good_vals = np.array([v for v in arr if str(v) != "nan"])
un = np.unique(good_vals)
print(un)

print("Total number of sessions: " + str(len(sessions)))

print(sessions.head())

## Grab data from the sessions

filtered_sessions = sessions[
    (sessions.sex == "M")
    & (sessions.full_genotype.str.find("Sst") > -1)
    & (sessions.session_type == "brain_observatory_1.1")
    & (["VISl" in acronyms for acronyms in sessions.ecephys_structure_acronyms])
]

print(filtered_sessions.head())

probes = cache.get_probes()

print("Total number of probes: " + str(len(probes)))

print(probes.head())

channels = cache.get_channels()

print("Total number of channels: " + str(len(channels)))

print(channels.head())

units = cache.get_units()

print("Total number of units: " + str(len(units)))

units = cache.get_units(
    amplitude_cutoff_maximum=np.inf,
    presence_ratio_minimum=-np.inf,
    isi_violations_maximum=np.inf,
)

print("Total number of units: " + str(len(units)))

analysis_metrics1 = cache.get_unit_analysis_metrics_by_session_type(
    "brain_observatory_1.1"
)

analysis_metrics2 = cache.get_unit_analysis_metrics_by_session_type(
    "functional_connectivity"
)

print(str(len(analysis_metrics1)) + " units in table 1")
print(str(len(analysis_metrics2)) + " units in table 2")

analysis_metrics1 = cache.get_unit_analysis_metrics_by_session_type(
    "brain_observatory_1.1",
    amplitude_cutoff_maximum=np.inf,
    presence_ratio_minimum=-np.inf,
    isi_violations_maximum=np.inf,
)

analysis_metrics2 = cache.get_unit_analysis_metrics_by_session_type(
    "functional_connectivity",
    amplitude_cutoff_maximum=np.inf,
    presence_ratio_minimum=-np.inf,
    isi_violations_maximum=np.inf,
)

all_metrics = pd.concat([analysis_metrics1, analysis_metrics2], sort=False)

print(str(len(all_metrics)) + " units overall")

## Take out one session from all of this
session = cache.get_session_data(
    filtered_sessions.index.values[0],
    isi_violations_maximum=np.inf,
    amplitude_cutoff_maximum=np.inf,
    presence_ratio_minimum=-np.inf,
)

print([attr_or_method for attr_or_method in dir(session) if attr_or_method[0] != "_"])

probe_id = session.probes.index.values[0]

lfp = session.get_lfp(probe_id)
